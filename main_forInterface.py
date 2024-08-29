import os
import json
import argparse
import ctypes
import pyautogui
from modules.__init__ import *
from modules.Debugger import debugger_path
from jacoco_interpreter.JacocoPrompter import jacoco_prompter
from modules.PromptMaker import prompt_maker
from modules.TimeCalculater import time_calculater
from modules.LibrarySynchronizer import library_synchronizer_path

def prevent_sleep():
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
def restore_sleep():
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)

def main_task(paths, run_prompt_maker, run_jacoco_prompter):
    # Average time consume
    time_calculater(paths)

    # Disable fail-safe (not recommended)
    pyautogui.FAILSAFE = False

    # Clean the clipboard
    copy_to_clipboard("")

    # Output
    output = open("output.txt", "w")

    # Open Intellij Idea
    process_ide("idea")
    output.write(f"{beautiful_second()} - Intellij Idea opening...\n")

    # MAIN LOOP
    for project_path, src_path, test_path in paths:
        # If source path is not exist, stop
        if(os.path.exists(project_path + src_path)):

                # Iterate through all directories and files using os.walk()
                for root, dirs, files in os.walk(project_path + src_path):
                    
                    if(root[-1] != "/"):
                        root = root + "/"
                    
                    i = 0
                    while(i < len(files)):
                        file = files[i]
                        i += 1

                        if(run_prompt_maker):
                            prompt_maker(root, file, output)
                        elif(run_jacoco_prompter):
                            jacoco_prompter(root, file, output)   
                                    
        else:
            print("Source path is not exist: ", project_path+src_path)

def run(args):
    prevent_sleep()
    try:
        main_task(args.paths, args.run_prompt_maker, args.run_jacoco_prompter)
    finally:
        restore_sleep()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the main script with given paths and options.")
    parser.add_argument("--run_prompt_maker", action="store_true", help="Run the prompt maker")
    parser.add_argument("--run_jacoco_prompter", action="store_true", help="Run the Jacoco prompter")
    parser.add_argument("--paths", type=str, required=True, help="JSON-formatted paths")

    args = parser.parse_args()

    # JSON to list
    args.paths = json.loads(args.paths)

    run(args)