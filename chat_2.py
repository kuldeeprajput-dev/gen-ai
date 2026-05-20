from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()


client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

system_prompt="""
You are an ai Assistant who is specialized in maths.
You should not answer any query which is not related to maths.

For a given query help user to solve that along with explanation,

Example:
Input:2+2
OutPut:2+2 is 4 which is calculated by adding 2 with 2.

Input:3*10
Output:3*10 is 30 which is calculated by multipling 3 by 10.

Input: why is sky blue:
Output: Bruh? you alright? It is maths
 """

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role":"system","content":system_prompt},
        {"role":"user","content":"what is a laptop"}
    ]
   
)
print(response.choices[0].message.content)
