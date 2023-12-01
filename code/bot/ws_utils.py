import websocket

from config import backend as backend_url

async def sendWSMessage(url: str, msg: str):
    ws = websocket.WebSocket()
    ws.connect(url)
    ws.send(msg)
    ws.close()

async def receiveWSMessage(url: str):
    ws = websocket.WebSocket()
    ws.connect(url)
    msg = ws.recv()
    ws.close()
    return msg

def sendReceiveMessage(url: str, message: str):
    response_message = None

    def onOpen(ws):
        print("Connessione aperta")
        ws.send(message)
    def onMessage(_, message):
        nonlocal response_message
        response_message = message
    def onClose(_):
        print("Connessione chiusa")

    # Inizializza la connessione WebSocket
    ws = websocket.WebSocketApp(url,
                                on_open=onOpen,
                                on_message=onMessage,
                                on_close=onClose)
    # Avvia la connessione WebSocket in modo asincrono
    ws.run_forever()
    return response_message

def getWsUrl(gameId: str, token: str) -> str:
    return f'ws://{backend_url}/api/v1/game/{gameId}/{token}/ws'
