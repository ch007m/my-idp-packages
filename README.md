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

| Package name                                   | Version | comment                                                                 | Project                                                          |
|------------------------------------------------|---------|-------------------------------------------------------------------------|------------------------------------------------------------------|
| [external-secrets](external-secrets)           | 0.15.1  | Yaml file generated from Helm chart with bash scrip                     | https://external-secrets.io/latest/                              |
| [external-secrets](external-secrets)           | 0.15.1  | Yaml file generated from Helm chart with bash script                    | https://external-secrets.io/latest/introduction/getting-started/ |
| [kubernetes-dashboard](kubernetes-dashboard)   | 7.11.1  | Yaml file generated from Helm chart with bash script                    | https://github.com/kubernetes/dashboard                          |
| [kyverno-policy-secret](kyverno-policy-secret) | n/a     |                                                                         |                                                                  |
| [kyverno](kyverno)                             | 3.3.7   | Helm deployment through Argo CD Application + some customized resources | https://kyverno.io/                                              |
| [tekton](tekton)                               | v0.62.8 | Kustomize project combining external resources and local files          | https://github.com/tektoncd/pipeline/                            |

## How to add a new package

To create a `new package` directory  where the yaml resource files should be populated from a helm chart using `helm template`, execute the following script. 

**Note**: Different env variables are available to customize the package project: 

```shell
// export them or add thelm to your .env file
PACKAGE_NAME=kubernetes-dashboard
PACKAGE_VERSION=7.11.1
CHART_REPO_URL=https://kubernetes.github.io/dashboard/
CHART_REPO_NAME=kubernetes-dashboard
CHART_NAME=kubernetes-dashboard
CHART_RELEASE_NAME=kubernetes-dashboard
TARGET_NAMESPACE=kubernetes-dashboard

./scripts/new-package-project.sh
```

