#!/bin/bash

# Start ZAP in daemon mode
zap.sh -daemon -config api.disablekey=true

# Allow ZAP to fully start
sleep 10

# Spider the target
zap-cli -p 8090 open-url http://nginx-gateway-svc
zap-cli -p 8090 spider http://nginx-gateway-svc

# Perform an active scan
zap-cli -p 8090 active-scan http://nginx-gateway-svc

# Generate the report
zap-cli -p 8090 report -o zap_report.html -f html

# Output the report
cat zap_report.html
