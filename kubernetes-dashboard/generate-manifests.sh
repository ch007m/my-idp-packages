#!/usr/bin/env bash
set -e
cd $(dirname "$0")

# env variable to be added to your .env file => PACKAGE_VERSION
if [[ -n $PACKAGE_VERSION ]]; then
  CHART_VERSION=$PACKAGE_VERSION
else
  CHART_VERSION=0.1.0
fi

echo "# KUBERNETES-DASHBOARD INSTALL RESOURCES" > manifests/install.yaml
echo "# This file is auto-generated with 'kubernetes-dashboard/generate-manifests.sh'" >> manifests/install.yaml

helm repo add kubernetes-dashboard --force-update https://kubernetes.github.io/dashboard/
helm repo update
helm template -n kubernetes-dashboard kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard -f values.yaml --version $CHART_VERSION >> manifests/install.yaml

