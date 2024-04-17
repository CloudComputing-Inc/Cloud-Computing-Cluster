### MARKET-PERFORMANCE PROTOBUFS
python -m venv venv
source venv/bin/activate
cd ~/cn-group03/app/microservices/market-performance
python -m pip install -r requirements.txt
cd ~/cn-group03/app/microservices
python -m grpc_tools.protoc -I./market-performance --python_out=./market-performance --grpc_python_out=./market-performance market-performance/market-performance.proto
deactivate

### QUESTION_ANALYSIS PROTOBUFS
python -m venv venv
source venv/bin/activate
cd ~/cn-group03/app/microservices/question-analysis
python -m pip install -r requirements.txt
cd ~/cn-group03/app/microservices
python -m grpc_tools.protoc -I./question-analysis --python_out=./question-analysis --grpc_python_out=./question-analysis question-analysis/question-analysis.proto
deactivate