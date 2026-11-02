from fastapi import FastAPI, HTTPException
import json
import requests
from consul import Consul
import socket
import time

import sqlite3
from datetime import datetime
import threading

import pika

app = FastAPI()


consul = Consul(host="consul", port=8500)
STATS_URL = None

CALORIES_PER_MIN = {
    "running": 10,
    "cycling": 7,
    "swimming": 12,
    "fitness": 8,
}

DB_PATH = "outbox.db"



def discover_service(service_name, retries=20, delay=2):
    for attempt in range(retries):
        try:
            services = consul.agent.services()

            for svc in services.values():
                if svc["Service"] == service_name:
                    url = f"http://{svc['Address']}:{svc['Port']}"
                    print(f"[DISCOVERY] Found {service_name} at {url}")
                    return url

        except Exception as e:
            print(f"[DISCOVERY] Error: {e}")

        print(f"[DISCOVERY] {service_name} not found, retry {attempt+1}/{retries}")
        time.sleep(delay)

    raise Exception(f"{service_name} not found in Consul")



def init_outbox_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS outbox (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'NEW',
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()
    print("[OUTBOX] Initialized")


def save_outbox_event(event_type: str, payload: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO outbox (event_type, payload, status, created_at)
        VALUES (?, ?, 'NEW', ?)
        """,
        (event_type, json.dumps(payload), datetime.utcnow().isoformat()),
    )

    conn.commit()
    conn.close()
    print("[OUTBOX] Saved:", event_type, payload)



def outbox_dispatcher():
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute("SELECT id, event_type, payload FROM outbox WHERE status='NEW'")
            events = cur.fetchall()

            if events:
                print(f"[OUTBOX] Found {len(events)} NEW events")

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    credentials=pika.PlainCredentials("admin", "admin"),
                )
            )
            channel = connection.channel()


            channel.exchange_declare("training_dlx", "direct", durable=True)
            channel.queue_declare("training_events_dlq", durable=True)
            channel.queue_bind(
                exchange="training_dlx",
                queue="training_events_dlq",
                routing_key="training_events_dlq",
            )

            args = {
                "x-dead-letter-exchange": "training_dlx",
                "x-dead-letter-routing-key": "training_events_dlq",
            }
            channel.queue_declare(
                queue="training_events",
                durable=True,
                arguments=args,
            )

            for event_id, event_type, payload in events:
                data = json.loads(payload)

                channel.basic_publish(
                    exchange="",
                    routing_key="training_events",
                    body=json.dumps(data),
                    properties=pika.BasicProperties(delivery_mode=2),
                )

                cur.execute("UPDATE outbox SET status='SENT' WHERE id=?", (event_id,))
                print(f"[OUTBOX] Event {event_id} sent")

            conn.commit()
            conn.close()
            connection.close()

        except Exception as e:
            print("[OUTBOX] ERROR:", e)

        time.sleep(3)



def dlq_consumer():
    global STATS_URL

    while True:
        try:
            if STATS_URL is None:
                print("[SAGA] Waiting for STATS_URL...")
                time.sleep(2)
                continue

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    credentials=pika.PlainCredentials("admin", "admin"),
                )
            )
            channel = connection.channel()

            channel.queue_declare("training_events_dlq", durable=True)

            def callback(ch, method, properties, body):
                data = json.loads(body)
                print("[SAGA] Received DLQ event:", data)

                try:
                    resp = requests.post(
                        f"{STATS_URL}/stats/compensate",
                        json=data,
                        timeout=5,
                    )
                    print("[SAGA] Compensation:", resp.status_code)
                except Exception as e:
                    print("[SAGA] Compensation error:", e)
                    ch.basic_nack(method.delivery_tag, requeue=True)
                    return

                ch.basic_ack(method.delivery_tag)

            channel.basic_consume("training_events_dlq", callback)
            print("[SAGA] DLQ consumer started")
            channel.start_consuming()

        except Exception as e:
            print("[SAGA] ERROR:", e)
            time.sleep(5)



@app.on_event("startup")
def startup():
    global STATS_URL

    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)

    consul.agent.service.register(
        name="training-service",
        service_id=f"training-{hostname}",
        address=host_ip,
        port=8000,
    )
    print("[CONSUL] Registered training-service at", host_ip)

    time.sleep(2)

    STATS_URL = discover_service("stats-service")

    init_outbox_db()

    threading.Thread(target=outbox_dispatcher, daemon=True).start()
    threading.Thread(target=dlq_consumer, daemon=True).start()



@app.post("/training")
def create_training(data: dict):
    if STATS_URL is None:
        raise HTTPException(503, "stats-service not found")

    user_id = data["user_id"]
    activity = data["activity"]
    duration = data["duration"]

    calories = CALORIES_PER_MIN.get(activity, 0) * duration

    sync_resp = requests.post(
        f"{STATS_URL}/stats/update",
        json={
            "user_id": user_id,
            "activity": activity,
            "duration": duration,
            "calories": calories,
        },
    )

    save_outbox_event(
        "training_created",
        {
            "user_id": user_id,
            "activity": activity,
            "duration": duration,
            "calories": calories,
        },
    )

    return {
        "status": "ok",
        "sync_result": sync_resp.json(),
        "async": "saved_to_outbox",
    }
