## Tekton

This package installs the CI/CD [Tekton](https://tekton.io/) engine on an IDPlatform like the [Tekton Dashboard](https://tekton.dev/docs/dashboard/).

To avoid the `Certificate signed by an unknow authority` error when images will be pushed on the registry, execute the following command to get the idpbuilder CA cert and to create a configmap patching Tekton. The configMap should be created before to deploy the package !
```shell
kubectl get secret -n default idpbuilder-cert -ojson | jq -r '.data."ca.crt"' | base64 -d > $(pwd)/tekton/cert
kubectl create configmap -n tekton-pipelines config-registry-cert \
  --from-file=$(pwd)/tekton/cert \
  --dry-run='client' \
  -o yaml > $(pwd)/tekton/manifests/overlays/config-registry-cert-cm.yml
```
