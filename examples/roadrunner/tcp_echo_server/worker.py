from pygoridge import create_relay, Worker
from pygoridge.json import json_loads, json_dumps


if __name__ == "__main__":
    rl = create_relay("pipes")
    worker = Worker(rl)

    while True:
        context, body = worker.receive()
        context = json_loads(context.tobytes())
        remote_addr = context["remote"]
        context["worker"] = "python"
        worker.send(body, context)
