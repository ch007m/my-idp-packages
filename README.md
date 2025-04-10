## IDP Packages

To install a package, pass the url reference using the package name and `//`

Example:
```shell
set REPO_IDP_PACKAGES https://github.com/ch007m/my-idp-packages

idp create \
   --color \
   --name idplatform \
   --dev-password \
   -p $REPO_IDP_PACKAGES//external-secrets \
   -p $REPO_IDP_PACKAGES//tekton
```

## Packages

| Package name                         | Version | comment                                    | Project                                                          |
|--------------------------------------|---------|--------------------------------------------|------------------------------------------------------------------|
| [external-secrets](external-secrets) | 0.15.1  | Unique yaml file generated from Helm chart | https://external-secrets.io/latest/introduction/getting-started/ |
| [tekton](tekton)                     | v0.62.8 | Kustomize project                          | https://github.com/tektoncd/pipeline/                            