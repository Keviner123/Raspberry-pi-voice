import asyncio
import websockets

class WebSocketClient:

    
async def main():
    client = WebSocketClient("wss://api.prøve.svendeprøven.dk/ws/r2d2device")
    response = await client.send_and_receive('{"Type": "mac","Message": "00:B0:D0:63:C2:11"}')
    print(response)

asyncio.run(main())