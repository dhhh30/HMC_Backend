import asyncio
import websockets
from parser import parse_all
from os import environ, path
import signal
import init
from concurrent.futures import ProcessPoolExecutor
#returned mem_con object from init
memcon = init.init()
#task executor for multiprocessing
task_executer = ProcessPoolExecutor(max_workers=3)
#main handler of request
async def handler(websocket):
    print("Got request")
    remote_ip = websocket.remote_address
    try:
        loop = asyncio.get_running_loop()
        async for message in websocket:
            print(message)
            #response = await loop.run_in_executor(task_executor, parse_All, message)
            #await websocket.send(str(response))
    except websockets.ConnectionClosedOK:
        print("Client Disconnected with IP:", remote_ip)
    #Catch connection reset by peer
    except ConnectionResetError:
        print("Connection reset by peer with IP:", remote_ip)
    finally:
        return
#main function
async def main():

    #Serves WS behind NGINX via UNIX Socket
    # loop = asyncio.get_running_loop()
    # stop = loop.create_future()
    # loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    # async with websockets.unix_serve(handler, path=f"{os.environ['SUPERVISOR_PROCESS_NAME']}.sock",):
    #     await asyncio.Future()


    async with websockets.serve(handler,"",2186):
        await asyncio.Future()
#ping client
#run main function

asyncio.run(main())
