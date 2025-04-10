#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [[ -n $EXTERNAL_SECRETS_CHART_VERSION ]]; then
  CHART_VERSION=$EXTERNAL_SECRETS_CHART_VERSION
else
  CHART_VERSION="0.15.1"
fi

INSTALL_YAML="manifests/install.yaml"

echo "# EXTERNAL SECRETS INSTALL RESOURCES" >${INSTALL_YAML}
echo "# This file is auto-generated with 'external-secrets/generate-manifests.sh'" >>${INSTALL_YAML}

helm repo add external-secrets --force-update https://charts.external-secrets.io
helm repo update
helm template --namespace external-secrets external-secrets external-secrets/external-secrets -f values.yaml --version ${CHART_VERSION} >>${INSTALL_YAML}