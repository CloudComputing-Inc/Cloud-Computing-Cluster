DELETE CLUSTER:
gcloud container clusters delete cluster-amazon-data --zone europe-west4-a

DELETE Persistent Disks:
gcloud compute disks list
gcloud compute disks delete [DISK_NAME] --zone [ZONE]

DELETE Network Services:
gcloud compute forwarding-rules list
gcloud compute forwarding-rules delete [NAME] --region [REGION]
gcloud compute target-pools delete [NAME] --region [REGION]

CLEAN CONTAINER Registry:
gcloud container images list
gcloud container images delete [IMAGE_NAME] --force-delete-tags

CLEAN Cloud Storage:
gsutil ls
gsutil rm -r gs://[BUCKET_NAME]

DELETE static IPS:
gcloud compute addresses list
gcloud compute addresses delete [ADDRESS_NAME] --region [REGION]
