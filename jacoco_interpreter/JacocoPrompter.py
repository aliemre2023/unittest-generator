import os
import sys
sys.path.append("..")
from modules.__init__ import *
import subprocess
import time
import pyautogui
from modules.Debugger import debugger_file

jacoco_outputs = "C:/path/to/unittest-generator/jacoco_interpreter/jacoco-coverage-lines/"

def should_develop(jacoco_NC_file_path):
    jacoco_file = open(jacoco_NC_file_path, "r", encoding="utf-8")
    jacoco_lines = jacoco_file.readlines()
    jacoco_file.close()

    if(len(jacoco_lines) > 10):
        return True
    else:
        return False

def jacoco_prompter(root, file, output):
    base_name, ext = os.path.splittext(file)
    test_file_name = base_name + "_vJ_Test"
    
    prompt = ""
    jacoco_NC_path = ""

    pure_file = file.split(".")[0]
    print(pure_file)

    for j_root, j_dirs, j_files in os.walk(jacoco_outputs):
        if(pure_file in j_root):
            if(j_root[-1] != "/"): j_root += "/"
            jacoco_NC_path = j_root + "/nc.txt"
        
    print(jacoco_NC_path)
    if os.path.exists(jacoco_NC_path):
        with open(jacoco_NC_path, "r", encoding="utf-8") as file_r:
            file_content = ""
            lines = file_r.readlines()
            if(len(lines) > 50):
                for line in lines[0:50]:
                    file_content += line[:-1].strip() + "--"
            else:
                for line in lines:
                    file_content += line[:-1].strip() + "--"
            file_content = restrict_encode(file_content, allowed_characters)

            prompt += f" prepare unit test for {file}."
            prompt += file_content.decode("utf-8")
            prompt += " Especially cover those lines."

        print(file)
        
        if(is_java_file(file) and is_service(root + file) and not is_dys(root+file)): # dys file should not consider
            # Construct full paths for source and test files
            src_file_path = os.path.join(root, file)
            base_name, ext = os.path.splitext(file)
            test_file_path = os.path.join(root.replace("src", "test"), base_name + f"_vJ_" + "Test" + ext)

            # Create test path if it doesn't exist
            if not os.path.exists(test_file_path):
                folder_path_list = test_file_path.split("/")[:-1]
                folder_path = "/".join(folder_path_list)
                os.makedirs(folder_path, exist_ok=True)

                with open(test_file_path, "a") as new_file:
                    pass
            
            # Spessific file arrange
            if(is_java_file(file) and is_service(root + file) and not is_dys(root + file)):
                
                print(f"Processing {file}...")
                output.write(f"{beautiful_second()} - {base_name} is processing jacoco version...\n")

                # Open src file in Intellij
                process_file("idea", src_file_path)

                # Select whole src file for better prompt
                pyautogui.hotkey("ctrl", "a")
                
                # Open Copilot Chat ith shortcut
                pyautogui.hotkey("ctrl", "shift", "alt", "5")
                time.sleep(2)

                # Prompt for copilot chat
                pyautogui.write("/test")
                time.sleep(0.25)
                pyautogui.press("enter")
                pyautogui.write(prompt)
                pyautogui.press("enter")
                time.sleep(40) # wait for result

                '''
                Assumption : 
                    Intellij window should be in the rightmost and full width
                    It may be developed but I didn't find any shortcut to copy result 
                '''

                # Copy the given suggestion
                pyautogui.rightClick(1800, 500)
                time.sleep(1)
                pyautogui.click(1800, 500)

                # Open test file in Intellij
                process_file("idea", test_file_path)

                # Overwrite, paste copied solution
                pyautogui.hotkey("ctrl", "a")
                time.sleep(0.1)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(0.1)
                pyautogui.hotkey("ctrl", "s")
                time.sleep(2)

                # Close the current service file and its test
                pyautogui.hotkey("ctrl", "f4")
                time.sleep(1)
                pyautogui.hotkey("ctrl", "f4")

                # Clean the copyboard
                copy_to_clipboard("")

                # Clean copilot chat for new conversation
                pyautogui.hotkey("ctrl", "shift", "alt", "6")
            
                # Debug the file
                debugger_file(test_file_path)

def restrict_encode(text, allowed_characters):
    # Filter out unwanted characters
    filtered_text = ''.join(c for c in text if c)

    # Encode the filtered text in UTF-8
    encoded_text = filtered_text.encode("utf-8")

    return  encoded_text

allowed_characters = set(
    'abcdefghijklmnoprstuvxyz'
    'ABCDEFGHIJKLMNOPRSTUVXYZ'
    '0123456789'
    ' .,!?"\'()&=|;[]{}%\\-_*'
)