import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY environment varaiable not found in .env file or system environment.")

parser = argparse.ArgumentParser(description="Send a prompt to Gemini API")
parser.add_argument("user_prompt",type=str,help="User prompt to sent to the model")
parser.add_argument("--verbose",action="store_true",help="Enable verbose output")

args = parser.parse_args()

client = genai.Client(api_key=api_key)

model_name = "gemini-2.5-flash"
prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

messages = [types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]

available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)

try:
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
            temperature=0,
            top_p=0.95,
            top_k=20,
        ),
    )
    if response.usage_metadata is None :
        raise RuntimeError("This is a failed API request.")
    
    prompt_token = response.usage_metadata.prompt_token_count
    candidate_token = response.usage_metadata.candidates_token_count
    if args.verbose:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {prompt_token}")
        print(f"Response tokens: {candidate_token}")
        
    #Print normal text response (if any)    
    if response.text:
        print(f"Response: {response.text}")
        
    #Check for function calls
    for candidate in response.candidates:
        content = candidate.content
        if not content or not content.parts:
            continue
        
        for part in content.parts:
            if part.text:
                print(f"Response: {part.text}")
            
            if part.function_call:
                print(f"Calling function: {part.function_call.name}({part.function_call.args})")

except Exception as e:
    print(f"An error occured during content generation: {e}")
    
