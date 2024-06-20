# Applies Kubernetes configurations for microservices
for file in kubernetes/*/*.yaml; do kubectl apply -f "$file"; done

# Applies Prometheus configurations
for file in prometheus/*.yaml; do kubectl apply -f "$file"; done

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Ensure Prometheus and Pushgateway services are running
kubectl rollout status deployment/prometheus-deployment
kubectl rollout status deployment/pushgateway

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
