# Cloud Computing Project Group 03
[![GKE Deploy](https://github.com/CloudComputing-Inc/cn-group03/actions/workflows/google.yml/badge.svg)](https://github.com/CloudComputing-Inc/cn-group03/actions/workflows/google.yml)
## Members: 
- Beatriz Rosa 55313, José Ricardo Ribeiro 62761, Christopher Anaya 60566, Ayla Stehling 63327


# Running 
### Discussion
1. `chmod +x ~/cn-group03/scripts/*`
2. Delete cluster in GCP and GCR(Google Container Registry) and kubernetes allocated resources:

`./scripts/gcp_clean.sh`

3. Create service acc. and cluster and secrets:
   
`./scripts/cluster_create.sh`

`./scripts/gcp_configure.sh`

4. Build and push docker images

`./scripts/gcr_publish.sh`

5. Apply deployment configurations:

`./scripts/gcr_apply_kubernetes.sh`

6. Run tests:

`./scripts/test.sh`

-----------------------------------------------------
### Phase 4
1. Create new project in GCP called 'test-project-tp1'
2. Delete cluster in GCP and GCR(Google Container Registry) and kubernetes allocated resources:

`./scripts/gcp_clean.sh`

3. Open Google Cloud Shell in the project and run:

`./scripts/cluster_create.sh`

And then:

`./scripts/deploy.sh`

-----------------------------------------------------
### Phase 3
Install docker and run the script: \
`./scripts/run.sh` 

In case of permission denied, run:
`chmod +x ~/cn-group03/scripts/*`






# Roles
#Role | Role                                                  | Number  | Name            
 :--: |:----------------------------------------------------- | :------ |:---------------
1     | Microservices                                         | fc55313 | Beatriz Rosa     
2     | Data Science                                          | fc60566 | Christopher Anaya   
3     | DevOps                                                  | fc62761 | José Ricardo Ribeiro 
4     | TODO                                                  | fc63327 | Ayla Stehling

## Microservices
 | Name of microservice                                  | Number  | Responsible            
 |:----------------------------------------------------- | :------ |:---------------
 | API Gateway and Market-Analysis                       | fc55313 | Beatriz Rosa     
 | Sentiment Analysis                                    | fc60566 | Christopher Anaya   
 | Yelp Category Recommendation                          | fc62761 | José Ricardo Ribeiro 
 | Question-Analysis                                     | fc63327 | Ayla Stehling
