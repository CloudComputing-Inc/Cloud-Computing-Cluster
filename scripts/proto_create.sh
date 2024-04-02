### MARKET-PERFORMANCE PROTOBUFS
python -m venv venv
source venv/bin/activate
cd ~/cn-group03/app/microservices/market-performance
python -m pip install -r requirements.txt
cd ~/cn-group03/app/microservices
python -m grpc_tools.protoc -I./market-performance --python_out=./market-performance --grpc_python_out=./market-performance market-performance/market-performance.proto
deactivate

