export PROJECT_ID=$(gcloud info --format='value(config.project)')
cd ~/cn-group03

# scripts to build proto dependencies.
./scripts/1_proto_dependencies.sh
./scripts/2_proto_create.sh

cd api/
# Navigate to the directory containing Dockerfiles and build  images
# This assumes that each microservice has a corresponding Dockerfile in its directory
docker build -t gcr.io/${PROJECT_ID}/api-gateway .
cd ~/cn-group03/app/microservices/market-performance
docker build -t gcr.io/${PROJECT_ID}/market-performance .
# etc. for all your microservices

docker images
gcloud services enable containerregistry.googleapis.com
gcloud auth configure-docker


# Push the images to GCR
docker push gcr.io/${PROJECT_ID}/api-gateway
docker push gcr.io/${PROJECT_ID}/market-performance

# etc. for all your microservices


docker images
gcloud container images list
kubectl get nodes
# Get credentials for kubectl
gcloud container clusters get-credentials cluster-amazon_data --zone europe-west4-a
cd ../../..
# Apply the deployment configuration
kubectl apply -f deployment.yaml
