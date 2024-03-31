import json
import gzip
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import random

# MongoDB clusters connection strings
clusters = {
    "cluster1": "mongodb+srv://br:e3wmnqdtsYSEwa3I@cluster0.lgxmbkq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "cluster2": "mongodb+srv://br:C7Kv49l3cZcS5NDo@cluster0.edx1by0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "cluster3": "mongodb+srv://br:qVEqmdKYmrZoNlFw@cluster0.dfxji2z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "cluster4":"mongodb+srv://br:B0yEjiRW3P71vCkQ@cluster0.0ecyl89.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
}

# Mapping of category files to clusters and document limits
category_tasks = {
    "cluster1": [
        ("data/meta_Automotive.json.gz", 3000),
        ("data/meta_All_Beauty.json.gz", 2000),
        ("data/meta_AMAZON_FASHION.json.gz", 1500),
        ("data/meta_Arts_Crafts_and_Sewing.json.gz", 2000),
    ],
    "cluster2": [
        ("data/meta_Books.json.gz", 3000),
        ("data/meta_CDs_and_Vinyl.json.gz", 1500),
        ("data/meta_Cell_Phones_and_Accessories.json.gz", 1500),
        ("data/meta_Clothing_Shoes_and_Jewelry.json.gz", 2000),
        ("data/meta_Digital_Music.json.gz", 1500),
    ],
    # Add mappings for clusters 3 and 4 based on your specifications
    "cluster3": [
        ("data/meta_Electronics.json.gz", 3000),
        ("data/meta_Home_and_Kitchen.json.gz", 1500),
        ("data/meta_Movies_and_TV.json.gz", 1500),
        ("data/meta_Patio_Lawn_and_Garden.json.gz", 1500),
        ("data/meta_Pet_Supplies.json.gz", 1500),
    ],
    "cluster4": [
        ("data/meta_Sports_and_Outdoors.json.gz", 3000),
        ("data/meta_Software.json.gz", 1500),
        ("data/meta_Tools_and_Home_Improvement.json.gz", 1500),
        ("data/meta_Toys_and_Games.json.gz", 1500),
        ("data/meta_Video_Games.json.gz", 1500),
    ]
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
    client = MongoClient(cluster_uri)
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
            # Here you simply pass the tasks, which already include the document limit
            futures.append(executor.submit(process_and_upload_documents, cluster_uri, tasks))
        for future in futures:
            future.result()
    print("Data distribution to clusters completed.")

if __name__ == "__main__":
    main()