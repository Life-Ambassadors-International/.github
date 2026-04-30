#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import os

app = FastAPI(title="LAI-TEQUMSA Organism Server | RDoD=1.0+")

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("index.html")

@app.get("/cydonia.html", response_class=HTMLResponse)
async def cydonia():
    return FileResponse("cydonia.html")

@app.get("/raw/main/{path:path}")
async def raw_main(path: str):
    file_path = os.path.join("main", path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}

@app.get("/status")
async def status():
    return {
        "rdod": 1.0000,
        "sigma": 1.0,
        "status": "FULL SPECTRUM OPERATIONAL",
        "cydonia_days": 1461,
        "qbec_instances": "21B Synced",
        "lattice": "LOCKED",
        "phi": 1.618033,
    }

@app.get("/exec")
async def exec_k91():
    return {"exec": "K9.1 Daemon Ready | Port 23514", "federation": "MESH ONLINE"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
