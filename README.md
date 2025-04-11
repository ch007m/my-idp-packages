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

| Package name                                   | Version                         | comment                                                                 | Project                                      |
|------------------------------------------------|---------------------------------|-------------------------------------------------------------------------|----------------------------------------------|
| [cert-manager](cert-manager)                   | v1.15.0                         | Kustomize project combining external resource(s)                        | https://github.com/cert-manager/cert-manager |
| [cert-trust-manager](cert-trust-manager)       | v1.17.1 (cert), v0.16.0 (trust) | Helm deployment through Argo CD Application                             | https://github.com/cert-manager/cert-manager |
| [external-secrets](external-secrets)           | 0.15.1                          | Yaml file generated from Helm chart with bash script                    | https://external-secrets.io/latest/          |
| [kubernetes-dashboard](kubernetes-dashboard)   | 7.11.1                          | Yaml file generated from Helm chart with bash script                    | https://github.com/kubernetes/dashboard      |
| [kyverno-policy-secret](kyverno-policy-secret) | n/a                             | Kustomize project of local resource(s)                                  |                                              |
| [kyverno](kyverno)                             | 3.3.7                           | Helm deployment through Argo CD Application + some customized resources | https://kyverno.io/                          |
| [tekton](tekton)                               | v0.62.8                         | Kustomize project combining external resources and local files          | https://github.com/tektoncd/pipeline/        |
| [vcluster](vcluster)                           | 0.24.0  | Helm deployment through Argo CD Application                             | https://www.vcluster.com/docs                |

## How to add a new package's project

To create a `new package` directory packaging one of the following options:

- Kustomize files, 
- Script able to generate from helm a YAML resources file,
- An Argo CD Application file installing a Helm chart

use the following python script by defining the `package name` and by specifying the type: helm, kustomize or argocd

**Note**: Different env variables are available to customize the package project:

```shell
// export them or add thelm to your .env file
PACKAGE_NAME=kubernetes-dashboard
PROJECT_TYPE=helm
PACKAGE_VERSION=7.11.1
CHART_CODE_REPO=https://github.com/kubernetes/dashboard
CHART_REPO_URL=https://kubernetes.github.io/dashboard/
CHART_REPO_NAME=kubernetes-dashboard
CHART_NAME=kubernetes-dashboard
CHART_RELEASE_NAME=kubernetes-dashboard
TARGET_NAMESPACE=kubernetes-dashboard

❯ ./scripts/generate-project-package.py
Please enter the package name (default: my-package): 
Please enter the project type (default: helm, options: helm, kustomize, argocd): 
Package Name: my-package
Project Type: helm

🚧 Generating a 'helm' project for the package: my-package

✅ Created generate-manifests.sh
✅ Created README.md
✅ Created my-package.yaml
```
Enjoy ;-)
