import asyncio
import websockets
from os import environ, path
import signal
from parser import parse_all
from concurrent.futures import ProcessPoolExecutor
task_executor = ProcessPoolExecutor()

async def handler(websocket):
    print("Got request")
    remote_ip = websocket.remote_address
    print(remote_ip)
    loop = asyncio.get_event_loop()
    try:
        async for message in websocket:
            print(message)
            response = loop.run_in_executor(task_executor,parse_all, message)
            print(response)
            await websocket.send(str(response))

    except websockets.ConnectionClosedOK:
        print("Client Disconnected with IP:", remote_ip)
    #Catch connection reset by peer
    except ConnectionResetError:
        print("Connection reset by peer with IP:", remote_ip)
#main function
async def main():
    websockets.serve(handler,"",2186)
#ping client
#run main function

asyncio.run(main())
