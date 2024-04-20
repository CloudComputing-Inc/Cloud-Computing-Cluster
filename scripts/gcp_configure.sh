gcloud iam service-accounts create gcloud-project-acc --description="Account for local deployment of k8s" --display-name="Local Account"
gcloud iam service-accounts list
gcloud iam service-accounts keys create ./gcr.json --iam-account gcloud-project-acc@cloudcomputinginc.iam.gserviceaccount.com
kubectl create secret docker-registry gcr-io --docker-server=gcr.io --docker-username=_json_key --docker-password="$(cat ./gcr.json)" --docker-email=any@valid.email
kubectl get secrets