# Cloud Computing Project Group 03
## Members: 
- Beatriz Rosa 55313, José Ricardo Ribeiro 62761, Christopher Anaya 60566, Ayla Stehling 63327

## Setup MongoDB Atlas Clusters:

1. Create 4 MongoDB Atlas Clusters M0 Free Tier without loading the sample data into them.
2. Get the username and password of each cluster and change class metadata_clusters.py user and passwordX values.
3. Check IP address from cloud shell in (c:\Users\xxxx\.ssh\config)
4. For each cluster : Add that IP in Security > Network Access > Add IP Address 
5. You can test fast if you are connected to a cluster by running test.py class.

# Running (provisory)
$ cd app/data/Amazon_metadata
$ python metadata_clusters.py
$ cd ~/cn-group03
$ python app.py