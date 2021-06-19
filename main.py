from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from websockets.exceptions import ConnectionClosed

from detect.stubs import AnalyzerStub

analyzer = AnalyzerStub()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive()
            data = message.get("bytes")
            if data is None:
                await websocket.send_json({"status": "bad_data"})
                continue

            result = await analyzer.analyze(bytes(data).decode())
            if result is None:
                await websocket.send_json({"status": "bad_data"})
                continue

            await websocket.send_json({"status": "success"})
            await websocket.send_bytes(result.get_png_content())
            await websocket.send_json(result.get_stats().dict())
            await websocket.send_text(result.get_csv_content())

    except (WebSocketDisconnect, ConnectionClosed):
        pass

