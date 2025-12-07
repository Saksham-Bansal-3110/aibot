import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY environment varaiable not found in .env file or system environment.")

client = genai.Client(api_key=api_key)

model_name = "gemini-2.5-flash"
prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

try:
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    if response.usage_metadata is None :
        raise RuntimeError("This is a failed API request.")
    
    prompt_token = response.usage_metadata.prompt_token_count
    candidate_token = response.usage_metadata.candidates_token_count
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {prompt_token}")
    print(f"Response tokens: {candidate_token}")
    print(f"Response: {response.text}")

except Exception as e:
    print(f"An error occured during content generation: {e}")
    
