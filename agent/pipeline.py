from .ingestion import clone_repo, list_python_files
from .parser import parse_file
from .reviewer import review_chunk
from typing import List, Dict, Any

def run_review_pipeline(repo_url: str, progress_callback=None) -> List[Dict[str, Any]]:
    """Orchestrates the entire code review pipeline."""
    try:
        # Step 1: Ingestion
        if progress_callback:
            progress_callback("Cloning repository...", 10)
        repo_path = clone_repo(repo_url)
        
        if progress_callback:
            progress_callback("Listing Python files...", 20)
        py_files = list_python_files(repo_path)
        
        # Step 2: Parsing
        if progress_callback:
            progress_callback(f"Parsing {len(py_files)} files...", 40)
            
        all_chunks = []
        for file in py_files:
            # Skip files > 500 lines for safety as per requirements
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                if len(lines) > 500:
                    print(f"Skipping {file} (too large: {len(lines)} lines)")
                    continue
            chunks = parse_file(file)
            all_chunks.extend(chunks)
            
        # Step 3: Review
        if progress_callback:
            progress_callback(f"Reviewing {len(all_chunks)} chunks...", 60)
            
        reviews = []
        for i, chunk in enumerate(all_chunks):
            if progress_callback:
                progress = 60 + int(40 * (i / max(len(all_chunks), 1)))
                progress_callback(f"Reviewing chunk {i+1}/{len(all_chunks)}: {chunk['name']}", progress)
            
            review = review_chunk(chunk)
            if review:
                reviews.append(review)
                
        if progress_callback:
            progress_callback("Review complete!", 100)
            
        return reviews
    except Exception as e:
        raise Exception(f"Pipeline failed: {str(e)}")
