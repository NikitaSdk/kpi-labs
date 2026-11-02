from fastapi import FastAPI
import requests
from consul import Consul
import socket
import time

app = FastAPI()

consul = Consul(host="consul", port=8500)
STATS_URL = None

def discover_service(service_name, retries=10, delay=2):
    for attempt in range(retries):
        try:
            services = consul.agent.services()
            for svc in services.values():
                if svc["Service"] == service_name:
                    return f"http://{svc['Address']}:{svc['Port']}"
        except:
            pass
        time.sleep(delay)
    raise Exception("Service not found")


@app.on_event("startup")
def register_service():
    global STATS_URL
    service_name = "reporting-service"

    consul.agent.service.register(
        name=service_name,
        service_id=f"{service_name}-{socket.gethostname()}",
        address=service_name,
        port=8000
    )

    STATS_URL = discover_service("stats-service")
    print("REPORT connected to:", STATS_URL)


@app.get("/report/{user_id}")
def generate_report(user_id: int):
    stats = requests.get(f"{STATS_URL}/stats/{user_id}").json()

    total_minutes = stats.get("total_minutes", 0)
    trainings = stats.get("trainings", [])

    # total calories burned
    total_calories = sum(t["calories"] for t in trainings)

    return {
        "user_id": user_id,
        "total_minutes": total_minutes,
        "total_calories": total_calories,
        "trainings_count": len(trainings),
        "report": f"User trained for {total_minutes} minutes and burned {total_calories} calories in total.",
        "status": "report_generated"
    }
