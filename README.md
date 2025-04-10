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

| Package name                         | Version | comment                                                        | Project                                                          |
|--------------------------------------|---------|----------------------------------------------------------------|------------------------------------------------------------------|
| [external-secrets](external-secrets) | 0.15.1  | Unique yaml file generated from Helm chart with bash script    | https://external-secrets.io/latest/introduction/getting-started/ |
| [tekton](tekton)                     | v0.62.8 | Kustomize project combining external resources and local files | https://github.com/tektoncd/pipeline/                            |

## New package

To create a `new package` directory  where the resources should be populated from a helm chart, execute the following script. Different env variables are available to configure the project: 

```shell
// export them or add thelm to your .env file
PACKAGE_NAME=kubernetes-dashboard666
PACKAGE_VERSION=7.11.1
CHART_REPO_URL=https://kubernetes.github.io/dashboard/
CHART_REPO_NAME=kubernetes-dashboard
CHART_NAME=kubernetes-dashboard
CHART_RELEASE_NAME=kubernetes-dashboard
TARGET_NAMESPACE=kubernetes-dashboard

./scripts/new-package-project.sh
```

