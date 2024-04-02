## Populating databases and preprocessing data........
#cd ~/cn-group03/app/data/Amazon_metadata/
#python metadata_clusters.py

## Creating Protobuf python files..........
cd ~/cn-group03/scripts
chmod +x ~/cn-group03/scripts/proto_create.sh
./proto_create.sh

#cd ~/cn-group03/api/
#python app.py

## Building and Running docker containers........
docker-compose up --build