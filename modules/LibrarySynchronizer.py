import time
import os
import pyautogui
import subprocess
import sys
sys.path.append("..")
from modules.__init__ import *

def library_synchronizer_file(path):
    if(os.path.exists(path)):
        # Eclipse should open already
        '''
        process_ide("eclipse")
        '''
        
        print(f"{path.split("/")[-1]} - libraries synchronizing...")

        process_file("eclipse", path)
        time.sleep(2)

        pyautogui.hotkey("ctrl", "end")
        time.sleep(0.1)
        pyautogui.hotkey("ctrl", "shift", "o")
        time.sleep(10)
        pyautogui.press("enter")
        time.sleep(0.1)
        pyautogui.hotkey("ctrl", "end")
        time.sleep(0.1)
        pyautogui.hotkey("ctrl", "shift", "o")
        time.sleep(5)
        for _ in range(10):
            pyautogui.press("enter")
            time.sleep(0.1)
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "f4")

    else:
        print("Source path does not exist:", path)

def library_syncronizer_path(paths):
    for project_path, src_path, test_path in paths:
        if(os.path.exists(project_path + src_path)):
            for root, dirs, files in os.walk(project_path + test_path):
                if(root[-1] != "/"): root = root + "/"

                i = 0
                while(i < len(files)):
                    file = files[i]
                    i += 1

                    print(f"{file} - libraries synchronizing...")

                    file_path = root + file
                    if not os.path.exists(file_path):
                        print(f"File {file_path} does not exist.")
                        continue
                    process_file("eclipse", file_path)

                    pyautogui.hotkey("ctrl", "end")
                    time.sleep(0.1)
                    pyautogui.hotkey("ctrl", "shift", "o")
                    time.sleep(10)
                    pyautogui.press("enter")
                    time.sleep(0.1)
                    pyautogui.hotkey("ctrl", "end")
                    time.sleep(0.1)
                    pyautogui.hotkey("ctrl", "shift", "o")
                    time.sleep(5)
                    for _ in range(10):
                        pyautogui.press("enter")
                        time.sleep(0.1)
                    pyautogui.hotkey("ctrl", "s")
                    time.sleep(1)
                    pyautogui.hotkey("ctrl", "f4")

    else:
        print("Source path does not exist:", project_path + src_path)