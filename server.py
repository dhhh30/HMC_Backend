import asyncio
from cProfile import run
import websockets
from parser import parse_all
from os import environ, path
from multiprocessing import Process
import init
import threading
from multiprocessing import Semaphore
#returned mem_con object from init
memcon = init.init()
concurrency = 4
sema = Semaphore(concurrency)
async def parser(websocket):
    print("Got request")
    remote_ip = websocket.remote_address
    print("Client Disconnected with IP:", remote_ip)    
    try:
        message = await websocket.recv()
        response = parse_all(message, memcon)
        #print(response)
        await websocket.send(str(response))
    except websockets.ConnectionClosedOK:
        print("Client Disconnected with IP:", remote_ip)
    #Catch connection reset by peer
    except ConnectionResetError:
        print("Connection reset by peer with IP:", remote_ip)
#main handler of request
def handler(websocket):
    all_processes = []
    sema.acquire()
    p = Process(target=f, args=(i, sema))
    all_processes.append(p)
    p.start()
    p.join()
def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ws_server = websockets.serve(handler,"",2186)
    loop.run_until_complete(ws_server)
    loop.run_forever()
    loop.close()
#main function

#async def main():

    #Serves WS behind NGINX via UNIX Socket
    # loop = asyncio.get_running_loop()
    # stop = loop.create_future()
    # loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    # async with websockets.unix_serve(handler, path=f"{os.environ['SUPERVISOR_PROCESS_NAME']}.sock",):
    #     await asyncio.Future()


 #   async with websockets.serve(handler,"",2186):
#      await asyncio.Future()
#ping client
#run main function
server_main = threading.Thread(target=main)
server_main.start()
