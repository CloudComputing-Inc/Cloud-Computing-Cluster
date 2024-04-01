# See Setup before running
# Download Metadata files from https://cseweb.ucsd.edu/~jmcauley/datasets/amazon_v2/

import os
import json
import gzip
import certifi
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor, as_completed

# connect to MongoDB, change the user and passwordX  to reflect your own clusters  connection strings
user = "br"
password0 = "e3wmnqdtsYSEwa3I"
up0 = user + ":" + password0

password2 = "C7Kv49l3cZcS5NDo"
up2 = user + ":" + password2

password3 = "qVEqmdKYmrZoNlFw"
up3 = user + ":" + password3

password4 = "B0yEjiRW3P71vCkQ"
up4 = user + ":" + password4 

# MongoDB clusters connection strings
clusters = {
    "cluster1": "mongodb+srv://" + up0 +"@cluster0.0zctiyc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "cluster2": "mongodb+srv://" + up2 +"@cluster0.ica6ojz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "cluster3": "mongodb+srv://" + up3 + "@cluster0.hv5qtwc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
     "cluster4":"mongodb+srv://" + up4 + "@cluster0.cymhfm5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
}

# Mapping of category files to clusters and document limits(small values for fast app dev small GCP storage limit)
category_tasks = {
    # "cluster1": [
    #     ("meta_Automotive.json.gz", 3000),
  
    #    ("../../data/meta_All_Beauty.json.gz", 2000),
    #     ("../../data/meta_AMAZON_FASHION.json.gz", 1500),
    #     ("../../data/meta_Arts_Crafts_and_Sewing.json.gz", 2000), 

    # ],
    "cluster2": [
        ("./meta_Books.json.gz", 3000),
        
        # ("../../data/meta_CDs_and_Vinyl.json.gz", 1500),
        # ("../../data/meta_Cell_Phones_and_Accessories.json.gz", 1500),
        # ("../../data/meta_Clothing_Shoes_and_Jewelry.json.gz", 2000),
        # ("../../data/meta_Digital_Music.json.gz", 1500), 

    ],
    
    # "cluster3": [
    #     ("../../data/meta_Electronics.json.gz", 3000),
    #     ("../../data/meta_Home_and_Kitchen.json.gz", 1500),
        
    #     ("../../data/meta_Movies_and_TV.json.gz", 1500),
    #     ("../../data/meta_Patio_Lawn_and_Garden.json.gz", 1500),
    #     ("../../data/meta_Pet_Supplies.json.gz", 1500),  


    # ],
    # "cluster4": [
    #     ("../../data/meta_Sports_and_Outdoors.json.gz", 3000),
       
    #     ("../../data/meta_Software.json.gz", 1500),
    #     ("../../data/meta_Tools_and_Home_Improvement.json.gz", 1500),
    #     ("../../data/meta_Toys_and_Games.json.gz", 1500),
    #     ("../../data/meta_Video_Games.json.gz", 1500), 
    # ]
}


def process_entry(entry):
    """Process and return the entry with only the required fields."""
    return {
        'title': entry.get('title'),
        'brand': entry.get('brand'),
        'price': entry.get('price'),
        'salesRank': entry.get('salesRank', {}),
        'categories': entry['categories'][0] if 'categories' in entry and entry['categories'] else [],
        'category': entry.get('category', ''),
        'rank': entry.get('rank', ''),
        'main_cat': entry.get('main_cat', '')
    }

def upload_document_to_cluster(document, cluster_uri):
    """Upload a single document to the specified MongoDB cluster."""
    client = MongoClient(cluster_uri, ssl=True, ssl_ca_certs=certifi.where())
    db = client['amazon_metadata']
    collection = db['metadata']
    processed_document = process_entry(document)
    collection.insert_one(processed_document)

def process_and_upload_documents(cluster_uri, category_files):
    """Process documents from given category files and upload to the specified cluster."""
    client = MongoClient(cluster_uri)
    db = client['amazon_metadata']
    collection = db['metadata']

    for category_file, limit in category_files:
        print(f"Processing {category_file} for {cluster_uri}")
        with gzip.open(category_file, 'rt') as f:
            count = 0
            for line in f:
                if count >= limit:
                    break
                document = json.loads(line)
                collection.insert_one(process_entry(document))
                count += 1
        print(f"Uploaded {count} documents from {category_file} to {cluster_uri}")

def clear_collections():
    """Clear collections in all clusters."""
    for cluster_uri in clusters.values():
        client = MongoClient(cluster_uri)
        db = client['amazon_metadata']
        db['metadata'].drop()
        print(f"Cleared collection for cluster {cluster_uri}")

def main():
    clear_collections()
    with ThreadPoolExecutor(max_workers=len(category_tasks)) as executor:
        futures = []
        for cluster_name, tasks in category_tasks.items():
            cluster_uri = clusters[cluster_name]
            # Passing the tasks, which already include the document limit
            futures.append(executor.submit(process_and_upload_documents, cluster_uri, tasks))
        for future in futures:
            future.result()
    print("Data distribution to clusters completed.")

if __name__ == "__main__":
    main()