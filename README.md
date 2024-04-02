# Cloud Computing Project Group 03
## Members: 
- Beatriz Rosa 55313, José Ricardo Ribeiro 62761, Christopher Anaya 60566, Ayla Stehling 63327


# Running (provisory)
$ cd ~/cn-group03/scripts
$ ./run.sh


## Market Performance Service with GRPC example:

### Server:
$ python -m venv venv

$ source venv/bin/activate

(venv) $ cd ~/cn-group03/app/microservices/market-performance

(venv) $ python -m pip install -r requirements.txt

$ python market-performance.py


### Client:
$ cd ~/cn-group03/app/microservices/market-performance

$ python

>>> import grpc

>>> from market_performance_pb2 import GetMainCategoriesRequest

>>> import market_performance_pb2_grpc

>>> channel= grpc.insecure_channel('localhost:50051')

>>> client=market_performance_pb2_grpc.MarketPerformanceServiceStub(channel)

>>> request= GetMainCategoriesRequest()

>>> client.GetMainCategories(request)
