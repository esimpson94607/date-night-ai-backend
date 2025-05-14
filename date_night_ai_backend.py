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
    spouseInterests: str

def generate_itineraries(profile: dict) -> List[str]:
    prompt = f"""
    Generate 3 real-world, location-specific date night itineraries for a couple in {profile['location']}.
    Use these shared interests only: {profile['interests']}, {profile['spouseInterests']}.

    Each itinerary must:
    - Include a title (e.g., "Sushi & Sunset")
    - Be realistic and tailored to the city
    - Include 2–3 specific steps or stops in the order they'll happen
    - Clearly state the total duration ("2 hours" or "4–5 hours")
    - Only use real places/events
    - Include working links to Yelp, Google Maps, or official sites

    Format:
    1. [Title] – [Duration]
    [Step 1 description]
    [Step 2 description]
    [Links]

    Return each on its own line.
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
        suggestions = generate_itineraries(profile.dict())
        return { "suggestions": suggestions }
    except Exception as e:
        return { "error": str(e), "suggestions": [
            "1. Sushi & Sunset – 2 hours\nDinner at Ozumo followed by a sunset stroll through the San Jose Municipal Rose Garden.\nhttps://ozumo.com | https://goo.gl/maps/rose-garden",
            "2. Jazz & Art Night – 4–5 hours\nVisit San Jose Museum of Art, then enjoy cocktails and live music at Cafe Stritch.\nhttps://sjmusart.org | https://cafestritch.com",
            "3. Outdoor & Ramen – 2 hours\nShort hike at Alum Rock Park followed by ramen at Ramen Nagi.\nhttps://goo.gl/maps/alum-rock | https://ramennagiusa.com"
        ]}