# Collection of IDP Packages

This project references IDP packages that you can install top of a kind cluster created using the tool: [idpbuilder](https://github.com/cnoe-io/idpbuilder/).

<!-- INCLUDE:sorted.md -->

To install a package or more, pass the git url of this project along the name of the package. 

**Note**: As mentioned [within the kustomize documentation](https://github.com/kubernetes-sigs/kustomize/blob/master/examples/remoteBuild.md#remote-directories), The directory or package name is specified by appending a `//` after the repo URL

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

## How to add a new IDP package's project

To create a `new IDP package` directory packaging one of the following options:

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