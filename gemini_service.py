
# # gemini_service.py

# import os
# import json
# from dotenv import load_dotenv
# # import generativeai as genai

# from google import genai


# load_dotenv()

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# model = genai.GenerativeModel("models/gemini-2.5-flash")


# def generate_prd(text_input: str):
#     prompt = f"""
# You are a senior product manager.

# From the below conversation extract a PRD in STRICT JSON format.

# Return ONLY valid JSON.

# Format:
# {{
# "project_name": "",
# "date": "",
# "requirements": [],
# "team_tasks": [],
# "eta": "",
# "project_overview": []
# }}

# Rules:
# - If ETA date mentioned → return in DD/MM/YYYY
# - If not mentioned → assume 90 days
# - Requirements → bullet point array
# - Team tasks → split by roles if mentioned
# - Overview → array format

# Conversation:
# {text_input}
# """

#     response = model.generate_content(prompt)
    
#     try:
#         return json.loads(response.text)
#     except:
#         return {"error": "Invalid JSON returned", "raw_output": response.text}


# def transcribe_audio(audio_bytes):
#     audio_model = genai.GenerativeModel("models/gemini-2.5-flash-native-audio-latest")

#     response = audio_model.generate_content(
#         [
#             {"mime_type": "audio/wav", "data": audio_bytes},
#             "Transcribe this audio"
#         ]
#     )

#     return response.text





# gemini_service.py

import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Create client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-2.5-flash"
# AUDIO_MODEL = "models/gemini-2.5-flash-native-audio-latest"
AUDIO_MODEL = "models/gemini-2.5-flash"

# --------------------------------------------------
# GENERATE PRD JSON
# --------------------------------------------------

def generate_prd(text_input: str):

    prompt = f"""
You are a senior product manager.

From the below conversation extract a PRD in STRICT JSON format.

Return ONLY valid JSON.

Format:
{{
"project_name": "",
"date": "",
"requirements": [],
"team_tasks": [],
"eta": "",
"project_overview": []
}}

Rules:

- DO NOT generate project date.
- Only extract ETA if explicitly mentioned.

- Requirements → bullet point array
- Team tasks → split by roles if mentioned
- Overview → array format

Conversation:
{text_input}
"""

    # response = client.models.generate_content(
    #     model=MODEL_NAME,
    #     contents=prompt,
    #     config=types.GenerateContentConfig(
    #         temperature=0.3,
    #         response_mime_type="application/json"
    #     )
    # )




    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                    "date": {"type": "string"},
                    "requirements": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "team_tasks": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "eta": {"type": "string"},
                    "project_overview": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": [
                    "project_name",
                    "date",
                    "requirements",
                    "team_tasks",
                    "eta",
                    "project_overview"
                ]
            }
        )
    )




    try:
        return json.loads(response.text)
    except Exception:
        return {
            "error": "Invalid JSON returned",
            "raw_output": response.text
        }


# --------------------------------------------------
# TRANSCRIBE AUDIO
# --------------------------------------------------

def transcribe_audio(audio_bytes: bytes):

    response = client.models.generate_content(
        model=AUDIO_MODEL,
        contents=[
            types.Part.from_bytes(
                data=audio_bytes,
                mime_type="audio/wav"  # change if mp3 etc
            ),
            "Transcribe this audio clearly."
        ],
        config=types.GenerateContentConfig(
            temperature=0
        )
    )

    return response.text
