## Kratix - new agent

This package creates Argo CD Application files to allow the kratix `agent` (Argocd, Fluxcd, etx) deployed on a cluster to access its `GitStateStore` and to fetch the resources to be installed within the cluster.

**Note**: Several agents can be created as this package uses an Argo cd `ApplicationSet` file !!

TODO: Review if we could install Argo CD within each vcluster without doing it manually !

Connect to each vcluster to install Argo CD
```shell
❯ vcluster connect worker-1
17:13:36 done vCluster is up and running
17:13:37 info Starting background proxy container...
17:13:37 done Switched active kube context to vcluster_worker-1_worker-1_kind-idplatform
- Use `vcluster disconnect` to return to your previous kube context
- Use `kubectl get namespaces` to access the vcluster

❯ kubectl create namespace argocd
  kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
 
❯ k get pods -n argocd
NAME                                               READY   STATUS    RESTARTS   AGE
argocd-application-controller-0                    1/1     Running   0          80s
argocd-applicationset-controller-9cbb56dff-wzfbp   1/1     Running   0          81s
argocd-dex-server-74d5d76d7-5c8hq                  1/1     Running   0          81s
argocd-notifications-controller-68459f6cbb-szrdt   1/1     Running   0          81s
argocd-redis-794f68fb68-4mw7q                      1/1     Running   0          81s
argocd-repo-server-864476c5cf-rzmwb                1/1     Running   0          81s
argocd-server-6496dc8859-mv7bb                     1/1     Running   0          80s  
```

Change within the [kratix-new-agent.yaml](kratix-new-agent.yaml) file the name of the cluster as registered part of the Argo cd instance running on kratix and the repository path

**Note**: Refer to the list of the Argo CD `clusters` under the UI: `https://argocd.cnoe.localtest.me:8443/settings/clusters` to verify the name of the cluster to be set

```yaml
spec:
  generators:
    - list:
        elements:
          - clusterName: worker-1
            repoPath: worker-1
          - clusterName: worker-2
            repoPath: worker-2
...
```

The information to access the Gitea Kratix StateStore are defined with the following Helm values which can be overridden using the field `valuesObject` of the [Application](kratix-new-agent.yaml) resource file:
  
```yaml
clusterName: worker-1 # Name of the cluster where the agent is running
giteaServer:
  url: http://<HOST_IP_ADDRESS>:<NODE_PORT> # or <INGRESS_URL>:<IDP_PORT> like : gitea.cnoe.localtest.me:8443
  username: "giteaAdmin"
  password: "developer"

gitKratix:
  org: kratix # Kratix git organization 
  repository: state # Kratix StateStore repository 
```