## Kyverno vcluster ClusterPolicy - secret

This package installs a Kyverno `ClusterPolicy` able to find a `vCluster` secret and to populate using a template
the Argocd `cluster` secret that Argocd will use to access each vCluster !

**Remark**: The matching rule used part of the policy is looking to one of the worker's names: worker-1, worker-2 ... worker-5. Such a hard coded list of values should be defined as a parameter if we convert the `generate-secrets` package into a helm chart to get rid of that !

Such an issue comes from the fact that the use of variables like `{{ vclusterName }}` in the match block of a rule is not allowed by Kyverno.
Variables can only be used in the generate or context sections, so match blocks must rely on static values or label selectors.
Additionally, attempting to use wildcards in the names field (e.g., "vc-*") doesn't work either, as Kyverno expects exact names there.
To match secrets dynamically, you must list full names or switch to using labels.