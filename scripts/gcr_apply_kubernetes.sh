# Applies Kubernetes configurations for your microservices
for file in kubernetes/*/*.yaml; do kubectl apply -f "$file"; done

# Apply Prometheus configurations
PROMETHEUS_DIR=~/cn-group03/prometheus

kubectl apply -f $PROMETHEUS_DIR/prometheus-config.yaml
kubectl apply -f $PROMETHEUS_DIR/prometheus-deployment.yaml
kubectl apply -f $PROMETHEUS_DIR/prometheus-service.yaml
kubectl apply -f $PROMETHEUS_DIR/grafana.yaml

# Apply Locust configuration
kubectl create configmap locust-scripts --from-file=kubernetes/locust/locust_marketAnalysis.py
kubectl get configmap locust-scripts
kubectl apply -f kubernetes/locust/locust-deployment.yaml
