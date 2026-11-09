import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function


parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt for the chatbot")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]


load_dotenv()
api_key=os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("api key is not set")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
for _ in range(20):
    response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
    temperature=0.7,  # Optional: adjust the creativity of the response
)


    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)
            messages.append(result_message)
            if not result_message["content"]:
                raise Exception("Function returned empty content")
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print(message.content)
        break
else:
    print("Agent reached the maximum number of interactions")



if response.usage is None:
    raise RuntimeError("Failed to get usage information")
print(response.choices[0].message.content)
if args.verbose:
    print("User prompt: ", args.user_prompt)
    print("Prompt tokens:", response.usage.prompt_tokens)
    print("Response tokens:", response.usage.completion_tokens)
    print("Response:")
    
   