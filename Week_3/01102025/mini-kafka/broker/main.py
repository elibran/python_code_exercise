import asyncio
import uuid
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Response # pyright: ignore[reportMissingImports]
from fastapi.responses import JSONResponse # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
import uvicorn # type: ignore

from pathlib import Path
import sys
BASE = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE))
from shared.schemas import (
    TopicRegistration,
    ProducerRegistration,
    ConsumerRegistration,
    PublishRequest,
    ConsumeRequest,
    Message,
)

app = FastAPI(
    title="Mini Kafka Broker",
    version="0.2.1",
    description=(
        "A tiny educational broker that simulates Kafka-like publish/consume semantics.\n\n"
        "**Key notes**\n\n"
        "- In-memory only (data lost on restart)\n"
        "- Single topic list (no partitions/replication)\n"
        "- Per-consumer offset tracking\n\n"
        "Use the **/docs** page to try endpoints."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

topics: Dict[str, List[Dict]] = {}
consumers: Dict[str, Dict] = {}
locks: Dict[str, asyncio.Lock] = {}

def _ensure_topic(topic: str):
    if topic not in topics:
        topics[topic] = []
        locks[topic] = asyncio.Lock()

@app.get("/", tags=["meta"], summary="Welcome")
async def root():
    return {"message": "Mini Kafka Broker up. See /docs for Swagger UI."}

@app.get("/health", tags=["meta"], summary="Health check")
async def health():
    return {"status": "ok"}

@app.post("/topics/register", tags=["topics"], summary="Create/ensure a topic")
async def register_topic(payload: TopicRegistration):
    _ensure_topic(payload.topic)
    return {"status": "ok", "topic": payload.topic}

@app.post("/producers/register", tags=["producers"], summary="Register a producer (optional)")
async def register_producer(payload: ProducerRegistration):
    _ensure_topic(payload.topic)
    pid = payload.producer_id or f"producer-{uuid.uuid4().hex[:8]}"
    return {"status": "ok", "topic": payload.topic, "producer_id": pid}

@app.post("/consumers/register", tags=["consumers"], summary="Register a consumer and start at offset 0")
async def register_consumer(payload: ConsumerRegistration):
    _ensure_topic(payload.topic)
    cid = payload.consumer_id or f"consumer-{uuid.uuid4().hex[:8]}"
    consumers[cid] = {"topic": payload.topic, "offset": 0}
    return {"status": "ok", "topic": payload.topic, "consumer_id": cid}

@app.post("/produce", tags=["messages"], summary="Publish a message to a topic")
async def produce(payload: PublishRequest):
    if payload.topic not in topics:
        raise HTTPException(status_code=404, detail="Topic not found. Register it first.")
    msg = {"topic": payload.topic, "value": payload.value, "key": payload.key}
    async with locks[payload.topic]:
        offset = len(topics[payload.topic])
        msg["offset"] = offset
        topics[payload.topic].append(msg)
    return {"status": "ok", "offset": offset}

@app.post("/consume", response_model=Optional[Message], tags=["messages"], summary="Fetch next message for a consumer")
async def consume(req: ConsumeRequest):
    if req.consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Unknown consumer. Register first.")
    topic = consumers[req.consumer_id]["topic"]
    current_offset = consumers[req.consumer_id]["offset"]
    async with locks[topic]:
        messages = topics.get(topic, [])
        if current_offset < len(messages):
            msg = messages[current_offset]
            consumers[req.consumer_id]["offset"] = current_offset + 1
            return Message(**msg)
    # Important: 204 must not include a body
    return Response(status_code=204)

@app.get("/stats", tags=["meta"], summary="Broker stats")
async def stats():
    return {
        "topics": {t: len(msgs) for t, msgs in topics.items()},
        "consumers": consumers,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
