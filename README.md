## IDP Packages

To install a package, pass the url reference using the package name and `//`

Example:
```shell
set REPO_IDP_PACKAGES https://github.com/ch007m/my-idp-packages

idp create \
   --color \
   --name idpplatform \
   --dev-password \
   -p $REPO_IDP_PACKAGES//external-secrets \
   -p $REPO_IDP_PACKAGES//tekton
```

## Packages

- [external-secrets](external-secrets) - https://external-secrets.io/latest/introduction/getting-started/
- [tekton](tekton) - https://github.com/tektoncd/pipeline/