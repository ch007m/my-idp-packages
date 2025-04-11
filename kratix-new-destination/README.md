## Kratix - new destination

This package performs the following steps when it is needed to create a new Kratix [Destination](https://docs.kratix.io/main/reference/destinations/intro):

- Deploy on the `main` kratix instance a new `Destination` CR 
- Create, using a kubernetes job, a new path under the GitStateStore (gitea.cnoe.localtest.me:8443) where `resources` will be published

It is possible to customize the `Destination` to be generated and registered using the following parameters within the [kratix-new-destination.yaml](kratix-new-destination.yaml) file
```yaml
- clusterName: worker1 # name of the target kubernetes cluster and Destination
  repoPath: worker-1   # Path to access the resources files within the GitStateStore
  environment: test    # Environment's label
  team: team-a         # Team's label
```

The information to access the Gitea Kratix StateStore are defined with the following Helm values which can also be overridden under the field `valuesObject` of the ApplicationSet resource file:
```yaml

stateStore:
  kind: GitStateStore
  reference: gitea

  username: giteaAdmin
  password: developer

  gitOrgName: kratix
  gitStateRepoName: state
  gitApiUrl: https://gitea.cnoe.localtest.me:8443/api
```