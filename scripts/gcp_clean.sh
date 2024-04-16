kubectl delete configmaps --all
kubectl delete pvc --all
kubectl delete secrets --all
kubectl delete ingress --all
kubectl delete services --all
kubectl delete deployments --all

gcloud container images delete gcr.io/test-project-tp1/api-gateway --force-delete-tags
gcloud container images delete gcr.io/test-project-tp1/market-performance --force-delete-tags
#gcloud container clusters delete cluster-amazon-data --zone europe-west4-a