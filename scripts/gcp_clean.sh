gcloud container images delete gcr.io/test-project-tp1/api-gateway --force-delete-tags
gcloud container images delete gcr.io/test-project-tp1/market-performance --force-delete-tags
kubectl delete svc api-gateway-service
gcloud container clusters delete cluster-amazon-data --zone europe-west4-a