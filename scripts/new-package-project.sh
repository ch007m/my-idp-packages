#!/usr/bin/env bash
set -e

# The following bash script will create for a new package the following directory structure and files
# package-name/
#   manifests/
#     install.yaml
#   generate-manifests.sh
#   values.yaml
#
# and generate the content of the install.yaml using the generate.sh file
#

# The package name should be equivalent to the chart name or chart repo name
# To be defined as lower case name: "external-secrets", "kubernetes-dashboard"
PACKAGE_NAME=${PACKAGE_NAME:-kubernetes-dashboard}
# See the version to be used as defined within the chart index.yaml file
PACKAGE_VERSION=${PACKAGE_VERSION:-7.11.1}

CHART_REPO_URL=${CHART_REPO_URL:-https://kubernetes.github.io/dashboard/}
CHART_REPO_NAME=${CHART_REPO_NAME:-$PACKAGE_NAME}
CHART_NAME=${CHART_NAME:-$PACKAGE_NAME}
CHART_RELEASE_NAME=${CHART_RELEASE_NAME:-$PACKAGE_NAME}
TARGET_NAMESPACE=${TARGET_NAMESPACE:-PACKAGE_NAME}

INSTALL_YAML=${INSTALL_YAML:-manifests/install.yaml}
ARGO_APPLICATION_YAML=${PACKAGE_NAME:-application}.yaml
SCRIPT_FILE="generate-manifests.sh"

mkdir -p $PACKAGE_NAME/$(dirname $INSTALL_YAML)
touch $PACKAGE_NAME/$INSTALL_YAML

echo "#!/usr/bin/env bash
set -e
cd \$(dirname \"\$0\")

# env variable to be added to your .env file => PACKAGE_VERSION
if [[ -n \$PACKAGE_VERSION ]]; then
  CHART_VERSION=\$PACKAGE_VERSION
else
  CHART_VERSION=0.1.0
fi

echo \"# ${PACKAGE_NAME^^} INSTALL RESOURCES\" > ${INSTALL_YAML}
echo \"# This file is auto-generated with 'kubernetes-dashboard/generate-manifests.sh'\" >> ${INSTALL_YAML}

helm repo add $PACKAGE_NAME --force-update $CHART_REPO_URL
helm repo update
helm template -n $TARGET_NAMESPACE $CHART_RELEASE_NAME $CHART_REPO_NAME/$PACKAGE_NAME -f values.yaml --version $CHART_VERSION >> ${INSTALL_YAML}
" > $PACKAGE_NAME/$SCRIPT_FILE

touch $PACKAGE_NAME/values.yaml

touch $PACKAGE_NAME/$ARGO_APPLICATION_YAML
echo "apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: $PACKAGE_NAME
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  destination:
    namespace: $TARGET_NAMESPACE
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
      - CreateNamespace=true" > $PACKAGE_NAME/$ARGO_APPLICATION_YAML