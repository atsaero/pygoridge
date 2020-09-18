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
