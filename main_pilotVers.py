import os
import subprocess
import time
import pyautogui
from modules import *
from modules.AnomalyAgent import anomaly_agent
from jacoco_interpreter import *
from jacoco_interpreter.jacocoPrompter import *

# Output
output = open("output.txt", "w")

# Disable fail-safe (not recommended)
pyautogui.FAILSAFE = False

# Projects: project_path, src_path, test_path
paths = [
    [
        "root",
        "src",
        "test"
    ],[ 
        "root",
        "src",
        "test"
    ],[ 
        "root",
        "src",
        "test"
    ]
]

def path_creator(root, file):
    # Contruct full paths for source and test files
    src_file_path = os.path.join(root, file)
    base_name, ext = os.path.join(file)
    test_file_path = os. path.join(root.replace("src", "test"), base_name+"Tester", ext)
    return src_file_path, base_name, ext, test_file_path

def unittest_firstTime(root, file):
    src_file_path, base_name, ext, test_file_path = path_creator(root, file)

    # Create test path if it does not exist
    os.makedirs(root.replace("src", "test"), exist_ok=True)

    print(f"Processing {file}")
    output.write(f"{beautiful_second()} {base_name} is processing...\n")

    # Copy imports and package from source to test file
    pre_materials = ""
    with open(src_file_path, "r", encoding="utf-8") as src_file:
        for line in src_file:
            if "public" in line:
                break
            pre_materials += line

    # Create test files
    with open(test_file_path, "w", encoding="utf-8") as test_file:
        test_file.write("// Warning! This test file was created by copilot\n\n")
        test_file.write(pre_materials)
        # Unit test materials
        with open("data/unittest_materials.txt", "r") as materials:
            content = materials.read()
            test_file.write()
        # Copilot prompts
        test_file.write(f"""
public class {base_name + "Test"} {{
    // Preare an unit test for this ({base_name + "Test"}) class
""") # {{ makes { in f-based string
        
        services = extract_services(src_file_path)
        for service in services:
            test_file.write(f"\t// Write a @Test for {service}\n")

    # Open file in to the Intellij Idea
    command = [idea, test_file_path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(5)

def unittest_basedJacoco(root, file):
    src_file_path, base_name, ext, test_file_path = path_creator(root, file)

    extracted_path = path_extracter(root, file)
    extracted_path_NC = extracted_path + "/nc.txt"

    if(os.path.exists(extracted_path_NC)):
        if(os.path.exists(test_file_path)):
            if(root[-1] != "/"):
                root += "/"
            if(should_develop(extracted_path_NC)):
                jacoco_prompter(os.path.join(root, test_file_path), extracted_path_NC)

                output.write(f"{beautiful_second()} {base_name}, jacoco based unittest running")
                # Open file in to the Intellij Idea
                command = [idea, test_file_path]
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                time.sleep(5)
                return True
            else:
                print("Test covered enough")
                return False
        else:
            print(f"{(test_file_path)} is not exist")
            return False
    else:
        print(f"Not covered file is not exist for {file}")
        return False

# Start time
start = time.time()
# Time arranger
def beautiful_second(start=start):
    passed_seconds = time.time() - start
    return f"{passed_seconds:09.4f} -"

# Open Intellij Idea
idea = r'C:\Users\N68213\unittest-generator\iidea.bat'
process = subprocess.Popen(idea, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
output.write(f"{beautiful_second()} Intellij Idea opening...")
time.sleep(5)

# MAIN LOOP
for project_path, src_path, test_path in paths:
    # If source path is not exist, stop
    if(os.path.exists(project_path + src_path)):

            # Iterate through all directories and files using os.walk()
            for root, dirs, files in os.walk(project_path + src_path):
                if(root[-1] != "/"):
                    root = root + "/"
                
                i = 0
                retry_time = 0
                while(i < len(files)):
                    file = files[i]
                    i += 1

                    if(is_java_file(file)):
                        if(is_service(root + file)):
                            src_file_path, base_name, ext, test_file_path = path_creator(root, file)

                            choose = 1
                            if(choose == 1):
                                unittest_firstTime(root, file)
                            elif(choose == 2):
                                is_ok = unittest_basedJacoco(root, file)
                                if(not is_ok):
                                    continue
                            else:
                                print("Wrong input")
                                continue



                            # Accept suggestions
                            while(True):
                                pyautogui.hotkey("ctrl", "shift", "alt", "1") # Open copilot plugin (my shortcut)
                                time.sleep(1) # for handling cache warning

                                pyautogui.hotkey("ctrl", "end") # Reach end of the file
                                pyautogui.press("enter")
                                pyautogui.press("home") # Start of the current line
                                pyautogui.hotkey("ctrl", "shift", "alt", "1")
                                time.sleep(13) # Wait for copiloat's response

                                pyautogui.press("enter") # Accept suggestion
                                pyautogui.hotkey("ctrl", "s") # save current content
                                time.sleep(0.2)

                                # Determine if there is an anomaly and fix it if possible
                                if(anomaly_agent(test_file_path)):
                                    retry_time += 1
                                    if(retry_time < 2):
                                        print(f"{base_name} is broken. Retrying...")
                                        output.write(f"{beautiful_second()} {base_name} is broken. Retrying...\n")
                                        i -= 1
                                    else:
                                        print(f"{base_name} is not completed.")
                                        output.write(f"{beautiful_second()} {base_name} is not completed. ")

                                        retry_time = 0
                                        pyautogui.hotkey("ctrl", "f4") # close the current file                     
                                    break

                                # Check if strucructure true
                                if(is_end(test_file_path)):
                                    print(f"{base_name} is completed. ")
                                    delete_excess_enters(test_file_path)
                                    output.write(f"{beautiful_second()} {base_name} is completed.\n")

                                    retry_time = 0
                                    pyautogui.hotkey("ctrl", "f4") # close current file
                                    break
                                
    else:
        print("Source path is not exist: ", project_path+src_path)
    
output.close()