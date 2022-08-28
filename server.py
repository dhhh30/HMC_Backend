import asyncio
import websockets
import signal
from parser_ohaul import parse_all
import logging
import methods
logging.basicConfig(level=logging.DEBUG)
from parser_ohaul import parse_all
#current datetime for logging
cur_datetime = methods.datetimenow()
async def handler(websocket):
    logging.debug("Got request")
    #client's ip address
    remote_ip = websocket.remote_address
    print(remote_ip)
    try:
        #loop through messages sent by client
        async for message in websocket:       
            logging.debug(str(cur_datetime)+"The client at "+str(remote_ip)+"sent"+str(message))
            response = await parse_all(message)
            logging.debug(str(cur_datetime)+"Response to client at "+str(remote_ip)+"is"+str(response))
            print(type(response))
            await websocket.send(response)
        #on proper exit
    except websockets.ConnectionClosedOK:
        logging.info(str(cur_datetime)+"Client Disconnected with IP:"+str(remote_ip))
    #Catch connection reset by peer TCP RST
    except ConnectionResetError:
        logging.info(cur_datetime+"Connection reset by peer with IP:"+str(remote_ip))
    #on client refresh page, force end of connection
    except websockets.exceptions.ConnectionClosedError:
        logging.info(str(cur_datetime)+"client at "+str(remote_ip)+"disconnected improperly")
#main function
async def main():
    async with websockets.serve(handler,"",2186):
        #run forever with asyncio
        await asyncio.Future()
#ping client
#run main function

asyncio.run(main())