import os
import json
from typing import Dict, Any, Optional
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def review_chunk(chunk: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Sends a code chunk to LLM for review."""
    prompt = f"""
    You are an expert AI code reviewer. Review the following Python {chunk['type']} named `{chunk['name']}` from `{chunk['file_path']}`.
    Identify if there are any issues. If there are no issues, return null.
    If there are issues, return a JSON object exactly matching this schema:
    {{
      "issue": "string — what the problem is",
      "suggestion": "string — how to fix it",
      "severity": "low | medium | high",
      "category": "security | performance | style | correctness | maintainability",
      "confidence": 0-100 (integer)
    }}
    
    Code:
    ```python
    {chunk['code']}
    ```
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI code reviewer. Always respond with valid JSON or null."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if not content or content.strip().lower() == "null":
            return None
            
        review_data = json.loads(content)
        
        # Validate schema loosely
        if "issue" in review_data and "suggestion" in review_data:
            review_data['chunk'] = chunk
            return review_data
        return None
    except Exception as e:
        print(f"Error reviewing chunk {chunk['name']}: {e}")
        return None
