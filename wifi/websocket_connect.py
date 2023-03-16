import websockets
import asyncio
import json

async def hello():
    async with websockets.connect("wss://api.prøve.svendeprøven.dk/ws/r2d2device") as websocket:
        # create a socket message as a json object
        web_socket_message = {
            "Type": "register",
            "Message": "11:11:11:11:11:11", # mac address here
        }
        jsons = json.dumps(web_socket_message)
        await websocket.send(jsons)
        result = await websocket.recv()
        print(f"< {result}")


asyncio.run(hello())