from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

text = "TJ Cradick\nPrincipal & Fractional CSO"

prompt = f"""
Extract the following information about a speaker from the given text.
Return ONLY a raw JSON object with the exact keys:
"name", "job_title", "company", "summary".

Rules:
- If a field cannot be determined, you MUST return a perfectly empty string "". Do NOT return "nan", "null", "N/A", or "None".
- "company": MUST be a valid corporate or organizational entity (e.g., Pfizer, Moderna, Harvard University).
- "job_title": MUST be the role or profession (e.g., Director, CEO, Scientist, CSO).
- If a string describes a department, division, or scientific area (e.g., "Discovery & Preclinical Development", "Department of Oncology", "Market Access Strategy"), IT IS NOT A COMPANY. Combine it with the "job_title".
- "summary" should be a biography paragraph. Strip out any spam or marketing boilerplate.

Text to analyze:
{text}
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)

print(response.text)
