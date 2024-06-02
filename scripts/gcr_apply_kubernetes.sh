# Applies Kubernetes configurations for microservices
for file in kubernetes/*/*.yaml; do kubectl apply -f "$file"; done

# Apply Prometheus configurations
PROMETHEUS_DIR=~/cn-group03/prometheus

kubectl apply -f $PROMETHEUS_DIR/prometheus-config.yaml
kubectl apply -f $PROMETHEUS_DIR/prometheus-deployment.yaml
kubectl apply -f $PROMETHEUS_DIR/prometheus-service.yaml
kubectl apply -f $PROMETHEUS_DIR/grafana.yaml

# Apply Locust configuration
kubectl create configmap locust-scripts --from-file=kubernetes/locust/locust_marketAnalysis.py || kubectl create configmap locust-scripts --from-file=kubernetes/locust/locust_marketAnalysis.py --dry-run=client -o yaml | kubectl apply -f -
kubectl get configmap locust-scripts

# Fetch the external IP of nginx-gateway-svc
EXTERNAL_IP=""
while [ -z "$EXTERNAL_IP" ]; do
  echo "Waiting for external IP of nginx-gateway-svc..."
  EXTERNAL_IP=$(kubectl get svc nginx-gateway-svc -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  [ -z "$EXTERNAL_IP" ] && sleep 10
done

echo "External IP found: $EXTERNAL_IP"

# Path to the locust deployment yaml file
LOCUST_DEPLOYMENT_YAML="kubernetes/locust/locust-deployment.yaml"

# Update the locust-deployment.yaml with the fetched EXTERNAL_IP
sed -i "s|--host=http://PLACEHOLDER|--host=http://$EXTERNAL_IP|g" $LOCUST_DEPLOYMENT_YAML

echo "Updated locust-deployment.yaml with external IP: $EXTERNAL_IP"

# Apply the updated locust-deployment.yaml
kubectl apply -f $LOCUST_DEPLOYMENT_YAML
