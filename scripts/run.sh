chmod +x ~/cn-group03/scripts/*

#./gcp_clean.sh

./cluster_create.sh

./gcp_configure.sh

./gcr_publish.sh

./gcr_apply_kubernetes.sh

./test.sh