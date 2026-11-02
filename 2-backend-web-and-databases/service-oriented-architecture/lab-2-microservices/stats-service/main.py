from fastapi import FastAPI
from consul import Consul
import socket
import pika
import json
import threading
import time

app = FastAPI()


stats = {}
trainings = {}
event_log = []


@app.on_event("startup")
def register_service():
    consul = Consul(host="consul", port=8500)
    service_name = "stats-service"
    service_port = 8000
    service_id = f"{service_name}-{socket.gethostname()}"

    consul.agent.service.register(
        name=service_name,
        service_id=service_id,
        address=service_name,
        port=service_port,
    )
    print("Stats-service registered in Consul")

    thread = threading.Thread(target=rabbitmq_consumer, daemon=True)
    thread.start()
    print("Stats-service consumer started")



@app.post("/stats/update")
def update_stats(data: dict):

    user_id = data["user_id"]
    activity = data["activity"]
    duration = data["duration"]
    calories = data["calories"]

    stats[user_id] = stats.get(user_id, 0) + duration

    if user_id not in trainings:
        trainings[user_id] = []

    trainings[user_id].append(
        {
            "activity": activity,
            "duration": duration,
            "calories": calories,
        }
    )

    return {"status": "ok", "total_minutes": stats[user_id]}


@app.get("/stats/{user_id}")
def get_stats(user_id: int):
    return {
        "user_id": user_id,
        "total_minutes": stats.get(user_id, 0),
        "trainings": trainings.get(user_id, []),
    }


@app.get("/stats/events")
def get_events():
    return {"async_events": event_log}


@app.post("/stats/compensate")
def compensate_stats(data: dict):

    user_id = data["user_id"]
    activity = data["activity"]
    duration = data["duration"]
    calories = data["calories"]


    stats[user_id] = stats.get(user_id, 0) - duration
    if stats[user_id] < 0:
        stats[user_id] = 0

    if user_id in trainings:
        for i, t in enumerate(trainings[user_id]):
            if (
                t["activity"] == activity
                and t["duration"] == duration
                and t["calories"] == calories
            ):
                trainings[user_id].pop(i)
                break

    event_log.append({"event": data, "status": "compensated"})

    return {"status": "compensated", "total_minutes": stats.get(user_id, 0)}



def rabbitmq_consumer():

    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    credentials=pika.PlainCredentials("admin", "admin"),
                )
            )
            channel = connection.channel()


            channel.exchange_declare(
                exchange="training_dlx", exchange_type="direct", durable=True
            )
            channel.queue_declare(queue="training_events_dlq", durable=True)
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

            def callback(ch, method, properties, body):
                data = json.loads(body)
                print("[STATS] Received ASYNC event for processing:", data)

                event_log.append({"event": data, "status": "received"})


                try:
                    raise Exception("Simulated processing error in stats-service")
                except Exception as e:
                    print(
                        "[STATS] Error processing event, send to DLQ via nack:",
                        e,
                    )
                    event_log.append({"event": data, "status": "failed"})

                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                    return

            channel.basic_consume(
                queue="training_events",
                on_message_callback=callback,
            )
            print("[STATS] Listening for async events with DLQ")
            channel.start_consuming()

        except Exception as e:
            print("Consumer error in stats-service:", e)
            time.sleep(5)
