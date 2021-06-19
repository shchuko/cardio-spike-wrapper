from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
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


@app.get("/")
async def main():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="en">
<body>
<h1>Health</h1>
<h2>Analyze data from CSV file</h2>
<form id="formElem" onsubmit="return false">
    <input id="fileinput" type="file" name="fileupload"/>
    <button id="uploadbtn" disabled="disabled">Analyze Data</button>
</form>

<ul id="messages">
</ul>

<div id="downloadlink">
</div>

<div id="statslist">
</div>

<div id="picture">
</div>

<script>
    const ws = new WebSocket(`ws://cardio-spike-alvani.herokuapp.com/ws`)
    const linkelem = document.getElementById('downloadlink')
    const messages = document.getElementById('messages')
    const statslist = document.getElementById('statslist')
    const picture = document.getElementById('picture')
    const uploadbtn = document.getElementById('uploadbtn')
    const fileinput = document.getElementById('fileinput')
    const funcs = [process_status, process_png, process_stats, process_csv]
    let func_no = 0

    uploadbtn.disabled = "disabled"

    ws.onopen = function () {
        uploadbtn.disabled = ""
    }

    ws.onclose = function () {
        uploadbtn.disabled = "disabled"
    }

    ws.onmessage = async function (event) {
        await funcs[func_no](event.data)
    }
    
    function viewMsg(msg) {
        var message = document.createElement('li')
        var content = document.createTextNode(msg)
        message.appendChild(content)
        messages.appendChild(message)
    }
    
    uploadbtn.onclick = async () => {
        messages.innerHTML = ''
        downloadlink.innerHTML = ''
        statslist.innerHTML = ''
        picture.innerHTML = ''
        uploadbtn.disabled = "disabled"
        
        ws.send(fileinput.files[0])
        viewMsg('processing started...')
    }

    async function process_status(data) {
        const json = JSON.parse(data)
        viewMsg('processing done, status: ' + json.status)
        
        if (json.status === 'success') {
            func_no++
        } else {
            func_no = 0
            uploadbtn.disabled = ""
        }
    }

    async function process_png(data) {
        const blob = new Blob([data], {type: "image/png"});
        const url = URL.createObjectURL(blob);
        const img = new Image();
        img.src = url;
        picture.appendChild(img)
        func_no++
    }

    async function process_stats(data) {
        const json = JSON.parse(data)
        var content = document.createTextNode(JSON.stringify(json))
        statslist.appendChild(content)
        func_no++
    }

    async function process_csv(data) {
        const blob = new Blob([data], {type: 'text/plain'})

        const link = document.createElement('a')
        link.download = 'results.csv'
        link.href = URL.createObjectURL(blob)
        const linkText = document.createTextNode(link.download)
        link.appendChild(linkText)

        linkelem.appendChild(link)
        func_no = 0
        uploadbtn.disabled = ""
    }

</script>
</body>
</html>
""")
