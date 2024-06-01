# ## Populating databases and preprocessing data........
# printf "Populating databases and preprocessing data..................\n"
# #cd ~/cn-group03/app/data/Amazon_metadata/
# #python metadata_clusters.py
# ## Creating Protobuf python files..........
# printf "Creating Protobuf python files.............................\n"
# cd ~/cn-group03/scripts
# chmod +x ~/cn-group03/scripts/proto_create.sh
# ./proto_create.sh
# ## Building and Running docker containers........
# printf "Building and Running docker containers..........................\n"
# docker-compose up --build

chmod +x ~/cn-group03/scripts/*

#./scripts/gcp_clean.sh

./scripts/cluster_create.sh

./scripts/gcp_configure.sh

./scripts/gcr_publish.sh

./scripts/gcr_apply_kubernetes.sh

./scripts/test.sh