from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()


client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role":"user","content":"what is 2+2*8"}
    ]
   
)
print(response.choices[0].message.content)
