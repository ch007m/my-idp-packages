#!/usr/bin/env python3

import os
from pathlib import Path

# Environment-like variables (you can also read from os.environ if needed)
PACKAGE_NAME = os.getenv("PACKAGE_NAME", "kubernetes-dashboard").lower()
PACKAGE_VERSION = os.getenv("PACKAGE_VERSION", "7.11.1")

CHART_REPO_URL = os.getenv("CHART_REPO_URL", "https://kubernetes.github.io/dashboard/")
CHART_REPO_NAME = os.getenv("CHART_REPO_NAME", PACKAGE_NAME)
CHART_NAME = os.getenv("CHART_NAME", PACKAGE_NAME)
CHART_RELEASE_NAME = os.getenv("CHART_RELEASE_NAME", PACKAGE_NAME)
TARGET_NAMESPACE = os.getenv("TARGET_NAMESPACE", PACKAGE_NAME)

INSTALL_YAML = os.getenv("INSTALL_YAML", "manifests/install.yaml")
ARGO_APPLICATION_YAML = f"{PACKAGE_NAME}.yaml"
SCRIPT_FILE = "generate-manifests.sh"

# Paths
package_path = Path(PACKAGE_NAME)
install_yaml_path = package_path / INSTALL_YAML
script_path = package_path / SCRIPT_FILE
values_yaml_path = package_path / "values.yaml"
argo_app_path = package_path / ARGO_APPLICATION_YAML

# Create directory structure
install_yaml_path.parent.mkdir(parents=True, exist_ok=True)

# Create empty install.yaml
install_yaml_path.touch(exist_ok=True)

# Create generate-manifests.sh content
script_content = f"""#!/usr/bin/env bash
set -e
cd $(dirname "$0")

# env variable to be added to your .env file => PACKAGE_VERSION
if [[ -n $PACKAGE_VERSION ]]; then
  CHART_VERSION=$PACKAGE_VERSION
else
  CHART_VERSION=0.1.0
fi

echo "# {PACKAGE_NAME.upper()} INSTALL RESOURCES" > {INSTALL_YAML}
echo "# This file is auto-generated with '{PACKAGE_NAME}/generate-manifests.sh'" >> {INSTALL_YAML}

helm repo add {PACKAGE_NAME} --force-update {CHART_REPO_URL}
helm repo update
helm template -n {TARGET_NAMESPACE} {CHART_RELEASE_NAME} {CHART_REPO_NAME}/{PACKAGE_NAME} -f values.yaml --version $CHART_VERSION >> {INSTALL_YAML}
"""

script_path.write_text(script_content)
os.chmod(script_path, 0o755)

# Create values.yaml
values_yaml_path.touch(exist_ok=True)

# Create ArgoCD Application YAML
argo_content = f"""# Git repository of the chart/project: $CHART_CODE_REPO
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {PACKAGE_NAME}
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  destination:
    namespace: {TARGET_NAMESPACE}
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

argo_app_path.write_text(argo_content)
