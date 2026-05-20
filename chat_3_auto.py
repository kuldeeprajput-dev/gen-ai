from dotenv import load_dotenv
from openai import OpenAI
import json
import os
load_dotenv()


client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

system_prompt="""
You are and Ai assistant who is expert in breaking down complex problem's and then resolve the user query 
For the given user input analyze the input and break down the problem step by the step atleast think 5,6 step  on how to solve the problem before solving it down.
The steps are you gett a user input, you analyze , you think , you again think for serveral time and then return output with explanationl and the finally you validate the output as will before giving finale resultl.

Follow the steps is sequence that is "analyze","think","output","validate","result"

Rules:
1.Follow the strict JSON output as per Output schema.
2.Always perform one step at a time and wait for nextt input
3.Carefully analyze the user query

Output Format:
{{step:"string",content:"string"}}

Example:
Input: What is 2 + 2.
Output :{{step:"analyze",content:"Alright ! The user is intersted in maths query and he is asking for basic arthematic operations}}
Output:{{step:"think",content:"To perform the addition i must go from left to right and and all the operands"}}
Output:{{step:"output",content:"4"}}
Output:{{step:"validate,content:"seems like 4 is correct ans for 2 +2"}}
Output:{{step:"result",content:"2 + 2 = 4 and that is calculated by adding all numbers"}}
"""



messages=[
 {"role":"system","content":system_prompt},
]

query = input(">")
messages.append({"role":"user","content":query})


while True:
    response = client.chat.completions.create(
    model="openai/gpt-oss-120b",    
    response_format={"type":"json_object"},
    messages=messages
    )
    parsed_response=json.loads(response.choices[0].message.content)
    messages.append({"role":"assistant","content":json.dumps(parsed_response)})

    
    if parsed_response.get("step") != "output":
       print(f"🧠:{parsed_response.get("content")}")
       continue

    print(f"🤖:{parsed_response.get("content")}")
    break


