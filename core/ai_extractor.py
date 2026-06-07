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
            - CRITICAL: If the text does NOT describe a specific human individual (e.g., it is a marketing paragraph, an event description, a panel title, a photo gallery, or a sponsor ad), you MUST return perfectly empty strings "" for ALL fields.
            - If a field cannot be determined, you MUST return a perfectly empty string "". Do NOT return "nan", "null", "N/A", or "None".
            - "company": MUST be a valid corporate or organizational entity (e.g., Pfizer, Moderna, Harvard University).
            - "job_title": MUST be the role or profession (e.g., Director, CEO, Scientist).
            - If a string describes a department, division, or scientific area (e.g., "Discovery & Preclinical Development", "Department of Oncology", "Market Access Strategy"), IT IS NOT A COMPANY. Combine it with the "job_title".
            - "summary" should be a biography paragraph. Strip out any spam, 404 errors, or marketing boilerplate (e.g., event locations, "Next in Series", etc.).
            
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
