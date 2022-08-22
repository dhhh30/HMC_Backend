import asyncio
import websockets
import signal
from parser import parse_all
import logging
import methods
logging.basicConfig(level=logging.INFO)
#current datetime for logging
cur_datetime = methods.datetimenow()
async def handler(websocket):
    print("Got request")
    #client's ip address
    remote_ip = websocket.remote_address
    print(remote_ip)
    try:
        #loop through messages sent by client
        async for message in websocket:       
            logging.debug(cur_datetime+"The client at "+remote_ip+"sent"+str(message))
            response = await parse_all(message)
            logging.debug(cur_datetime+"Response to client at "+remote_ip+"is"+response)
            await websocket.send(str(response))
        #on proper exit
    except websockets.ConnectionClosedOK:
        logging.info(cur_datetime+"Client Disconnected with IP:"+remote_ip)
    #Catch connection reset by peer TCP RST
    except ConnectionResetError:
        logging.info(cur_datetime+"Connection reset by peer with IP:"+remote_ip)
    #on client refresh page, force end of connection
    except websockets.exceptions.ConnectionClosedError:
        logging.info(cur_datetime+"client at "+remote_ip+"disconnected improperly")
#main function
async def main():
    async with websockets.serve(handler,"",2186):
        #run forever with asyncio
        await asyncio.Future()
#ping client
#run main function

asyncio.run(main())