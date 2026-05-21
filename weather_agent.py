from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
def get_weather(city:str):
    print("< Tool Called:get_weather",city)
    url= f"https://wttr.in/{city}?format=%C+%t"
    response=requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

available_tools ={
    "get_weather":{
        "fn":get_weather,
        "description":"takes a city name as an input and returns the current weather for the city"
    }
}

system_prompt = """
You are an helpfull At Assistant who is specialized in resolving user query.
You work on start , plan , action , observe mode.
For the given user query and available tools, plan the step by step execution, based on the planning,
select the relevant tool from the available  tool. and based on the tool selection you perform an action to  call the tool wait for the observation and based on the observation from the tool call resolve the user query.

Rules:
- Follow the Output JSON Format.
- Always perform one step at a time and wait for next input
- Carefully analyse the user query

Output JSON Format:
{{
"step":"string",
"content":"string",
"function":"The name of function if the step is action",
"input":"The input parameter for the function",
}}

Available Tools:
- get_weather:Takes a city name as an input and returns the current weather for the city

Example:
User Query: What is the weather of new york?
Output:{{"step":"plan","content":"The user is intereseted inn weather data of new york"}}
Output:{{"step":"plan","content":"From the available tools I should call get_weather"}}
Output:{{"step:"action","function":"get_weather","input":"new york"}}
Output:{{"step:"observe","output":"12 Degree Cel"}}
Output:{{"step:"output","content":"The weather for new york seems to be 12 degress."}}
"""

messages=[
    {"role":"system","content":system_prompt}
]

user_query=input("> ")
messages.append({"role":"user","content":user_query})

while True:
    response=client.chat.completions.create(
        model="openai/gpt-oss-20b",
        response_format={"type":"json_object"},
        messages=messages
    )

    parsed_output=json.loads(response.choices[0].message.content)

    messages.append({"role":"assistant","content":json.dumps(parsed_output)})

    if parsed_output.get("step")=="plan":
         print(f"🧠:{parsed_output.get("content")}")
         continue
    
    if parsed_output.get("step")=="action":
        tool_name=parsed_output.get("function")
        tool_input=parsed_output.get("input")

        if available_tools.get(tool_name,False) !=False:
            output=available_tools[tool_name].get("fn")(tool_input)
            messages.append({"role":"assistant","content":json.dumps({"step":"observe","output": output})})
            continue

    if parsed_output.get("step")=="output":
        print(f"🤖:{parsed_output.get("content")}")
        break









# response = client.chat.completions.create(
#     model="openai/gpt-oss-120b",
#     response_format={"type":"json_object"},
#     messages=[
#          {"role":"system","content":system_prompt},
#          {"role":"user","content":"What is the current weather of delhi?"},
#          {"role":"assistant","content":json.dumps({"step":"plan","content":"User wants the current weather information for Delhi."})},
#          {"role":"assistant","content":json.dumps({"step":"plan","content":"From the available tools I should call get_weather"})},
#          {"role":"assistant","content":json.dumps({"step":"action","function":"get_weather","input":"Delhi"})},
#          {"role":"assistant","content":json.dumps({"step":"observe","content":"31 degree Celsius"})}
#     ]
# )

# print(response.choices[0].message.content)   