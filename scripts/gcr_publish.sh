docker build -t yelp_reviews ./app/microservices/yelp-reviews
docker tag yelp_reviews gcr.io/cloudcomputinginc/yelp_reviews:latest

docker build -t market_analysis ./app/microservices/market-analysis
docker tag market_analysis gcr.io/cloudcomputinginc/market_analysis:latest

docker build -t question_analysis ./app/microservices/question-analysis
docker tag question_analysis gcr.io/cloudcomputinginc/question_analysis:latest

docker build -t api_gateway ./api
docker tag api_gateway gcr.io/cloudcomputinginc/api_gateway:latest


gcloud auth configure-docker
docker push gcr.io/cloudcomputinginc/yelp_reviews:latest
docker push gcr.io/cloudcomputinginc/market_analysis:latest

docker push gcr.io/cloudcomputinginc/question_analysis:latest
docker push gcr.io/cloudcomputinginc/api_gateway:latest


