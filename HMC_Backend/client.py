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
import time

start = time.time()


input_int = input("input page number:")
#json = ("""{
#     "request":"uploading",
#     "host_name":"Dylan",
#     "tulpas_name" : ["veronica", "example"],
#     "host_age": "15",
#     "email": "chendylan680@gmail.com",
#     "file_name": "dchen4",
#     "cover_name": "cover",
#     "imgs": ["imagebrurbub","image placeholder"],
#     "img_names": ["random.jpg","placeholder.jpg"],
#     "introduce": "Hello guys",
#     "webInput": "<h1>This is dang intresting</h1>",
#     "cover": "PGgxPuWXqOWXqOWXqDwvaDE+",
#     "file": "PGgxPuWXqOWXqOWXqDwvaDE+"
#
# }""")
json = ("""
{"request":"mainList",
"page": 1
}""")

async def test():
    async with websockets.connect("ws://english-poetry.com:2186") as websocket:
        await websocket.send(json)
        retur_msg = await websocket.recv()
        return retur_msg
for i in range(1000):
    print(asyncio.run(test()))
end = time.time()
print("1000 queries completed in:"+ str(end - start))
