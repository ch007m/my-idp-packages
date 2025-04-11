## Kratix - new agent

This package creates two Argo CD Application files to allow to the kratix `agent` (Argocd, Fluxcd, etx) deployed on a cluster to access its `GitStateStore`
to fetch the resources to be installed within the cluster.

The information to access the Gitea Kratix StateStore are defined with the following Helm values which can be overridden using the field `valuesObject` of the [Application](kratix-new-agent.yaml) resource file:
  
```yaml
clusterName: worker1 # Name of the cluster where the agent is running
giteaServer:
  url: http://<HOST_IP_ADDRESS>:<NODE_PORT> # or <INGRESS_URL>:<IDP_PORT> like : gitea.cnoe.localtest.me:8443
  username: "giteaAdmin"
  password: "developer"

gitKratix:
  org: kratix # Kratix git organization 
  repository: state # Kratix StateStore repository 
```