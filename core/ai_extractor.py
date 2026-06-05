import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize the Gemini Client
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
else:
    print("WARNING: GEMINI_API_KEY not found in .env")
    client = None

def extract_speaker_info(raw_text):
    if not raw_text or not raw_text.strip() or not client:
        return {"name": "", "job_title": "", "company": "", "summary": ""}
        
    try:
        prompt = f"""
        Extract the following information about a speaker from the given text.
        Return ONLY a raw JSON object with the exact keys:
        "name", "job_title", "company", "summary".
        
        Rules:
        - If a field is missing, return an empty string "".
        - "company" should be the actual corporate entity. Do not include academic departments, labs, or centers as the company. If it's an academic department, put it in "job_title" instead.
        - "summary" should be a biography paragraph. Strip out any spam, 404 errors, or marketing boilerplate (e.g., event locations, "Next in Series", etc.).
        - "job_title" should contain their role (e.g. Director, Scientist, etc).
        
        Text to analyze:
        {raw_text}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        # Parse the JSON response
        data = json.loads(response.text)
        
        return {
            "name": str(data.get("name", "")).strip(),
            "job_title": str(data.get("job_title", "")).strip(),
            "company": str(data.get("company", "")).strip(),
            "summary": str(data.get("summary", "")).strip()
        }
        
    except Exception as e:
        print(f"AI Extraction failed: {e}")
        # Return fallback empty structure
        return {"name": "", "job_title": "", "company": "", "summary": ""}
