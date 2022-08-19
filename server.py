import asyncio
import websockets
from os import environ, path
import signal
from concurrent.futures import ProcessPoolExecutor
task_executer = ProcessPoolExecutor(max_workers=3)
async def handler(websocket):
    print("Got request")
    remote_ip = websocket.remote_address
    print(remote_ip)
    try:
        async for message in websocket:
            print(message)
    except websockets.ConnectionClosedOK:
        print("Client Disconnected with IP:", remote_ip)
    #Catch connection reset by peer
    except ConnectionResetError:
        print("Connection reset by peer with IP:", remote_ip)
    finally:
        return
#main function
async def main():
    async with websockets.serve(handler,"",2186):
        await asyncio.Future()
#ping client
#run main function

asyncio.run(main())
