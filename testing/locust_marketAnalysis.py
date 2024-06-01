from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task(1)
    def get_categories(self):
        self.client.get("/market/categories")

    @task(2)
    def get_metadata(self):
        self.client.get("/market/metadata?category=Books&minPrice=2&maxPrice=50")
    
    @task(3)
    def get_top_brand(self):
        self.client.get("/market/top-brand?category=Software")
    @task(4)
    def get_top_products(self):
        self.client.get("/market/top-products?category=Books")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 6)
