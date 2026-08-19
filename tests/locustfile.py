from locust import HttpUser, task, between


class LogiTrackLoadUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def test_health_endpoint(self):
        self.client.get("/health")

    @task(2)
    def test_root_endpoint(self):
        self.client.get("/")