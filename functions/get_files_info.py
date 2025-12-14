
import os

def get_files_info(working_dir,directory="."):
    try:
        working_dir_abs = os.path.abspath(working_dir)
        target_dir = os.path.normpath(os.path.join(working_dir_abs,directory))
        
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir])
        if not valid_target_dir == working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        lines = []
        for entry in os.listdir(target_dir):
            entry_path = os.path.join(target_dir,entry)
            size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            
            lines.append(
                f"- {entry}: file_size={size} bytes, is_dir={is_dir}"
            )
            
        return "\n".join(lines)
    
    except Exception as e:
        return f"Error: {e}"