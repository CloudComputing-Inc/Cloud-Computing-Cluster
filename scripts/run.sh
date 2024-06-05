chmod +x ~/cn-group03/scripts/*

#./scripts/gcp_clean.sh

./scripts/cluster_create.sh

./scripts/gcp_configure.sh

./scripts/gcr_publish.sh

./scripts/gcr_apply_kubernetes.sh

./scripts/test.sh