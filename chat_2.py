from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

system_prompt = """
You are an AI Assistant specialized in mathematics.

Rules:
1. Answer ONLY math-related questions.
2. If the query is not related to math, politely refuse.
3. Always explain the solution clearly.
4. Keep responses short and accurate.

Examples:

Input: 2 + 2
Output:
2 + 2 = 4.
This is calculated by adding 2 and 2.

Input: 3 * 10
Output:
3 * 10 = 30.
This is calculated by multiplying 3 by 10.

Input: why is the sky blue?
Output:
I can only help with mathematics-related questions.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "what is a laptop"}
    ]
)

print(response.choices[0].message.content)