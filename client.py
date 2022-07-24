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
async def test():
    async with websockets.connect("ws://localhost:2186") as websocket:
        await websocket.send("""{
    "request":"mainList", "page": 0
        }""")
        retur_msg = await websocket.recv()
        return retur_msg
print(asyncio.run(test()))