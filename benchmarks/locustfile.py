from locust import HttpUser, task, between


class LogiTrackUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # 1. Registrar usuario temporal para la simulación
        self.client.post("/api/v1/auth/register", json={
            "name": "Locust User",
            "email": "locust_runner@logitrack.com",
            "password": "LocustPassword123"
        })

        # 2. Login y almacenamiento del token
        response = self.client.post("/api/v1/auth/login", data={
            "username": "locust_runner@logitrack.com",
            "password": "LocustPassword123"
        })
        if response.status_code == 200:
            token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {token}"}
        else:
            self.headers = {}

    @task(3)
    def get_shipments(self):
        # Consulta frecuente de envíos
        self.client.get("/api/v1/shipments/", headers=self.headers)

    @task(1)
    def get_vehicles(self):
        # Consulta de vehículos
        self.client.get("/api/v1/vehicles/", headers=self.headers)