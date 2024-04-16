export PROJECT_ID=$(gcloud info --format='value(config.project)')
cd ~/cn-group03

# scripts to build proto dependencies.
chmod +x ~/cn-group03/scripts/proto_requirements.sh
./scripts/proto_requirements.sh

chmod +x ~/cn-group03/scripts/proto_create.sh
./scripts/proto_create.sh

cd api/
# Navigate to the directory containing Dockerfiles and build  images
# This assumes that each microservice has a corresponding Dockerfile in its directory
docker build -t gcr.io/${PROJECT_ID}/api-gateway .
cd ~/cn-group03/app/microservices/market-performance
docker build -t gcr.io/${PROJECT_ID}/market-performance .
# etc. for all  microservices

docker images
gcloud services enable containerregistry.googleapis.com
gcloud auth configure-docker


# Push the images to GCR
docker push gcr.io/${PROJECT_ID}/api-gateway
docker push gcr.io/${PROJECT_ID}/market-performance

# etc. for all  microservices

docker images
gcloud container images list
kubectl get nodes


# Get credentials for kubectl
gcloud container clusters get-credentials cluster-amazon-data --zone europe-west4-a
cd ../../..
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
# Apply the deployment configuration
kubectl apply -f ~/cn-group03/kubernetes/deploy.yaml

# Get the cluster name and its related tags and network for firewall rule.
CLUSTER_NAME=$(gcloud container clusters list --format="value(name)" --filter="zone:(europe-west4-a)")
TAG_NAME=$(gcloud compute instances list --filter="name~'^gke-$CLUSTER_NAME'" --format="value(tags.items[0])" --limit=1)
NETWORK_NAME=$(gcloud container clusters describe $CLUSTER_NAME --zone europe-west4-a --format="value(network)")

# Create a firewall rule if it doesn't exist.
FIREWALL_RULE_NAME="allow-nodeport-access"

if ! gcloud compute firewall-rules describe $FIREWALL_RULE_NAME &>/dev/null; then
  gcloud compute firewall-rules create $FIREWALL_RULE_NAME \
    --direction=INGRESS \
    --priority=1000 \
    --network=$NETWORK_NAME \
    --action=ALLOW \
    --rules=tcp:30000 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=$TAG_NAME
fi
