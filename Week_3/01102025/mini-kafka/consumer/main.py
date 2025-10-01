import argparse
import asyncio
import httpx # type: ignore
from pathlib import Path
import sys
BASE = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE))
from shared.schemas import ConsumerRegistration, ConsumeRequest, TopicRegistration

async def main():
    parser = argparse.ArgumentParser(description="Mini Kafka Consumer")
    parser.add_argument("--broker", default="http://127.0.0.1:8000")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--consumer-id", default=None)
    parser.add_argument("--poll-interval", type=float, default=1.0)
    args = parser.parse_args()

    async with httpx.AsyncClient(timeout=10.0) as client:
        await client.post(f"{args.broker}/topics/register", json=TopicRegistration(topic=args.topic).model_dump())        
        r = await client.post(f"{args.broker}/consumers/register", json=ConsumerRegistration(topic=args.topic, consumer_id=args.consumer_id).model_dump())        
        consumer_id = r.json()["consumer_id"]        
        print(f"Consumer registered: {consumer_id} on topic '{args.topic}'")
        while True:            
            res = await client.post(f"{args.broker}/consume", json=ConsumeRequest(consumer_id=consumer_id).model_dump())            
            if res.status_code == 200:                
                msg = res.json()                
                print(f"Consumed: topic={msg['topic']} offset={msg['offset']} value={msg['value']}")            
            elif res.status_code == 204:                
                await asyncio.sleep(args.poll_interval)            
            else:                
                print("Error:", res.status_code, res.text)                
                await asyncio.sleep(args.poll_interval)
if __name__ == "__main__":
    asyncio.run(main())
