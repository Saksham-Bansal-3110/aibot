import os

def write_file(working_dir, file_path, content):
    try: 
        #Resolve absolute working directory
        working_dir_abs = os.path.abspath(working_dir)
        
        #Build and normalize target file path
        target_path = os.path.normpath(os.path.join(working_dir_abs,file_path))
        
        #Ensure target path is within working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_path])
        if not valid_target_dir == working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        #Ensure parent directory exists
        parent_dir = os.path.dirname(target_path)
        if parent_dir:
            os.makedirs(parent_dir,exist_ok=True)
            
        #Write (overwrite) contents in file
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {e}"