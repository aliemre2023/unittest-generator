from modules.__init__ import *
import subprocess
import pyautogui
import os
import time
from modules.Debugger import debugger_file
from modules.LibrarySynchronizer import library_synchronizer_file

###########################################

def specialize_file(root, file, 
                    choose=1):
    if(choose == 0):
        return 0
    elif(choose == 1):
        return is_java_file(file) and is_service(root + file) and not is_dys(root+file)


determined_list = ["aServiceFile"]
def specialize_situation(test_file_path, src_file_name, determined_list, 
               choose=0):
    # Prepare unit-test for
    if(choose == 0):
        # nothing
        return 0
    elif(choose == 1):
        # all service files
        return 1
    elif(choose == 2):
        # only empty files
        return is_file_empty(test_file_path)
    elif(choose == 3):
        # spessific list
        return src_file_name in determined_list
    
    else:
        raise ValueError("Wrong secialization type")
    

def prompter(prompts, file):
    version = 1
    prompts = []

    Java = "JavaSE-1.7"

    prompt1 = ""
    prompt1 += f"prepare unit test in {Java} for {file}."
    prompt1 += f"main class name should be {file}_v{version}_Test."
    prompt1 += f"Take consider https://www.example.com"
    prompt1.append(prompt1)
    version += 1

    return prompts

#############################################

def prompt_maker(root, file, output):
    prompts = []
    prompts = prompter(prompts ,file)

    j = 0
    while(j < len(prompts)):
        prompt = prompts[j]
        j += 1

        if(specialize_file(root, file)): # dys file should not consider
            # Construct full paths for source and test files
            src_file_path = os.path.join(root, file)
            base_name, ext = os.path.splitext(file)
            test_file_path = os.path.join(root.replace("src", "test"), base_name + f"_v{j}_" + "Test" + ext)

            # Create test path if it doesn't exist
            if not os.path.exists(test_file_path):
                folder_path_list = test_file_path.split("/")[:-1]
                folder_path = "/".join(folder_path_list)
                os.makedirs(folder_path, exist_ok=True)

                with open(test_file_path, "a") as new_file:
                    pass
            
            # Spessific file arrange
            if(specialize_situation(test_file_path=test_file_path, src_file_name=src_file_path, determined_list=determined_list)):
                
                print(f"Processing {file}...")
                output.write(f"{beautiful_second()} - {base_name} is processing version-{j}...\n")

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

                # Library synchronizer
                library_synchronizer_file(test_file_path)