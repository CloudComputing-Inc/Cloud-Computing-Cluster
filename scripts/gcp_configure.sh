##########################################
# Already done once, no need to run again#
##########################################
gcloud iam service-accounts create gcloud-project-acc \
    --description="Account for local deployment of k8s" \
    --display-name="Local Account" \
gcloud projects add-iam-policy-binding cloudcomputinginc    --member=serviceAccount:gcloud-project-acc@cloudcomputinginc.iam.gserviceaccount.co
m    --role=roles/artifactregistry.admin
gcloud iam service-accounts list
gcloud iam service-accounts keys create ./gcr.json --iam-account gcloud-project-acc@cloudcomputinginc.iam.gserviceaccount.com
################################################################################
# From here, we can use the gcr.json file to authenticate with the GCP registry#
################################################################################
kubectl create secret docker-registry gcr-io --docker-server=gcr.io --docker-username=_json_key --docker-password="$(cat ./gcr.json)" --docker-email=any@example.com
kubectl get secrets