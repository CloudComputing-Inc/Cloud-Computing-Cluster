

cd ~/cn-group03/testing
pip install -r requirements.txt
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


### Security Tests
#!/bin/bash

# Check if Bandit is installed
if ! command -v bandit &> /dev/null; then
    echo "Bandit could not be found. Please install it using 'pip install bandit'."
    exit 1
fi

# Run Bandit on the market-analysis project
echo "Running Bandit for static code analysis..."
bandit -r ../app/microservices/market-analysis/ -f html -o bandit_report.html

# Output the report
if [ -f bandit_report.html ]; then
    echo "Bandit report generated: bandit_report.html"
    cat bandit_report.html
else
    echo "Failed to generate Bandit report."
    exit 1
fi


