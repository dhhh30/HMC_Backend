import asyncio
import websockets
import signal
from parser import parse_all
import logging
import methods
logging.basicConfig(level=logging.INFO)
async def handler(websocket):
    print("Got request")
    remote_ip = websocket.remote_address
    print(remote_ip)
    loop = asyncio.get_event_loop()
    try:
        async for message in websocket:       
            logging.debug("the client at "+remote_ip+"sent"+str(message))
            response = await parse_all(message)
            # print(response)
            await websocket.send(str(response))
    except websockets.ConnectionClosedOK:
        print("Client Disconnected with IP:", remote_ip)
    #Catch connection reset by peer
    except ConnectionResetError:
        print("Connection reset by peer with IP:", remote_ip)
    except websockets.exceptions.ConnectionClosedError:
        print("client at "+remote_ip+"disconnected improperly")
#main function
async def main():
    async with websockets.serve(handler,"",2186):
        await asyncio.Future()
#ping client
#run main function

asyncio.run(main())