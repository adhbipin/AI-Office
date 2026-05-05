from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from message_bus import manager
from orchestrator import run_task
from database import init_db, get_messages
from config import WORKSPACE_ROOT, HOST, PORT
import asyncio
import json
import os

# Initialize FastAPI app
app = FastAPI(
    title="AI Office",
    description="Multi-agent AI system running locally",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the HTML file
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on app startup."""
    print("\n" + "="*60)
    print("🚀 AI OFFICE BACKEND STARTING UP")
    print("="*60)
    print(f"Workspace: {WORKSPACE_ROOT}")
    print(f"Server: {HOST}:{PORT}")
    print(f"WebSocket: ws://{HOST}:{PORT}/ws")
    print("="*60 + "\n")
    
    init_db()
    print("✅ Backend ready. Waiting for connections...\n")

# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections for real-time agent communication."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Task submission endpoint
@app.post("/task")
async def start_task(payload: dict):
    """Start a new task execution."""
    description = payload.get("description", "No description provided")
    print(f"\n📝 NEW TASK RECEIVED: {description}\n")
    
    # Run task in background
    asyncio.create_task(run_task(description, manager))
    
    return {
        "status": "started",
        "description": description,
        "message": "Task started. Watch the live feed for agent updates."
    }

# Workspace file listing endpoint
@app.get("/workspace")
async def get_workspace_files():
    """List all files in the workspace."""
    files = []
    
    if not os.path.exists(WORKSPACE_ROOT):
        return {"files": []}
    
    try:
        for root, dirs, filenames in os.walk(WORKSPACE_ROOT):
            for filename in filenames:
                # Skip database and hidden files
                if filename.startswith(".") or filename.endswith(".db"):
                    continue
                
                rel_path = os.path.relpath(os.path.join(root, filename), WORKSPACE_ROOT)
                files.append(rel_path)
    except Exception as e:
        print(f"Error listing workspace: {e}")
    
    return {"files": sorted(files)}

# File content endpoint
@app.get("/workspace/{file_path:path}")
async def get_file_content(file_path: str):
    """Get the content of a specific file."""
    full_path = os.path.join(WORKSPACE_ROOT, file_path)
    
    # Security: prevent directory traversal
    if not os.path.abspath(full_path).startswith(os.path.abspath(WORKSPACE_ROOT)):
        return {"error": "Invalid file path"}
    
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        return {"error": f"File not found: {file_path}"}
    
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}

# Message history endpoint
@app.get("/messages")
async def get_message_history(limit: int = 100):
    """Get message history from the database."""
    messages = get_messages(limit)
    return {"messages": messages}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Office Backend",
        "connections": len(manager.active_connections),
        "workspace": WORKSPACE_ROOT
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API documentation."""
    return {
        "service": "AI Office Backend",
        "version": "1.0.0",
        "endpoints": {
            "websocket": "ws://127.0.0.1:8000/ws",
            "post_task": "POST /task",
            "get_workspace": "GET /workspace",
            "get_file": "GET /workspace/{file_path}",
            "get_messages": "GET /messages",
            "health_check": "GET /health"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

# Run with: uvicorn main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )
