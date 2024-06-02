cd ~/cn-group03/testing

### Unit tests

#!/bin/bash
# Fetch the external IP of the nginx-gateway-svc
EXTERNAL_IP=""
while [ -z "$EXTERNAL_IP" ]; do
  echo "Waiting for external IP of nginx-gateway-svc..."
  EXTERNAL_IP=$(kubectl get svc nginx-gateway-svc -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  [ -z "$EXTERNAL_IP" ] && sleep 10
done

echo "External IP found: $EXTERNAL_IP"

# Update the test file with the fetched EXTERNAL_IP
TEST_FILE="test_market_analysis.py"
sed -i "s|BASE_URL = .*|BASE_URL = \"http://$EXTERNAL_IP\"|g" $TEST_FILE
echo "Updated $TEST_FILE with BASE_URL: http://$EXTERNAL_IP"
# Run the tests
pytest $TEST_FILE



### Acceptance Tests



### Security



### Reliability
