from fastapi import FastAPI, HTTPException
import requests
from consul import Consul
import time
import threading

app = FastAPI()

consul = Consul(host="consul", port=8500)


SERVICE_URLS = {
    "access-service": None,
    "activity-service": None,
    "training-service": None,
    "stats-service": None,
    "reporting-service": None,
}

def discover_service_blocking(service_name):
    print(f"[GATEWAY] Waiting for {service_name}...")

    while SERVICE_URLS[service_name] is None:
        try:
            services = consul.agent.services()
            for svc in services.values():
                if svc["Service"] == service_name:
                    url = f"http://{svc['Address']}:{svc['Port']}"
                    SERVICE_URLS[service_name] = url
                    print(f"[GATEWAY] Discovered {service_name}: {url}")
                    return
        except Exception as e:
            print(f"[GATEWAY] Discovery error for {service_name}: {e}")

        time.sleep(2)


def background_discovery():

    for svc in SERVICE_URLS.keys():
        threading.Thread(
            target=discover_service_blocking,
            args=(svc,),
            daemon=True
        ).start()



@app.on_event("startup")
def startup_event():
    print("[GATEWAY] Startup OK, launching background discovery threads...")
    background_discovery()



def get_service_url(name: str):
    url = SERVICE_URLS[name]
    if url is None:
        raise HTTPException(503, detail=f"{name} is not yet available")
    return url




@app.post("/api/register")
def register(username: str, password: str):
    url = get_service_url("access-service")
    resp = requests.post(f"{url}/users/register", json={
        "username": username,
        "password": password
    })
    return resp.json()


@app.get("/api/activities")
def get_categories():
    url = get_service_url("activity-service")
    resp = requests.get(f"{url}/activities")
    return resp.json()


@app.post("/api/training")
def create_training(user_id: int, activity: str, duration: int):
    url = get_service_url("training-service")
    resp = requests.post(f"{url}/training", json={
        "user_id": user_id,
        "activity": activity,
        "duration": duration
    })
    return resp.json()


@app.get("/api/stats/{user_id}")
def get_stats(user_id: int):
    url = get_service_url("stats-service")
    resp = requests.get(f"{url}/stats/{user_id}")
    return resp.json()


@app.get("/api/report/{user_id}")
def get_report(user_id: int):
    url = get_service_url("reporting-service")
    resp = requests.get(f"{url}/report/{user_id}")
    return resp.json()
