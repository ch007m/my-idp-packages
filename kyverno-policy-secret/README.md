## Kyverno vcluster ClusterPolicy - secret

This package installs a Kyverno `ClusterPolicy` able to find a `vCluster` secret and to populate using a template
the Argocd `cluster` secret that Argocd will use to access each vCluster !

**Remark**: The matching rule used part of the policy is looking to one of the worker's names: worker-1, worker-2 ... worker-5. Such a hard coded list of values should be defined as a parameter if we convert the `generate-secrets` package into a helm chart to get rid of that !