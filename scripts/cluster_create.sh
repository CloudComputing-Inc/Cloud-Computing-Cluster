gcloud services enable cloudapis.googleapis.com container.googleapis.com containerregistry.googleapis.com
kubectl get nodes 
# Creating a cluster with 3 nodes and e2-medium machine type
gcloud container clusters create cluster-amazon-data \
    --zone=europe-west4-a \
    --cluster-version=latest \
    --num-nodes=3 \
    --machine-type=e2-medium \
    --enable-autorepair \
    --scopes=service-control,service-management,compute-rw,storage-ro,cloud-platform,logging-write,monitoring-write
gcloud container clusters get-credentials cluster-amazon-data --zone europe-west4-a
kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=$(gcloud config get-value core/account)
cd ~/cn-group03
# create the necessary Kubernetes secrets
kubectl create secret tls amazon-data --cert tls.crt --key tls.key


