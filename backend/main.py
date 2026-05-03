from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from message_bus import manager
from orchestrator import run_task
from database import init_db
import asyncio
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("DEBUG: WebSocket connection attempt")
    await manager.connect(websocket)
    print("DEBUG: WebSocket connected")
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print(f"DEBUG: WebSocket disconnected/error: {e}")
        manager.disconnect(websocket)

@app.post("/task")
async def start_task(task: dict):
    description = task.get("description", "No description")
    asyncio.create_task(run_task(description, manager))
    return {"status": "started"}

import os

@app.get("/workspace")
async def get_workspace_files():
    workspace_path = "/Users/bipin/programming/projects/AI office System/ai-office/workspace"
    files = []
    for root, dirs, filenames in os.walk(workspace_path):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(root, filename), workspace_path)
            if not rel_path.startswith(".") and not rel_path.endswith(".db"):
                files.append(rel_path)
    return {"files": files}

@app.get("/workspace/{file_path:path}")
async def get_file_content(file_path: str):
    full_path = os.path.join("/Users/bipin/programming/projects/AI office System/ai-office/workspace", file_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        with open(full_path, "r") as f:
            return {"content": f.read()}
    return {"error": "File not found"}
