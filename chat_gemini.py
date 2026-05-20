from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response =  client.models.generate_content(
    model='gemini-2.5-flash', contents='Tell me a story in 300 words.'
)

print(response.text)