import os

WORKSPACE_ROOT = "/Users/bipin/programming/projects/AI office System/ai-office/workspace"

def file_writer(file_path, content):
    """Writes content to a file in the workspace."""
    full_path = os.path.join(WORKSPACE_ROOT, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    return f"File written successfully to {file_path}"

def file_reader(file_path):
    """Reads content from a file in the workspace."""
    full_path = os.path.join(WORKSPACE_ROOT, file_path)
    if not os.path.exists(full_path):
        return f"Error: File {file_path} does not exist."
    with open(full_path, "r") as f:
        return f.read()

def directory_lister(dir_path=""):
    """Lists files in a directory within the workspace."""
    full_path = os.path.join(WORKSPACE_ROOT, dir_path)
    if not os.path.exists(full_path):
        return f"Error: Directory {dir_path} does not exist."
    return "\n".join(os.listdir(full_path))
