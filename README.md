Python-to-Golang IPC bridge
=================================================
[![Latest Stable Version](https://poser.pugx.org/spiral/goridge/v/stable)](https://packagist.org/packages/spiral/goridge) 
[![GoDoc](https://godoc.org/github.com/spiral/goridge?status.svg)](https://godoc.org/github.com/spiral/goridge)


Pygoridge is a Python-to-Golang codec library which works over sockets and Golang net/rpc package.
This is a python port of excellent [Goridge](https://github.com/spiral/goridge) library.
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

Example
--------
```python3
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
    print(rpc("App.Hi", "Antony"))
```

```go
package main

import (
    "fmt"
    "github.com/spiral/goridge/v2"
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

```python3
from pygoridge.json import json_dumps, json_loads


# you can also provide custom json encoder for faster marshalling
rpc = RPC(tcp_relay, json_encoder=json_dumps, json_decoder=json_loads)
```

See also [`examples`](./examples) for more examples (also with RoadRunner).
 
License
-------

The MIT License (MIT). Please see [`LICENSE`](./LICENSE) for more information.


Development
-----------

## Run tests

```bash
docker-compose -f ./goridge/tests/docker-compose.yml up
docker-compose -f tests/rr_test_app/docker-compose.yml up
python3 -m unittest discover -s tests
```

## TODO
- examples directory
- example with RR
- custom json encoder for Worker
