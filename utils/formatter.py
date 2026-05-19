from typing import List, Dict, Any

def format_reviews_as_markdown(reviews: List[Dict[str, Any]]) -> str:
    """Formats a list of reviews into a Markdown string."""
    if not reviews:
        return "No issues found! Great job."
        
    md = "# Code Review Report\n\n"
    
    for i, review in enumerate(reviews):
        chunk = review.get('chunk', {})
        md += f"## Issue {i+1}: {chunk.get('name', 'Unknown')} ({chunk.get('file_path', '')})\n"
        md += f"**Severity:** {review.get('severity', 'Unknown')} | "
        md += f"**Category:** {review.get('category', 'Unknown')} | "
        md += f"**Confidence:** {review.get('confidence', 0)}%\n\n"
        md += f"**Issue:** {review.get('issue', '')}\n\n"
        md += f"**Suggestion:** {review.get('suggestion', '')}\n\n"
        md += "---\n\n"
        
    return md
