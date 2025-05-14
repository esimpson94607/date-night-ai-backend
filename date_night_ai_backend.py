from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Profile(BaseModel):
    firstName: str
    lastName: str
    age: int
    sex: str
    email: str
    location: str
    interests: str
    needsSitter: bool
    spouseFirstName: str
    spouseLastName: str
    spouseAge: int
    spouseSex: str
    spouseEmail: str

def generate_ideas_with_openai(profile: dict) -> List[str]:
    prompt = f"""
    Create 3 detailed and creative monthly date night ideas for a couple based on:
    - Location: {profile['location']}
    - Interests: {profile['interests']}
    - Needs babysitter or pet sitter: {profile['needsSitter']}
    - Ages: {profile['age']} and {profile['spouseAge']}

    Each idea should be 1–2 sentences, vivid and practical for their city.
    Use varied tones: romantic, playful, or relaxing.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }],
        temperature=0.85
    )
    return response.choices[0].message.content.strip().split("\n")

@app.post("/get-date-ideas")
async def get_date_ideas(profile: Profile):
    try:
        suggestions = generate_ideas_with_openai(profile.dict())
        return { "suggestions": suggestions }
    except Exception as e:
        return { "error": str(e), "suggestions": [
            "🌇 Rooftop tapas & jazz night with skyline views.",
            "🌿 A guided sunset hike followed by gourmet food truck dinner.",
            "🎭 Local improv show and dessert at a late-night cafe."
        ]}