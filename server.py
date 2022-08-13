import asyncio
import websockets
from parser import parse_all
from os import environ, path
import signal
import init
from concurrent.futures import ProcessPoolExecutor
#returned mem_con object from init

#task executor for multiprocessing
task_executer = ProcessPoolExecutor(max_workers=3)
#main handler of request
def get_response(message):
    loop = asyncio.get_running_loop()
    response = loop.run_in_executor(task_executer, parse_all, message)
    return response
async def sender(websocket, message):
    remote_ip = websocket.remote_address 
    try:
        websocket.send(message)
    except websockets.ConnectionClosedOK:
        print("Client Disconnected with IP:", remote_ip)
    #Catch connection reset by peer
    except websockets.ConnectionResetError:
        print("Connection reset by peer with IP:", remote_ip)    
async def handler(websocket):

    print("Got request")
 
    #multiprocessing

    message = await websocket.recv()
    response = get_response(message)
    print(response)
    await sender(websocket, response)
    
        # for task in asyncio.asyncio.as_completed(tasks):
        #     response = await task
        #     loop.create_task(sender(websocket, response))



#main function
# async def main():

#     #Serves WS behind NGINX via UNIX Socket
#     # loop = asyncio.get_running_loop()
#     # stop = loop.create_future()
#     # loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
#     # async with websockets.unix_serve(handler, path=f"{os.environ['SUPERVISOR_PROCESS_NAME']}.sock",):
#     #     await asyncio.Future()



#ping client
#run main function
main = websockets.serve(handler,"",2186)
loop = asyncio.get_event_loop()
loop.run_until_complete(main)
loop.run_forever()
