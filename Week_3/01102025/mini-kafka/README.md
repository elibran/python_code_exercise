# Mini Kafka (FastAPI + Python)

A tiny educational Kafka-like system with a FastAPI **broker** and Python **producer/consumer** clients.
The broker stores messages **in memory** per topic and tracks each consumer’s **offset**.

---

## Quickstart

1) Install deps
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Start the broker
```bash
python broker/main.py
```

Open Swagger UI: http://127.0.0.1:8000/docs  
OpenAPI JSON: http://127.0.0.1:8000/openapi.json

3) Run producer (sends 5 messages)
```bash
python producer/main.py --topic demo --count 5
```

4) Run consumer (polls for messages)
```bash
python consumer/main.py --topic demo --consumer-id abinash
```

---

## Endpoints (Broker)

- `GET /` → Welcome
- `GET /health` → Health check
- `POST /topics/register` → `{ topic }`
- `POST /producers/register` → `{ topic, producer_id? }`
- `POST /consumers/register` → `{ topic, consumer_id? }`
- `POST /produce` → `{ topic, value, key? }`
- `POST /consume` → `{ consumer_id }` → returns `{ topic, offset, value, key? }` or **HTTP 204** if none
- `GET /stats` → summary of topics and consumers

> Tip: Use the **/docs** Swagger page to try requests interactively.

---

# Beginner’s Guide (FastAPI Broker, Producer, Consumer)

This guide explains the codebase step‑by‑step for beginners who know Python and FastAPI. You’ll learn the folder layout, data models, HTTP API, and the end‑to‑end flow of producing and consuming messages.

## 1) What we are building

A minimal, **in‑memory** message broker (like a tiny Kafka). Three apps:

- **Broker (FastAPI server)** – stores messages per topic and tracks each consumer’s offset.
- **Producer (Python script)** – registers a topic, then publishes messages via HTTP.
- **Consumer (Python script)** – registers to a topic, then polls the broker for the next message.

Key constraints:
- Data exists only in RAM (lost if the broker restarts).
- One message list per topic (no partitions or replication).
- Each consumer has its own offset.

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

## 3) The data models (Pydantic)

`shared/schemas.py` defines the request/response shapes:

- `TopicRegistration`: `{ topic: str }` – used by producer/consumer to ensure the topic exists.
- `ProducerRegistration`: `{ topic: str, producer_id?: str }` – optional ID to tag a producer.
- `ConsumerRegistration`: `{ topic: str, consumer_id?: str }` – if not given, broker creates one.
- `PublishRequest`: `{ topic: str, value: str, key?: str }` – message payload is a simple string.
- `ConsumeRequest`: `{ consumer_id: str }` – identifies which consumer wants the next message.
- `Message`: `{ topic: str, offset: int, value: str, key?: str }` – what the broker returns.

Remember: **offset** is the index in the topic’s list of messages.

## 4) Broker internals

**File:** `broker/main.py`

### 4.1 App setup
- Creates a FastAPI app with metadata (so you get Swagger UI at `/docs`).  
- Adds permissive CORS (so you can experiment from a browser later).

### 4.2 In‑memory storage
```python
# topics[topic] = list of messages (dicts with topic, value, key?, offset)
# consumers[consumer_id] = {"topic": str, "offset": int}
# locks[topic] = asyncio.Lock() so writes/reads are serialized per topic
```
- `topics`: maps topic -> list of message dicts.  
- `consumers`: for each consumer ID, track which topic they’re on and the next offset to read.  
- `locks`: an `asyncio.Lock()` per topic to prevent race‑conditions between produce/consume.

### 4.3 Endpoints (what they do)
- `GET /` – simple welcome.  
- `GET /health` – health check.  
- `POST /topics/register` – create the topic array if missing.  
- `POST /producers/register` – acknowledge a producer (for logging/demo).  
- `POST /consumers/register` – create a consumer and set its offset to `0`.  
- `POST /produce` – append a new message to `topics[topic]` and assign `offset = len(list)` before append.  
- `POST /consume` – look up the consumer’s current offset; if a message exists at that index, return it and increment the offset; otherwise return **HTTP 204** (no content).  
- `GET /stats` – returns counts per topic and all consumer offsets.

### 4.4 Why locks?
Even though FastAPI is async, multiple requests can interleave. If two producers append at the same time, without a lock the length/offset computations could clash. The per‑topic lock ensures **produce** and **consume** operations on that topic are atomic enough for our simple model.

## 5) Producer walkthrough

**File:** `producer/main.py`

High‑level flow:
1. Parse CLI args: `--broker`, `--topic`, `--count`, `--producer-id`.
2. `POST /topics/register` to ensure the topic exists.
3. `POST /producers/register` (optional bookkeeping) – broker returns a `producer_id`.
4. Loop `count` times:
   - Build `PublishRequest(topic, value=f"message-{i}")`.
   - `POST /produce`.
   - Print the returned `offset`.

**Why async httpx?** It fits naturally with FastAPI’s async style and makes it easy to add concurrency later.

## 6) Consumer walkthrough

**File:** `consumer/main.py`

High‑level flow:
1. Parse CLI args: `--broker`, `--topic`, `--consumer-id`, `--poll-interval`.
2. `POST /topics/register` to ensure topic.
3. `POST /consumers/register` to get (or confirm) a `consumer_id` and start at offset `0`.
4. Infinite loop:
   - `POST /consume` with `{ consumer_id }`.
   - If **200**, print the message and continue.
   - If **204**, sleep for `poll_interval` seconds and try again.

This is a basic **polling** consumer. (See §9 for alternatives.)

## 7) End‑to‑end flow (ASCII diagrams)

### 7.1 Topic creation and producing messages
```
Producer                   Broker
   |  POST /topics/register  |
   |------------------------>|  ensure topic exists
   |                         |
   |  POST /producers/register
   |------------------------>|  returns producer_id
   |                         |
Loop N times:
   |  POST /produce {topic, value}
   |------------------------>|  append to list; offset = list length before
   |  <----------------------|  {offset}
```

### 7.2 Consuming messages
```
Consumer                   Broker
   |  POST /topics/register  |
   |------------------------>|  ensure topic exists
   |                         |
   |  POST /consumers/register (topic)
   |------------------------>|  {consumer_id, offset=0}
   |                         |
Repeat:
   |  POST /consume {consumer_id}
   |------------------------>|
   |  <----------------------|  200 {topic, offset, value} or 204 (no content)
```

## 8) How offsets work (by example)

Suppose topic `demo` has messages: indices `[0, 1, 2]`.
- New consumer `abinash` starts with `offset = 0`.
- First `/consume` → returns message at index 0, then sets `offset = 1`.
- Next `/consume` → returns index 1, then `offset = 2`.
- If there is no message at index 2 yet, broker returns `204`.

Each consumer’s offset is independent. A second consumer `bob` also starts at `0` and will receive all messages from the beginning.

## 9) Polling vs. long‑polling vs. push

This sample uses **short polling** (consumer keeps asking). Improvements:
- **Long‑polling**: broker waits up to X seconds for a message before replying `204`.
- **Server‑Sent Events (SSE)**: broker streams events; consumer reads a stream.
- **WebSockets**: bi‑directional; more interactive but more code.

For learning, short polling is simplest and robust enough to demo offsets and ordering.

## 10) Running and testing

1. Install dependencies and start the broker:
```bash
python broker/main.py
```
Visit Swagger UI at `http://127.0.0.1:8000/docs` to try endpoints interactively.

2. Produce some messages:
```bash
python producer/main.py --topic demo --count 5
```

3. Consume them:
```bash
python consumer/main.py --topic demo --consumer-id abinash
```

4. View broker state:
```bash
curl http://127.0.0.1:8000/stats | jq
```

## 11) Common pitfalls & troubleshooting

- **204 No Content**: Not an error—means there is no new message for that consumer offset. Keep polling.
- **404 Topic not found**: Call `/topics/register` first or ensure the producer did it.
- **Restarting broker loses data**: By design; it’s in‑memory. If you need persistence, write to disk or a database.
- **Multiple consumers**: Give each a unique `--consumer-id`. They track offsets independently.
- **Throughput**: This demo is single‑process, single‑host. For higher throughput, you’d add partitions, batching, or async workers.

## 12) How to extend (ideas)

- **Durability**: Save messages to disk (e.g., SQLite or append‑only file).
- **Long‑polling**: Add a `timeout_ms` query param on `/consume` and `await asyncio.wait_for(...)` to wait for new messages.
- **Partitions**: Replace the single list per topic with multiple lists (shards) and a partitioner (e.g., by key hash).
- **Consumer groups**: Track groups and deliver each message to one member of the group.
- **Offset management**: Add `/commit` to let consumers manage when offsets are advanced (at‑least‑once vs at‑most‑once semantics).
- **Backpressure/limits**: Add max topic size, retention policies, and pagination in `/consume` to fetch batches.
- **Auth & ACLs**: Require tokens and per‑topic permissions.

## 13) Code reading checklist (for beginners)

1. Open `broker/main.py`:
   - Find the global dictionaries: `topics`, `consumers`, `locks`.
   - Read `_ensure_topic`.
   - Read `produce` and see where `offset` is assigned.
   - Read `consume` and see how the consumer’s offset is advanced.
2. Open `shared/schemas.py` and match models to endpoints.
3. Open `producer/main.py` and `consumer/main.py` and follow the CLI → HTTP call flow.
4. Use `/docs` to hit the endpoints and watch the console output of producer/consumer.

## 14) FAQ

**Q: Why FastAPI for the broker?**  
A: It’s lightweight, async‑friendly, and gives you Swagger UI for free.

**Q: Is message ordering guaranteed?**  
A: Within a topic list, yes—because we append and read sequentially. There are no partitions here.

**Q: What happens on broker restart?**  
A: All data is cleared. Persistence would need a storage layer.

**Q: Can I run multiple consumers on the same topic?**  
A: Yes. Each gets its own offset and will independently read all messages.

**Q: Can I have multiple topics?**  
A: Yes—`/topics/register` creates them on demand, and the broker keeps separate lists.

## 15) Next steps

- Try two consumers (`abinash` and `rahul`) on the same topic and observe offsets.
- Add a `key` to some messages and modify the consumer to filter by key (client‑side).
- Implement long‑polling for `/consume` (great small exercise!).

---

### License
Classroom Exercise in FIL (for this example project).
