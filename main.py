import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_files_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
        
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    function_name = function_call_part.name
    
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error":f"Unknown function: {function_name}"},
                )
            ],
        )
    
    #Copy args so we don't mutate the original
    function_args = dict(function_call_part.args or {})
    
    #manually inject working directory
    function_args["working_directory"] = "./calculator"
    
    #Call the function and capture the result
    result = function_map[function_name](**function_args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result":result},
            )
        ],
    )
        
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
    function_declarations=[schema_get_files_info,schema_write_file,schema_get_files_content,schema_run_python_file],
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
    function_call_result = []
    
    for candidate in response.candidates:
        content = candidate.content
        if not content or not content.parts:
            continue
        
        for part in content.parts:
            if part.text:
                print(f"Response: {part.text}")
            
            if part.function_call:
                #call the function via abstraction
                function_call_result = call_function(
                    part.function_call,
                    verbose=args.verbose,
                )
                
                #validate tool response
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                    or not function_call_result.parts[0].function_response.response
                ):
                    raise RuntimeError(
                        "Fatal error: function did not return a valid tool response"
                    )
                
                #store the tool response part for later use
                function_call_result.append(function_call_result.parts[0])
                
                #verbose logging
                if args.verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )
               

except Exception as e:
    print(f"An error occured during content generation: {e}")
    
