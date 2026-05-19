import os
import tempfile
from git import Repo
from pathlib import Path
from typing import List

def clone_repo(repo_url: str) -> str:
    """Clones a GitHub repository to a temporary directory."""
    try:
        temp_dir = tempfile.mkdtemp(prefix="ai_code_reviewer_")
        print(f"Cloning {repo_url} into {temp_dir}...")
        Repo.clone_from(repo_url, temp_dir)
        return temp_dir
    except Exception as e:
        raise Exception(f"Failed to clone repository: {str(e)}")

def list_python_files(repo_path: str) -> List[str]:
    """Lists all .py files in the given directory."""
    python_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files
