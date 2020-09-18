from functools import partial

import ujson
from pygoridge import create_relay, Worker, RPC


json_dumps = partial(ujson.dumps, ensure_ascii=False, escape_forward_slashes=False)
json_loads = ujson.loads


class HTTPWorker(Worker):

    def hello(self, headers):
        return headers, {"X-Server": "RoadRunner with python workers"}


if __name__ == "__main__":
    rl = create_relay("pipes")
    worker = HTTPWorker(rl, json_encoder=json_dumps, json_decoder=json_loads)

    while True:
        context, body = worker.receive()
        if context is None:
            continue
        http_headers = json_loads(context.tobytes())
        response, response_headers = worker.hello(http_headers)
        worker.send(
           json_dumps(response).encode("utf-8"),
           response_headers 
        )
