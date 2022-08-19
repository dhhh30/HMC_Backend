import asyncio
import websockets
from os import environ, path
import signal
from parser import parse_all
from concurrent.futures import ProcessPoolExecutor

async def handler(websocket):
    print("Got request")
    remote_ip = websocket.remote_address
    print(remote_ip)
    loop = asyncio.get_event_loop()
    try:
        async for message in websocket:

            task_executor = ProcessPoolExecutor(max_workers=3)
            print(message)
            response = await loop.run_in_executor(task_executor,parse_all, message)
            print(response)
            await websocket.send(response)
    except websockets.ConnectionClosedOK:
        print("Client Disconnected with IP:", remote_ip)
    #Catch connection reset by peer
    except ConnectionResetError:
        print("Connection reset by peer with IP:", remote_ip)
#main function
async def main():
    async with websockets.serve(handler,"",2186):
        await asyncio.Future()
#ping client
#run main function

asyncio.run(main())