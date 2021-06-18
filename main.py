import io

from fastapi import FastAPI, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

from detect.analyzers import BaseAnalyzer
from detect.stubs import AnalyzerStub

app = FastAPI()
analyzer = AnalyzerStub()


@app.post("/analyze")
async def load_file(file: bytes = File(...)):
    result_id = analyzer.queue_analyze(file.decode())
    return {"result_id": result_id}


@app.get("/result")
async def get_result_csv(result_id: str):
    if analyzer.is_ready(result_id=result_id) != BaseAnalyzer.AnalyzeStatus.READY:
        raise HTTPException(status_code=404, detail="Item not found")

    csv_path = analyzer.get_result(result_id=result_id).get_csv_path()
    return FileResponse(path=csv_path, filename="cardio-result.csv")


@app.get("/stats")
async def get_stats(result_id: str):
    if analyzer.is_ready(result_id=result_id) != BaseAnalyzer.AnalyzeStatus.READY:
        raise HTTPException(status_code=404, detail="Item not found")

    stats = analyzer.get_result(result_id=result_id).get_stats()
    return stats


@app.get("/diagram")
async def get_diagram(result_id: str):
    if analyzer.is_ready(result_id=result_id) != BaseAnalyzer.AnalyzeStatus.READY:
        raise HTTPException(status_code=404, detail="Item not found")

    png_bytes = analyzer.get_result(result_id=result_id).get_png()
    return StreamingResponse(io.BytesIO(png_bytes), media_type="image/png")


@app.get("/status")
async def check_status(result_id: str):
    status = "not_found"
    if analyzer.is_ready(result_id=result_id) == BaseAnalyzer.AnalyzeStatus.READY:
        status = "ready"
    elif analyzer.is_ready(result_id=result_id) == BaseAnalyzer.AnalyzeStatus.PROCESSING:
        status = "processing"

    return {"status": status}
