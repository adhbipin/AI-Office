import os

# Workspace path — relative to where the backend is run from
WORKSPACE_ROOT = os.path.join(os.getcwd(), "workspace")

# Create workspace directories if they don't exist
os.makedirs(os.path.join(WORKSPACE_ROOT, "frontend"), exist_ok=True)
os.makedirs(os.path.join(WORKSPACE_ROOT, "backend"), exist_ok=True)
os.makedirs(os.path.join(WORKSPACE_ROOT, "devops"), exist_ok=True)
os.makedirs(os.path.join(WORKSPACE_ROOT, "logs"), exist_ok=True)

# Database path
DB_PATH = os.path.join(WORKSPACE_ROOT, "ai_office.db")

# Ollama models (change these to match what you've pulled with `ollama pull`)
MODELS = {
    'pm':       'llama3:8b',
    'ui':       'llama3:8b',
    'frontend': 'codellama:latest',
    'backend':  'codellama:latest',
    'qa':       'llama3:8b',
    'devops':   'llama3:8b',
}

# Server config
HOST = "127.0.0.1"
PORT = 8000

print(f"✅ Workspace path: {WORKSPACE_ROOT}")
print(f"✅ Database path: {DB_PATH}")
