import argparse
import asyncio
import httpx # type: ignore
from pathlib import Path
import sys
BASE = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE))
from shared.schemas import ProducerRegistration, PublishRequest, TopicRegistration

async def main():
    parser = argparse.ArgumentParser(description="Mini Kafka Producer")
    parser.add_argument("--broker", default="http://127.0.0.1:8000")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--producer-id", default=None)
    args = parser.parse_args()

    async with httpx.AsyncClient(timeout=10.0) as client:        
        await client.post(f"{args.broker}/topics/register", json=TopicRegistration(topic=args.topic).model_dump())        
        r = await client.post(f"{args.broker}/producers/register", json=ProducerRegistration(topic=args.topic, producer_id=args.producer_id).model_dump())        
        producer_id = r.json().get("producer_id")        
        print(f"Producer registered: {producer_id} on topic '{args.topic}'")

        for i in range(args.count):            
            payload = PublishRequest(topic=args.topic, value=f"message-{i}") 
            res = await client.post(f"{args.broker}/produce", json=payload.model_dump())            
            res.raise_for_status()            
            print(f"Produced offset={res.json()['offset']} value='{payload.value}'")            
            await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(main())
