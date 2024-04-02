cd ~/cn-group03/app/data/Amazon_metadata/
python metadata_clusters.py

cd ~/cn-group03/scripts
chmod +x ~/cn-group03/scripts/proto_create.sh
./proto_create.sh

cd ~/cn-group03/api/
python app.py