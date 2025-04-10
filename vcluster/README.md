## vcluster

This package create several Argo CD Application (from an Applicationset) able to create a vcluster - https://www.vcluster.com/docs on a kubernetes cluster.

As each vcluster is exposed behind its Kubernetes API; it is then needed to create a Secret containing the kubeconfig that Argocd (or users) will use to access them and to register it as [Cluster](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#clusters).

To populate such an Argo CD secret, you will have to install the packages: 
- [kyverno](../kyverno) 
- [kyverno-policy-secret](../kyverno-policy-secret)

To create 2 vclusters: `worker-1` and `worker-2` using idpbuilder, then execute the following command
```shell
idpbuilder create \
  --color \
  --dev-password \
  --name idplatform \
  --port 8443 \
  -p vcluster \
  -p kyverno --recreate  
```
**Note**: You can add more vclusters or change the properties of the section `spec/generators/list/elements[]` by editing locally the ApplicationSet file: [vcluster.yaml](vcluster/vcluster.yaml) which is used to create the clusters.