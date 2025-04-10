# server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import signal
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global reference to the OSC script process
osc_process = None

@app.post("/start-osc")
async def start_osc(config: dict):
    """Launch the OSC script with user's IP/port"""
    global osc_process
    if osc_process is None:
        osc_process = subprocess.Popen([
            "python", 
            "osc_controller.py", 
            config["ip"], 
            str(config["port"])
        ])
        return {"status": "started"}
    return {"status": "already_running"}

@app.post("/stop-osc")
async def stop_osc():
    """Terminate the OSC script"""
    global osc_process
    if osc_process:
        osc_process.terminate()
        osc_process = None
        return {"status": "stopped"}
    return {"status": "not_running"}