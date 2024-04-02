### BUILD IMAGES FOR MICROSERVICES

## API GATEWAY
printf "Building Docker for API Gateway . . .\n"
docker build -f ~/cn-group03/api/Dockerfile -t api_gateway ~/cn-group03/api/
printf "done\n"

## MARKET PERFORMANCE
printf "Building Docker for Market Performance . . .\n"
docker build -f ~/cn-group03/app/microservices/market-performance/Dockerfile -t market_performance ~/cn-group03/app/microservices/market-performance/
printf "done\n"

### Creating network
docker network create microservices || true # This will not fail if the network already exists

### RUNNING IMAGES

## API GATEWAY
printf "Running API Gateway . . .\n"
docker run -d --network microservices --name api_gateway_container -p 8000:8000 api_gateway
printf "done\n"

## MARKET PERFORMANCE
printf "Running Market Performance . . .\n"
docker run -d --network microservices --name market_performance_container -p 50053:50053 market_performance
printf "done\n"
