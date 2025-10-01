# Mini Kafka – Beginner’s Guide (FastAPI Broker, Producer, Consumer)

This guide explains the codebase step‑by‑step for beginners who know Python and FastAPI. You’ll learn the folder layout, data models, HTTP API, and the end‑to‑end flow of producing and consuming messages.

---

## 1) What we are building

A minimal, **in‑memory** message broker (like a tiny Kafka). Three apps:

- **Broker (FastAPI server)** – stores messages per topic and tracks each consumer’s offset.
- **Producer (Python script)** – registers a topic, then publishes messages via HTTP.
- **Consumer (Python script)** – registers to a topic, then polls the broker for the next message.

Key constraints:
- Data exists only in RAM (lost if the broker restarts).
- One message list per topic (no partitions or replication).
- Each consumer has its own offset.

---

## 2) Folder structure at a glance

```
mini-kafka/
├─ broker/
│  └─ main.py          # FastAPI app (the broker)
├─ producer/
│  └─ main.py          # Producer script
├─ consumer/
│  └─ main.py          # Consumer script
├─ shared/
│  └─ schemas.py       # Pydantic models shared by all apps
├─ requirements.txt
└─ README.md
```

Why this split?
- **broker** is a web server with endpoints.
- **producer/consumer** are plain Python clients using HTTP.
- **shared** avoids duplicating request/response models.

---

## 3) The data models (Pydantic)

`shared/schemas.py` defines the request/response shapes. You already know Pydantic, so focus on what each model represents:

- `TopicRegistration`: `{ topic: str }` – used by producer/consumer to ensure the topic exists.
- `ProducerRegistration`: `{ topic: str, producer_id?: str }` – optional ID to tag a producer.
- `ConsumerRegistration`: `{ topic: str, consumer_id?: str }` – if not given, broker creates one.
- `PublishRequest`: `{ topic: str, value: str, key?: str }` – message payload is a simple string.
- `ConsumeRequest`: `{ consumer_id: str }` – identifies which consumer wants the next message.
- `Message`: `{ topic: str, offset: int, value: str, key?: str }` – what the broker returns.

Remember: **offset** is the index in the topic’s list of messages.

---

## 4) Broker internals

... (rest of the detailed explanation continues exactly as in the guide) ...
