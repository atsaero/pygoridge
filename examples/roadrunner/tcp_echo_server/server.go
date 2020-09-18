package main

import (
	"bufio"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net"
	"runtime"
	"strings"
	"time"

	"github.com/spiral/roadrunner"
)

type Context struct {
	Remote   string  	`json:"remote"`
}


func handleConnection(c net.Conn, rr *roadrunner.Server) {
	defer c.Close()
    data, err := bufio.NewReader(c).ReadString('\n')
    if err != nil && err != io.EOF {
        panic(err)
    }
    context := Context{Remote: c.RemoteAddr().String()}
    jsonContext, _ := json.Marshal(context)

    if !checkIsHealthy(rr) {
    	panic(errors.New("rr server is dead"))
    }
    res, err := rr.Exec(&roadrunner.Payload{Body: []byte(data), Context: jsonContext})
    if err != nil {
    	panic(err)
    }
    c.Write(res.Body)
}


func checkIsHealthy(rr *roadrunner.Server) bool {
	pool := rr.Pool()
	if pool == nil {
		return false
	}

	for _, w := range pool.Workers() {
		if w.State().IsActive() {
			return true
		}
	}
	return false
}


func main() {
	address := ":7081"
	ln, err := net.Listen("tcp", address)
	if err != nil {
		panic(err)
	}

	srv := roadrunner.NewServer(
    &roadrunner.ServerConfig{
        Command: "python3 worker.py",
        Relay:   "pipes",
        Pool: &roadrunner.Config{
            NumWorkers:      int64(runtime.NumCPU()),
            AllocateTimeout: time.Second,
            DestroyTimeout:  time.Second,
        },
    })
	defer srv.Stop()

	err = srv.Start()
	if err != nil {
		panic(err)
	}

	fmt.Printf("started rr server @ %s\n", address)
	for {
		conn, err := ln.Accept()
		if err != nil {
			panic(err)
		}
		go handleConnection(conn, srv)
	}
}
