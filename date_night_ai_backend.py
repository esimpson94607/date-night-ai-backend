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

def generate_strict_interest_ideas(profile: dict) -> List[str]:
    prompt = f"""
    Generate 3 creative, real-world date night ideas for a couple in {profile['location']}.
    
    Only use the following interests to inspire the date ideas: {profile['interests']}.
    Do not include any suggestions that are unrelated to these interests.
    
    Each suggestion must:
    - Match at least one keyword from the interest list
    - Mention a real place, business, or event in the area
    - Include a brief 1–2 sentence description
    - End with a working URL (Yelp, Google Maps, or the official site)

    Output each idea as a numbered item, one per line.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }],
        temperature=0.8
    )
    return response.choices[0].message.content.strip().split("\n")

@app.post("/get-date-ideas")
async def get_date_ideas(profile: Profile):
    try:
        suggestions = generate_strict_interest_ideas(profile.dict())
        return { "suggestions": suggestions }
    except Exception as e:
        return { "error": str(e), "suggestions": [
            "1. Sushi at Ozumo – Sleek vibe with premium sashimi and sake flights. https://ozumo.com",
            "2. Hike at Alum Rock Park – A peaceful sunrise trail experience. https://goo.gl/maps/...",
            "3. Live jazz at Cafe Stritch – Downtown music & cocktails. https://cafestritch.com"
        ]}