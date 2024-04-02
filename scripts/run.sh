## Populating databases and preprocessing data........
printf "Populating databases and preprocessing data"
#cd ~/cn-group03/app/data/Amazon_metadata/
#python metadata_clusters.py

## Creating Protobuf python files..........
printf "Creating Protobuf python files"
cd ~/cn-group03/scripts
chmod +x ~/cn-group03/scripts/proto_create.sh
./proto_create.sh

## Building and Running docker containers........
printf "Building and Running docker containers"
docker-compose up --build