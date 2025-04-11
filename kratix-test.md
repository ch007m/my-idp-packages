## Instructions to install kratix with 2 vclusters

See TODO and create the cluster using NodePort as needed to access the Gitea Server from a vcluster

echo "git clone this project: https://github.com/ch007m/my-idp-packages; cd my-idp-packages"
echo "Step 0: To create 2 vclusters: worker-1 and worker-2"
idpbuilder create \
  --color \
  --dev-password \
  --name idplatform \
  --port 8443 \
  -p vcluster \
  -p kyverno --recreate

echo "Step 1: Create the TLSconfig as Argocd Secret for the 2 vclusters"
idpbuilder create \
  --color \
  --dev-password \
  --name idplatform \
  --port 8443 \
  -p vcluster \
  -p kyverno \
  -p kyverno-policy-secret

echo "Step 2: Installing the kratix pre-requisites (cert manager, etc) and kratix"
idpbuilder create \
  --color \
  --dev-password \
  --name idplatform \
  --port 8443 \
  -p vcluster \
  -p kyverno \
  -p kyverno-policy-secret \
  -p cert-manager \
  -p kratix

echo "Step 3: Execute the job creating the Gitea Org: kratix and StateStore repository: state"
idpbuilder create \
  --color \
  --dev-password \
  --name idplatform \
  --port 8443 \
  -p vcluster \
  -p kyverno \
  -p kyverno-policy-secret \
  -p cert-manager \
  -p kratix \
  -p kratix-gitstore-job

echo "Step 4: Register 2 new destination(s) for worker-1 and worker-2 on main cluster running kratix"
idpbuilder create \
  --color \
  --dev-password \
  --name idplatform \
  --port 8443 \
  -p vcluster \
  -p kyverno \
  -p kyverno-policy-secret \
  -p cert-manager \
  -p kratix \
  -p kratix-gitstore-job \
  -p kratix-new-destination

echo "Step 4: Install Argocd on each vcluster"
echo "TODO: Find a way to install argocd agent, remove non needed servers: dex, etx"
vcluster connect worker-1
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
vcluster disconnect

vcluster connect worker-2
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
vcluster disconnect

echo "Step 4: Register new agents for worker-1 and worker-2. Edit the kratix-new-agent.yaml file to change the name of the cluster"
echo "TODO: Use ApplicationSet instead of Application to configure x agents"
idpbuilder create \
  --color \
  --dev-password \
  --name idplatform \
  --port 8443 \
  -p vcluster \
  -p kyverno \
  -p kyverno-policy-secret \
  -p cert-manager \
  -p kratix \
  -p kratix-gitstore-job \
  -p kratix-new-destination \
  -p kratix-new-agent

echo "Step 5: Install a promises and deploy it on the 2 destinations OR only dev and not test"