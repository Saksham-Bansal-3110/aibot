import os 
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_dir,file_path, args=[]):
    try:
        #Resolve absolute paths
        working_dir_abs = os.path.abspath(working_dir)
        target_path = os.path.normpath(os.path.join(working_dir_abs,file_path))
        
        #Check if file is outside the working directory
        valid_path = os.path.commonpath([working_dir_abs, target_path])
        if not valid_path == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        #Check if file exist
        if not os.path.exists(target_path):
            return f'Error: File "{file_path}" not found.'
        
        #Check if file is a python file
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        #Run the python file
        completed_process = subprocess.run(
            ["python",target_path, *args],
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output_parts = []
        
        if completed_process.stdout:
            output_parts.append(f"STDOUT: {completed_process.stdout}")
            
        if completed_process.stderr:
            output_parts.append(f"STDERR: {completed_process.stderr}")
            
        if completed_process.returncode != 0:
            output_parts.append(f"Process exicted with code {completed_process.returncode}")
        
        if not output_parts:
            return "No output produced"
        
        return"\n".join(output_parts)
        
    
    except subprocess.TimeoutExpired:
        return "Error: Execution timed out after 30 seconds."
    
    except Exception as e:
        return f'Error: executing Python file: {e}'
  
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