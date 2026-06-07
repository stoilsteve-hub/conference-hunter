import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

texts = [
    """Zach Zhu
Chief Technology Officer Innorna
Zach is Chief Technology Officer at Innorna, leading the company’s CMC division. With over 15 years in biotech and biopharma, he brings deep expertise in process development, technology transfer, and manufacturing. Previously, he was Senior Director and Head of Drug Product at Iveric Bio (an Astellas company). He also held roles at Moderna, Biogen, and Bristol Myers Squibb earlier in his career. Zach earned his Ph.D. in Biochemistry from the University of Notre Dame, and his M.S. and B.S. in Chemistry from Nanjing University.""",
    """Cécile Bauche
Company: C4bio
Job title: Chief Executive Officer
Seminars:
Identifying Bioproduction Challenges to Accelerate Therapies into the Clinic 4:30 pm"""
]

prompt_template = """
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
{text}
"""

for text in texts:
    prompt = prompt_template.replace("{text}", text)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    print("AI OUTPUT:")
    print(response.text)

