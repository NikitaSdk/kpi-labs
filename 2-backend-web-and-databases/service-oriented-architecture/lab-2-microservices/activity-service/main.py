from fastapi import FastAPI
from consul import Consul
import socket

app = FastAPI()

@app.on_event("startup")
def register_service():
    consul = Consul(host="consul", port=8500)
    service_name = "activity-service"
    service_port = 8000
    service_id = f"{service_name}-{socket.gethostname()}"
    
    consul.agent.service.register(
        name=service_name,
        service_id=service_id,
        address=service_name,  # Docker DNS
        port=service_port
    )
    print(f"{service_name} registered in Consul")

activities = [
    {"name": "running", "calories_per_min": 10},
    {"name": "cycling", "calories_per_min": 7},
    {"name": "swimming", "calories_per_min": 12},
    {"name": "fitness", "calories_per_min": 8},
]


@app.get("/activities")
def get_activities():
    return {"available_activities": activities}
