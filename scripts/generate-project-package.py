#!/usr/bin/env python3

import os
import argparse
from pathlib import Path

# Function to get environment variables with fallback defaults
def get_env_var(var_name, default_value):
    return os.getenv(var_name, default_value)

# Function to create README.md
def create_readme(package_name: str, folder: Path):
    content = f"# {package_name}\n\nThe {package_name} installs on the IDPlatform the following project:"
    (folder / "README.md").write_text(content)
    print(f"✅ Created README.md")

# Function to create Argocd Application YAML file to install a Helm Chart
def create_argocd_chart_yaml(package_name: str, target_namespace: str, chart_repo_url: str, chart_version: str, chart_name: str, folder: Path):
    content = f"""# Git repository of the chart/project: $CHART_CODE_REPO
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {package_name}
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  destination:
    namespace: {target_namespace}
    server: "https://kubernetes.default.svc"
  source:
    repoURL: {chart_repo_url}
    targetRevision: {chart_version}
    chart: {chart_name}
    helm:
      valuesObject:
  project: default
  syncPolicy:
    automated:
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
"""
    (folder / f"{package_name}.yaml").write_text(content)
    print(f"✅ Created {package_name}.yaml")

# Function to create Argocd Application YAML file
def create_argocd_yaml(package_name: str, target_namespace: str, folder: Path):
    content = f"""# Git repository of the chart/project: $CHART_CODE_REPO
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {package_name}
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  destination:
    namespace: {target_namespace}
    server: "https://kubernetes.default.svc"
  source:
    repoURL: cnoe://manifests
    targetRevision: HEAD
    path: "."
  project: default
  syncPolicy:
    automated:
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
"""
    (folder / f"{package_name}.yaml").write_text(content)
    print(f"✅ Created {package_name}.yaml")

# Function to create the generate-manifests.sh script
def create_generate_manifest_script(package_name: str, install_yaml: str, chart_repo_url: str, chart_release_name: str, target_namespace: str, folder: Path):
    script_content = f"""#!/usr/bin/env bash
set -e
cd $(dirname "$0")

if [[ -n $PACKAGE_VERSION ]]; then
  CHART_VERSION=$PACKAGE_VERSION
else
  CHART_VERSION=0.1.0
fi

echo "# {package_name.upper()} INSTALL RESOURCES" > {install_yaml}
echo "# This file is auto-generated with '{package_name}/generate-manifests.sh'" >> {install_yaml}

helm repo add {package_name} --force-update {chart_repo_url}
helm repo update
helm template -n {target_namespace} {chart_release_name} {package_name}/{package_name} -f values.yaml --version $CHART_VERSION >> {install_yaml}
"""
    script_path = folder / "generate-manifests.sh"
    script_path.write_text(script_content)
    os.chmod(script_path, 0o755)
    print("✅ Created generate-manifests.sh")

# Function to create files for Helm type package
def create_helm_files(package_name: str, base_path: Path, chart_repo_url: str, target_namespace: str):
    install_yaml_path = base_path / "manifests" / "install.yaml"
    install_yaml_path.parent.mkdir(parents=True, exist_ok=True)
    install_yaml_path.touch(exist_ok=True)

    (base_path / "values.yaml").touch(exist_ok=True)

    create_generate_manifest_script(
        package_name=package_name,
        install_yaml="manifests/install.yaml",
        chart_repo_url=chart_repo_url,
        chart_release_name=package_name,
        target_namespace=target_namespace,
        folder=base_path,
    )
    create_readme(package_name, base_path)
    create_argocd_yaml(package_name, target_namespace, base_path)

# Function to create files for Kustomize type package
def create_kustomize_files(package_name: str, base_path: Path):
    kustomize_path = base_path / "manifests"
    kustomize_path.mkdir(parents=True, exist_ok=True)

    kustomization_file = kustomize_path / "kustomization.yaml"
    kustomization_file.write_text("""---
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
""")
    print("✅ Created kustomization.yaml")

    create_readme(package_name, base_path)
    create_argocd_yaml(package_name, package_name, base_path)

# Function to create files for ArgoCD type package
def create_argocd_files(package_name: str, base_path: Path):
    create_readme(package_name, base_path)
    create_argocd_yaml(package_name, package_name, base_path)

def main():
    # Read environment variables
    PACKAGE_NAME = get_env_var("PACKAGE_NAME", "").lower()
    PACKAGE_VERSION = get_env_var("PACKAGE_VERSION", "").lower()
    PROJECT_TYPE = get_env_var("PROJECT_TYPE", "helm").lower()
    CHART_REPO_URL = get_env_var("CHART_REPO_URL","")
    CHART_REPO_NAME = get_env_var("CHART_REPO_NAME", PACKAGE_NAME)
    CHART_NAME = get_env_var("CHART_NAME", PACKAGE_NAME)
    CHART_RELEASE_NAME = get_env_var("CHART_RELEASE_NAME", PACKAGE_NAME)
    TARGET_NAMESPACE = get_env_var("TARGET_NAMESPACE", PACKAGE_NAME)

    # Argument parsing
    parser = argparse.ArgumentParser(description="Scaffold a project package")
    parser.add_argument("--package", "-p", help="The package name")
    parser.add_argument("--type", "-t", choices=["helm", "kustomize", "argocd"], help="Type of project to generate")
    args = parser.parse_args()

    if not args.package:
        package_name = input(f"Please enter the package name (default: {PACKAGE_NAME}): ").strip() or PACKAGE_NAME
    else:
        package_name = args.package

    if not args.type:
        project_type = input(f"Please enter the project type (default: {PROJECT_TYPE}, options: helm, kustomize, argocd): ").strip().lower() or PROJECT_TYPE
    else:
        project_type = args.type

    print(f"Package Name: {package_name}")
    print(f"Project Type: {project_type}")

    print(f"\n🚧 Generating a '{project_type}' project for the package: {package_name}\n")

    base_path = Path(package_name)
    base_path.mkdir(exist_ok=True)

    if project_type == "helm":
        create_helm_files(package_name, base_path, CHART_REPO_URL, TARGET_NAMESPACE)
    elif project_type == "kustomize":
        create_kustomize_files(package_name, base_path)
    elif project_type == "argocd":
        create_argocd_chart_yaml(package_name, TARGET_NAMESPACE, CHART_REPO_URL, PACKAGE_VERSION, CHART_NAME, base_path)
    else:
        print("❌ Unknown type! Use one of: helm, kustomize, argocd.")

if __name__ == "__main__":
    main()