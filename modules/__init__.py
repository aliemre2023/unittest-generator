import re
import os
import subprocess
import time

# Control the structure
def is_end(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines[::-1]:
            line = line.replace("\n", "")
            if(len(line) != 0):
                if(line[0] == "}"):
                    return True
                else:
                    return False
                
def delete_excess_enters(file_path):
    lines = []
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    i = 0
    while i < len(lines) - 1:
        if(lines[i] == "\n" and lines[i+1] == "\n"):
            del lines[i]
        else:
            i += 1

    with open(file_path, "w") as file:
        file.writelines(lines)

# Control extention
def is_java_file(filename):
    return filename.endswith(".java")

# Extraxt service names
def extract_services(file_path):
    file = open(file_path, "r", encoding="utf-8")
    pattern = r'@Service\("([^"]+)"\)'
    service_names = []

    lines = file.readlines()
    for line in lines:
        match = re.search(pattern, line)
        if(match):
            service_names.append(match.group(1))
    file.close()
    return service_names

# Control if file include Service annotation
def is_service(file_path):
    service_names = extract_services(file_path)
    if(len(service_names) != 0): return True
    else: return False

# Copy text
def copy_to_clipboard(text):
    process = subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=True)
    process.communicate(text.encode("utf-8"))

def is_file_empty(file_path):
    return os.path.getsize(file_path) <= 512

def is_dys(full_path):
    folders = full_path.split("/")
    if("dys" in folders):
        return True
    else:
        return False
    
# Start time
start = time.time()
# Time arrange
def beautiful_second(start=start):
    passed_seconds = time.time() - start
    return f"{passed_seconds:09.4f}"

def process_ide(ide):
    idea = r'C:\path\to\iidea.bat'
    eclipse = r'C:\path\to\eeclipse.bat'
    if(ide == "idea"):
        process = subprocess.Popen(idea, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        time.sleep(15)
    elif(ide == "eclipse"):
        process = subprocess.Popen(eclipse, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        time.sleep(15)
    else:
        raise ValueError("Wrong IDE type, (idea and elipse)")

def process_file(ide, path):
    idea = r'C:\path\to\iidea.bat'
    eclipse = r'C:\path\to\eeclipse.bat'
    if(ide == "idea"):
        command = [idea, path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        time.sleep(3)
    elif(ide == "eclipse"):
        command = [eclipse, path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        time.sleep(3)
    else:
        raise ValueError("Wrong IDE type, (idea and elipse)")