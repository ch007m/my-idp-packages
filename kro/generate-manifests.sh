#!/usr/bin/env bash
set -e
cd $(dirname "$0")

if [[ -n $PACKAGE_VERSION ]]; then
  CHART_VERSION=$PACKAGE_VERSION
else
  CHART_VERSION=0.2.3
fi

echo "# KRO INSTALL RESOURCES" > manifests/install.yaml
echo "# This file is auto-generated with 'kro/generate-manifests.sh'" >> manifests/install.yaml

helm template -n kro kro oci://ghcr.io/kro-run/kro/kro --version $CHART_VERSION -f values.yaml >> manifests/install.yaml
