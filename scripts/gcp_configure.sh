#!/bin/bash

##########################################
# Already done once, no need to run again#
##########################################
gcloud iam service-accounts create gcloud-project-acc \
    --description="Account for local deployment of k8s" \
    --display-name="Local Account"

gcloud projects add-iam-policy-binding cloudcomputinginc \
    --member=serviceAccount:gcloud-project-acc@cloudcomputinginc.iam.gserviceaccount.com \
    --role=roles/artifactregistry.admin

gcloud iam service-accounts list

# If the key creation fails, delete the existing service account key and recreate it
if ! gcloud iam service-accounts keys create ./gcr.json --iam-account gcloud-project-acc@cloudcomputinginc.iam.gserviceaccount.com; then
    echo "Failed to create service account key. Deleting existing keys and trying again..."
    EXISTING_KEYS=$(gcloud iam service-accounts keys list --iam-account=gcloud-project-acc@cloudcomputinginc.iam.gserviceaccount.com --format="value(name)")
    for key in $EXISTING_KEYS; do
        gcloud iam service-accounts keys delete "$key" --iam-account=gcloud-project-acc@cloudcomputinginc.iam.gserviceaccount.com --quiet
    done
    gcloud iam service-accounts keys create ./gcr.json --iam-account gcloud-project-acc@cloudcomputinginc.iam.gserviceaccount.com
fi

################################################################################
# From here, we can use the gcr.json file to authenticate with the GCP registry#
################################################################################

# Ensure the Docker registry secret is created
kubectl create secret docker-registry gcr-io \
  --docker-server=https://gcr.io \
  --docker-username=_json_key \
  --docker-password="$(cat ./gcr.json)" \
  --docker-email=your-email@example.com

# Link the Docker registry secret to the default service account
kubectl patch serviceaccount default \
  -p '{"imagePullSecrets": [{"name": "gcr-io"}]}'

kubectl get secrets

