#Test WS client
import asyncio
import websockets
# ws = websocket.WebSocket()
# ws.connect("ws://localhost:2186")
# ws.send("""{
# "request":"mainList", "page": 1
# }""")
# print(ws.recv())
# ws.close()

#input_int = input("input page number:")
json = ("""{
    "request":"uploading",
    "host_name":"Dylan",
    "tulpas_name" : ["veronica", "example"],
    "host_age": "15",
    "email": "chendylan680@gmail.com",
    "file_name": "dchen4",
    "cover_name": "cover",
    "introduce": "Hello guys",
    "webinput": "<h1>This is dang intresting</h1>",
    "cover": "PGgxPuWXqOWXqOWXqDwvaDE+",
    "file": "PGgxPuWXqOWXqOWXqDwvaDE+"

}""")
async def test():
    async with websockets.connect("ws://localhost:2186") as websocket:
        await websocket.send(json)
        retur_msg = await websocket.recv()
        return retur_msg
print(asyncio.run(test()))