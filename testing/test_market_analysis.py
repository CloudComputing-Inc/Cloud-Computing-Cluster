import requests

BASE_URL = "http://35.204.117.9"

def test_get_categories():
    response = requests.get(f"{BASE_URL}/market/categories")
    assert response.status_code == 200
    assert response.json()  

def test_get_metadata():
    response = requests.get(f"{BASE_URL}/market/metadata?category=Books&minPrice=2&maxPrice=50")
    assert response.status_code == 200
    assert response.json()  

def test_get_top_brand():
    response = requests.get(f"{BASE_URL}/market/top-brand?category=Software")
    assert response.status_code == 200
    assert response.json()  

def test_get_top_products():
    response = requests.get(f"{BASE_URL}/market/top-products?category=Books")
    assert response.status_code == 200
    assert response.json()  

# Error scenarios
def test_get_metadata_missing_category():
    response = requests.get(f"{BASE_URL}/market/metadata?minPrice=2&maxPrice=50")
    assert response.status_code == 400
    assert "error" in response.json()

def test_get_metadata_invalid_price():
    response = requests.get(f"{BASE_URL}/market/metadata?category=Books&minPrice=invalid&maxPrice=50")
    assert response.status_code == 400  # Invalid price format
    assert "error" in response.json()

def test_get_top_brand_missing_category():
    response = requests.get(f"{BASE_URL}/market/top-brand")
    assert response.status_code == 500
    #assert response.json().get("error") == "Category not handled by any cluster"

def test_get_top_brand_invalid_category():
    response = requests.get(f"{BASE_URL}/market/top-brand?category=InvalidCategory")
    assert response.status_code == 500
    #assert response.json().get("error") == "Category not handled by any cluster"

def test_get_top_products_missing_category():
    response = requests.get(f"{BASE_URL}/market/top-products")
    assert response.status_code == 500
    #assert response.json().get("error") == "Category not handled by any cluster"

def test_get_top_products_invalid_category():
    response = requests.get(f"{BASE_URL}/market/top-products?category=InvalidCategory")
    assert response.status_code == 500
    #assert response.json().get("error") == "Category not handled by any cluster"

# def test_metrics_endpoint():
#     response = requests.get(f"{BASE_URL}/metrics")
#     assert response.status_code == 200
#     assert "cpu_usage" in response.text
#     assert "memory_usage" in response.text

