import os
from config import MAX_FILE_CHARS
from google import genai
from google.genai import types

def get_file_content(working_dir, file_path):
    try: 
        #Resolve absolute working directory
        working_dir_abs = os.path.abspath(working_dir)
        
        #Build and normalize target file path
        target_path = os.path.normpath(os.path.join(working_dir_abs,file_path))
        
        #Ensure target path is within working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_path])
        if not valid_target_dir == working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        #Ensure target path is a regular file
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        #Read File contents
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        #Turnacate if necessary
        if len(content) > MAX_FILE_CHARS:
            content = (
                content[:MAX_FILE_CHARS]
                + f'\n[...File "{file_path}" turnates at {MAX_FILE_CHARS} characters]'
            )
            
        return content
        
    except Exception as e:
        return f"Error: {e}"

schema_get_files_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Writes the content of the files in a specified directory.",
    parameters=types.Schema(
        type = types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to get the contents of.",
            ),
        },
    ),
)