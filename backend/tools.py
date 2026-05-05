import os
from config import WORKSPACE_ROOT

def file_writer(file_path: str, content: str) -> str:
    """Writes content to a file in the workspace."""
    try:
        full_path = os.path.join(WORKSPACE_ROOT, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Written {len(content)} chars to {file_path}"
    except Exception as e:
        return f"❌ Error writing {file_path}: {str(e)}"

def file_reader(file_path: str) -> str:
    """Reads content from a file in the workspace."""
    try:
        full_path = os.path.join(WORKSPACE_ROOT, file_path)
        if not os.path.exists(full_path):
            return f"❌ File not found: {file_path}"
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"✅ Read {len(content)} chars from {file_path}:\n\n{content}"
    except Exception as e:
        return f"❌ Error reading {file_path}: {str(e)}"

def directory_lister(dir_path: str = "") -> str:
    """Lists files in a directory within the workspace."""
    try:
        full_path = os.path.join(WORKSPACE_ROOT, dir_path)
        if not os.path.exists(full_path):
            return f"❌ Directory not found: {dir_path}"
        items = os.listdir(full_path)
        files = [f for f in items if os.path.isfile(os.path.join(full_path, f))]
        dirs = [d for d in items if os.path.isdir(os.path.join(full_path, d))]
        
        result = f"📁 Directory: {dir_path}\n"
        if dirs:
            result += f"\nFolders: {', '.join(dirs)}"
        if files:
            result += f"\nFiles: {', '.join(files)}"
        return result
    except Exception as e:
        return f"❌ Error listing {dir_path}: {str(e)}"
