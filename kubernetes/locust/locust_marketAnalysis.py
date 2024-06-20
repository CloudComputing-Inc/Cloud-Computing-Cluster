from locust import HttpUser, TaskSet, task, between

class MarketAnalysisTasks(TaskSet):
    @task(4)
    def get_categories(self):
        self.client.get("/market/categories")

    @task(4)
    def get_metadata(self):
        self.client.get("/market/metadata?category=Books&minPrice=2&maxPrice=50")

    @task(1)
    def get_top_brand(self):
        self.client.get("/market/top-brand?category=Software")

    @task(2)
    def get_top_products(self):
        self.client.get("/market/top-products?category=Books")

class YelpTasks(TaskSet):
    @task(3)
    def list_businesses(self):
        self.client.get("/yelp/businesses?page=1&limit=20")

    @task(3)
    def get_top_rated_businesses(self):
        self.client.get("/yelp/businesses/top-rated?city=San Francisco&state=CA&limit=10")

    @task(2)
    def get_business(self):
        self.client.get("/yelp/businesses?page=2&limit=50")

    @task(1)
    def list_cities(self):
        self.client.get("/yelp/cities")

    @task(1)
    def list_states(self):
        self.client.get("/yelp/states")

class MarketAnalysisUser(HttpUser):
    tasks = [MarketAnalysisTasks, YelpTasks]
    wait_time = between(1, 5)
