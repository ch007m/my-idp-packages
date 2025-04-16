#!/usr/bin/env python3

import os
import subprocess
import requests
import yaml
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def prompt(text, default=None):
    prompt_text = f"{text} [{default}]: " if default else f"{text}: "
    user_input = input(prompt_text).strip()
    return user_input if user_input else default

def get_default_token():
    try:
        result = subprocess.run(
            ["idpbuilder", "get", "secrets", "-p", "gitea", "-o", "json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        import json
        secrets = json.loads(result.stdout)
        return secrets[0]["token"] if secrets else ""
    except Exception as e:
        print(f"⚠️ Failed to fetch default token: {e}")
        return ""

def create_gitea_repo(gitea_url, token, idp_name, repo_name, package_name, package_path):
    api_url = f"{gitea_url.rstrip('/')}/api/v1"
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }

    # Check if repo already exists
    check_response = requests.get(
        f"{api_url}/repos/giteaAdmin/{repo_name}",
        headers=headers,
        verify=False
    )

    if check_response.status_code == 200:
        confirm = input(f"⚠️ Repository '{repo_name}' already exists. Do you want to delete and recreate it? [y/N]: ").strip().lower()
        if confirm == 'y':
            delete_response = requests.delete(
                f"{api_url}/repos/giteaAdmin/{repo_name}",
                headers=headers,
                verify=False
            )
            if delete_response.status_code != 204:
                print(f"❌ Failed to delete repo: {delete_response.status_code} {delete_response.text}")
                return None
            print(f"🗑️ Deleted existing repo '{repo_name}'.")
        else:
            print("❌ Aborted by user.")
            return None

    repo_data = {
        "name": repo_name,
        "private": False,
        "auto_init": False
    }

    response = requests.post(
        f"{api_url}/user/repos",
        headers=headers,
        json=repo_data,
        verify=False  # adjust based on certs
    )

    if response.status_code == 201:
        print("✅ Repository created.")
        remote_url = f"{gitea_url.rstrip('/')}/giteaAdmin/idpbuilder-{idp_name}-{package_name}-{package_path}.git"
        print("\n📦 To push your local files, run the following commands:\n")
        print("    git init")
        print("    git checkout -b main")
        print("    git add .")
        print('    git commit -m "First commit"')
        print(f"    git remote add origin {remote_url}")
        print("    git push -u origin main")
        print("\n")
        return response.json()["clone_url"]
    else:
        print(f"❌ Failed to create repo: {response.status_code} {response.text}")
        return None

def patch_argocd_yaml(file_path, gitea_url, package_name):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    spec = data.get("spec", {})
    source = spec.get("source", {})

    repo_url = source.get("repoURL", "")
    if repo_url.startswith("cnoe://"):
        rel_path = repo_url.replace("cnoe://", "")
        source["repoURL"] = gitea_url

        if rel_path:
            if not source.get("path"):
                source["path"] = rel_path
            else:
                source["path"] = os.path.join(rel_path, source["path"])

        data["spec"]["source"] = source

        patched_filename = f"{package_name}-patched.yaml"
        with open(package_name + "/"+ patched_filename, "w") as f:
          yaml.safe_dump(data, f)
        print("✅ ArgoCD YAML patched.")
    else:
        print("ℹ️ No 'cnoe://' repoURL found, nothing to patch.")

def main():
    print("🔧 Welcome to the Gitea Repo + ArgoCD Patch CLI")

    gitea_url = prompt("Enter Gitea URL", "https://gitea.cnoe.localtest.me:8443")
    token = prompt("Enter Gitea token", get_default_token())
    idp_name = prompt("Enter the idp name", "idplatform")
    package_name = prompt("Enter package name")
    package_path = prompt("Enter package_path", "manifests")
    yaml_path = prompt("Enter ArgoCD YAML file path")

    if not package_name or not yaml_path:
        print("❌ repo_name and yaml_path are required.")
        return

    if not os.path.isfile(yaml_path):
        print("❌ File not found:", yaml_path)
        return

    repo_name = "idpbuilder" + "-" + idp_name + "-" + package_name + "-" + package_path

    clone_url = create_gitea_repo(gitea_url, token, idp_name, repo_name, package_name, package_path)
    if clone_url:
        patch_argocd_yaml(yaml_path, clone_url, package_name)

if __name__ == "__main__":
    main()
