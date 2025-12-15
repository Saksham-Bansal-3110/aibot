from functions.get_file_content import get_file_content
from config import MAX_FILE_CHARS
from prompts import system_prompt

def run_test():
    result = get_file_content("calculator","lorem.txt")
    
    #Ensure result is a string
    if not isinstance(result,str):
        print("Error: get_file_content did not return a string")
        return
    
    #Check truncation
    if len(result) <= MAX_FILE_CHARS:
        print("Error: file was not truncated as expected")
        return
    
    truncation_message = f'[...File "lorem.txt" turnates at {MAX_FILE_CHARS} characters]'
    
    if not result.endswith(truncation_message):
        print("Error: truncation message missing or incorrect")
        return
    
    print("Truncation test passed")
    print(f"Returned length: {len(result)}")
    print(f"Truncation message found at end")
    
    result = get_file_content("calculator","main.py")
    print(result)
    result = get_file_content("calculator","pkg/calculator.py")
    print(result)
    result = get_file_content("calculator","/bin/cat")
    print(result)
    result = get_file_content("calculator","pkg/does_not_exist.py")
    print(result)
    
    
if __name__ == "__main__":
    run_test()    