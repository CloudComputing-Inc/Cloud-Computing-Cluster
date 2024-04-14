gcloud services enable cloudapis.googleapis.com container.googleapis.com containerregistry.googleapis.com
kubectl get nodes 
# Creating a cluster with the smallest machine type and only 1 node to minimize costs
gcloud container clusters create cluster-amazon_data \
    --zone=europe-west4-a \
    --cluster-version=latest \
    --num-nodes=1 \
    --machine-type=e2-micro \
    --enable-autorepair \
    --scopes=service-control,service-management,compute-rw,storage-ro,cloud-platform,logging-write,monitoring-write
gcloud container clusters get-credentials cluster-amazon_data --zone europe-west4-a
kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=$(gcloud config get-value core/account)
cd ~/cn-group03
# create the necessary Kubernetes secrets
kubectl create secret tls amazon_data --cert scripts/fullchain1.pem --key scripts/privkey1.pem


