#!/l0/venv/bin/python
"""Bus observer for CTRL-0004. Runs in a container on the mesh network and records
what a third party can actually see on the wire.

This is how the descriptor, heartbeat and telemetry criteria are checked: not by
asking the citizen what it published, but by watching the bus. Audit is the
transport (PA-014), so the suite reads the transport.
"""
import argparse
import asyncio
import json
import sys

import nats


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="nats://nats:4222")
    ap.add_argument("--seconds", type=float, default=12.0)
    ap.add_argument("--subjects", nargs="+", default=["mesh.>", "acta.>", "work.>"])
    ap.add_argument("--publish-after", default=None,
                    help="JSON {subject, data} published once, N seconds in (rogue fixtures)")
    ap.add_argument("--publish-at", type=float, default=2.0)
    a = ap.parse_args()

    seen = []
    nc = await nats.connect(a.url, connect_timeout=5)

    async def handler(msg):
        try:
            payload = json.loads(msg.data)
        except ValueError:
            payload = {"_raw": msg.data.decode(errors="replace")}
        seen.append({"subject": msg.subject, "at": asyncio.get_event_loop().time(),
                     "envelope": payload})

    for s in a.subjects:
        await nc.subscribe(s, cb=handler)

    if a.publish_after:
        spec = json.loads(a.publish_after)
        await asyncio.sleep(a.publish_at)
        await nc.publish(spec["subject"], json.dumps(spec["data"]).encode())
        await asyncio.sleep(max(0.0, a.seconds - a.publish_at))
    else:
        await asyncio.sleep(a.seconds)

    await nc.drain()
    print("OBSERVED " + json.dumps(seen))
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
