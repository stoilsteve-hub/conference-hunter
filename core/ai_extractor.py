import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
else:
    print("WARNING: GEMINI_API_KEY not found in .env")
    client = None

def extract_speaker_info(raw_text):
    if not raw_text or not raw_text.strip() or not client:
        return {"name": "", "job_title": "", "company": "", "summary": ""}
        
    import time
    max_retries = 6
    for attempt in range(max_retries):
        try:
            prompt = f"""
            Extract the following information about a speaker from the given text.
            Return ONLY a raw JSON object with the exact keys:
            "name", "job_title", "company", "summary".
            
            Rules:
            - AGGRESSIVELY EXTRACT DATA. Even if the text is messy, contains Wayback Machine garbage, marketing text, or event descriptions, FIND the speaker's name, title, company, and bio and extract them.
            - Do NOT reject the page unless there is absolutely zero human biographical data present.
            - If a specific field cannot be determined, return an empty string "" for that field only. Do NOT return "nan", "null", "N/A", or "None".
            - "company": Try to find a corporate or organizational entity.
            - "job_title": Try to find the role or profession.
            - "summary": Extract the biography paragraph. It's okay if it contains some conference jargon.
            
            Text to analyze:
            {raw_text}
            """
            
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            data = json.loads(response.text)
            
            return {
                "name": str(data.get("name", "")).strip(),
                "job_title": str(data.get("job_title", "")).strip(),
                "company": str(data.get("company", "")).strip(),
                "summary": str(data.get("summary", "")).strip()
            }
            
        except Exception as e:
            print(f"AI Extraction failed (Attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                delay = 2 ** (attempt + 2) 
                print(f"Waiting {delay} seconds before retry...")
                time.sleep(delay)
            else:
                return {"name": "", "job_title": "", "company": "", "summary": ""}
