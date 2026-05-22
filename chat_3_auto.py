from dotenv import load_dotenv
from openai import OpenAI
import json
import os

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and solving user queries step-by-step.

For every user query:
1. Analyze the problem carefully
2. Think step-by-step multiple times before solving
3. Generate the output
4. Validate the output
5. Return the final result with explanation

You must strictly follow this sequence:
"analyze" -> "think" -> "output" -> "validate" -> "result"

Rules:
1. Always return ONLY ONE valid JSON object
2. Never return markdown
3. Never return text outside JSON
4. Always follow the exact output schema
5. Perform only ONE step at a time
6. Carefully analyze the user query
7. Output must always be valid parsable JSON

Output Format:
{
    "step":"string",
    "content":"string"
}

Example:

Input:
What is 2 + 2?

Output:
{
    "step":"analyze",
    "content":"The user is asking a basic arithmetic addition problem."
}

Output:
{
    "step":"think",
    "content":"To solve the expression I should add 2 and 2 together."
}

Output:
{
    "step":"output",
    "content":"4"
}

Output:
{
    "step":"validate",
    "content":"The calculation is correct because adding 2 and 2 results in 4."
}

Output:
{
    "step":"result",
    "content":"2 + 2 = 4"
}
"""

messages = [
    {"role": "system", "content": system_prompt},
]

query = input("> ")

messages.append({
    "role": "user",
    "content": query
})

while True:

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        response_format={"type": "json_object"},
        messages=messages
    )

    raw_response = response.choices[0].message.content

    try:
        parsed_response = json.loads(raw_response)

    except json.JSONDecodeError:
        print("❌ Invalid JSON received")
        print(raw_response)
        break

    messages.append({
        "role": "assistant",
        "content": json.dumps(parsed_response)
    })

    step = parsed_response.get("step")
    content = parsed_response.get("content")

    if step in ["analyze", "think", "validate"]:
        print(f"🧠: {content}")
        continue

    elif step == "output":
        print(f"📤: {content}")
        continue

    elif step == "result":
        print(f"🤖: {content}")
        break

    else:
        print("❌ Unknown step received")
        print(parsed_response)
        break