from fastapi import FastAPI
from consul import Consul
import socket

app = FastAPI()

@app.on_event("startup")
def register_service():
    consul = Consul(host="consul", port=8500)
    service_name = "access-service"
    service_port = 8000
    service_id = f"{service_name}-{socket.gethostname()}"
    
    consul.agent.service.register(
        name=service_name,
        service_id=service_id,
        address=service_name,
        port=service_port
    )
    print(f"{service_name} registered in Consul")


users = {}
next_id = 1


@app.post("/users/register")
def register(data: dict):
    global next_id
    username = data.get("username")
    password = data.get("password")

    if username in users:
        return {"status": "error", "message": "User already exists"}

    users[username] = {"id": next_id, "password": password}
    user_id = next_id
    next_id += 1

    return {"status": "ok", "user_id": user_id}
