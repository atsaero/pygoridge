Pygoridge: Python-to-Golang IPC bridge, python client for Goridge
=================================================================
[![GoDoc](https://godoc.org/github.com/spiral/goridge?status.svg)](https://godoc.org/github.com/spiral/goridge)


Pygoridge is a Python-to-Golang codec library which works over sockets and Golang net/rpc package.
This is a python port of php client for an excellent [Goridge](https://github.com/spiral/goridge) library.
The library allows you to call Go service methods from Python with minimal footprint, structures and `[]byte` support.


Also Pygoridge includes `Worker` class to use in worker processes with https://github.com/spiral/roadrunner - high-performance application server, load-balancer and process manager written in Golang.

Features
--------
 - no external dependencies
 - can be used with [RoadRunner](https://github.com/spiral/roadrunner) to create CPU-intensive servers with simple sequential python workers (no multiprocessing module required). This is really helpful to overcome GIL.

Installation
------------
```
$ go get "github.com/spiral/goridge"
```
```
$ pip install pygoridge
```

Example: python client calls go server methods
----------------------------------------------

```python
from pygoridge import create_relay, RPC, SocketRelay

rpc = RPC(SocketRelay("127.0.0.1", 6001))

# or, using factory
tcp_relay = create_relay("tcp://127.0.0.1:6001")
unix_relay = create_relay("unix:///tmp/rpc.sock")
stream_relay = create_relay("pipes")

print(rpc("App.Hi", "Antony"))
rpc.close()     # close underlying socket connection

# or using as a context manager
with RPC(tcp_relay) as rpc:
    print(rpc("App.Hi", "Antony, again"))
```

```go
package main

import (
    "fmt"
    "github.com/spiral/goridge"
    "net"
    "net/rpc"
)

type App struct{}

func (s *App) Hi(name string, r *string) error {
    *r = fmt.Sprintf("Hello, %s!", name)
    return nil
}

func main() {
    ln, err := net.Listen("tcp", ":6001")
    if err != nil {
        panic(err)
    }

    rpc.Register(new(App))

    for {
        conn, err := ln.Accept()
        if err != nil {
            continue
        }
        go rpc.ServeCodec(goridge.NewCodec(conn))
    }
}
```

Example: go http server (RoadRunner) with python workers
--------------------------------------------------------

You can download latest RoadRunner binary from [releases page](https://github.com/spiral/roadrunner/releases).

See also [`examples`](./examples).

```sh
cd examples/roadrunner/http_server/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Worker class

```python
from functools import partial

import ujson
from pygoridge import create_relay, Worker


json_dumps = partial(
    ujson.dumps, ensure_ascii=False,
    escape_forward_slashes=False)
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
```

Run RoadRunner server
```sh
cd examples/roadrunner/http_server/
./rr serve -d -v
```

Make http request to get request headers back as a response body
```sh
curl 'http://localhost:8080/' --compressed
```

RoadRunner is highly customizable and extendable so you can even write your own plugin for it with required API protocol (see for example [php-grpc server](https://github.com/spiral/php-grpc)).


Custom encoders/decoders for faster json processing
---------------------------------------------------

```python
from pygoridge.json import json_dumps, json_loads


# you can also provide custom json encoder for faster marshalling
rpc = RPC(tcp_relay, json_encoder=json_dumps, json_decoder=json_loads)
```
 
License
-------

The MIT License (MIT). Please see [`LICENSE`](./LICENSE) for more information.


Development
-----------

### Run tests

```sh
docker-compose -f ./goridge/tests/docker-compose.yml up -d
docker-compose -f tests/rr_test_app/docker-compose.yml up -d
python3 -m unittest discover -s tests
```

### Run linter

```
pip install flake8
flake8 pygoridge
```