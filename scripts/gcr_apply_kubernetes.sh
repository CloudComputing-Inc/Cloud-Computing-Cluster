# Applies Kubernetes configurations for your microservices
for file in kubernetes/*/*.yaml; do kubectl apply -f "$file"; done

# Apply Prometheus configurations
PROMETHEUS_DIR=~/cn-group03/prometheus

kubectl apply -f $PROMETHEUS_DIR/prometheus-config.yaml
kubectl apply -f $PROMETHEUS_DIR/prometheus-deployment.yaml
kubectl apply -f $PROMETHEUS_DIR/prometheus-service.yaml