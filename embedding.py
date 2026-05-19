from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
     api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

text = "Eiffel Tower is in paris and is a famous landmark, it is 324 meters tall"

response = client.responses.create(
    input=text,
    model="openai/gpt-oss-120b",
)

print("Vector Embeddings", response)