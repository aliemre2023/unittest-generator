import os
import re

def debugger_path(paths):
    for project_path, src_path, test_path in paths:
        if(os.path.exists(project_path + test_path)):
            for root, dirs, files in os.walk(project_path + test_path):
                if(root[-1] != "/"): root = root + "/"
                for file in files:
                    test_path = root + file
                    print(test_path)

                    lines = []
                    with open(test_path, "r", encoding="utf-8") as file:
                        lines = file.readlines()
                    
                    lines = debug_mockDao(lines)
                    lines = debug_Mockito(lines)
                    lines = debug_PowerMockito(lines)
                    lines = debug_BSAException(lines)
                    lines = debug_someRecid2short(lines)
                    lines = debug_packageName(lines, test_path)
                    lines = debug_structure(lines)

                    with open(test_path, "w", encoding="utf-8") as file:
                        file.write(lines)

def debugger_file(path):
    if(os.path.exists(path)):
        print(path)
        lines = []
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        lines = debug_mockDao(lines)
        lines = debug_Mockito(lines)
        lines = debug_PowerMockito(lines)
        lines = debug_BSAException(lines)
        lines = debug_someRecid2short(lines)
        lines = debug_packageName(lines, path)
        lines = debug_structure(lines)

        with open(path, "w", encoding="utf-8") as file:
            file.write(lines)
        

def debug_mockDao(lines):
    for i in len(range(lines)):
        line = lines[i]

        if(("PowerMockito.mockStatic" in line) and ("Dao.class);" in line)):
            lines[i] = line.replace("PowerMockito.mockStatic", "mockDao")
            print(f"{i+1}-line: mockDao added.")
        elif(("mockStatic" in line) and ("Dao.class);" in line)):
            lines[i] = line.replace("mockStatic", "mockDao")
            print(f"{i+1}-line: mockDao added.")
        elif(("PowerMockito.mock" in line) and ("Dao.class);" in line)):
            lines[i] = line.replace("PowerMockito.mock", "mockDao")
            print(f"{i+1}-line: mockDao added.")
        
    return lines
                
def debug_Mockito(lines):
    for i in range(len(lines)):
        line = lines[i]

        # anyString'i de düşünebiliriz
        line = re.sub(r'\bPowerMockito\.any\(', "Mockito.any(", line)
        if("Mockito.any(" in line):
            print(f"{i+1}-line: PowerMockito.any -> Mockito.any")
        
        line = re.sub(r'(?<!Mockito\.)\bany\(', "Mockito.any(", line)
        if("any(" in line):
            print(f"{i+1}-line: any -> Mockito.any")

        line = re.sub(r'\bPowerMockito\.eq\(', "Mockito.eq(", line)
        if("Mockito.any(" in line):
            print(f"{i+1}-line: PowerMockito.eq -> Mockito.eq")
        
        line = re.sub(r'(?<!Mockito\.)\beq\(', "Mockito.eq(", line)
        if("e1(" in line):
            print(f"{i+1}-line: eq -> Mockito.eq")
        
        line = re.sub(r'\bPowerMockito\.anyString\(', "Mockito.anyString(", line)
        if("Mockito.anyString(" in line):
            print(f"{i+1}-line: PowerMockito.anyString -> Mockito.anyString")
        
        line = re.sub(r'(?<!Mockito\.)\banyString\(', "Mockito.anyString(", line)
        if("anyString(" in line):
            print(f"{i+1}-line: anyString -> Mockito.anyString")
        
        line = re.sub(r'(?<!Mockito\.)\bverify\(', "Mockito.verify(", line)
        if("Mockito.verify(" in line):
            print(f"{i+1}-line: verify -> Mockito.verify")

        lines[i] = line

    return lines        

def debug_PowerMockito(lines):
    for i in range(len(lines)):
        line = lines[i]

        line = re.sub(r'(?<!PowerMockito\.)doNothing\(', "PowerMockito.doNothing(", line)
        line = re.sub(r'(?<!PowerMockito\.)doThrow\(', "PowerMockito.doThrow(", line)
        line = re.sub(r'(?<!PowerMockito\.)verifyStatic\(', "PowerMockito.verifyStatic(", line)
        line = re.sub(r'(?<!PowerMockito\.)doReturn\(', "PowerMockito.doReturn(", line)
        line = re.sub(r'(?<!PowerMockito\.)whenNew\(', "PowerMockito.whenNew(", line)

        sublist = [
            "PowerMockito.doNothing(",
            "PowerMockito.doThrow(",
            "PowerMockito.verifyStatic(",
            "PowerMockito.doReturn(",
            "PowerMockito.whenNew("
        ]

        if any(sub in line for sub in sublist):
            lines[i] = line
            print(f"{i+1}-line: PowerMockito method added.")
        
    return lines

def debug_BSAException(lines):
    vers = 1
    for i in range(len(lines)):
        line = lines[i]

        excs = []
        if(line.strip()[:len("BSAException")] != "BSAException"):
            for j in range(0, len(line)-len("new BSAException(")):
                if(line[j:j+len("new BSAException(")] == "new BSAException("):
                    print(f"{i+1}-line : BSAException handled")
                    exc = []
                    exc.append(j)
                    j = j + len("new BSAException (")
                    while(line[j] != ")"):
                        j += 1
                    j += 1
                    exc.append(j)
                    tab = len(line) - len(line.lstrip())
                    exc.append(tab)
                    excs.append(exc)
            
            for j in range(len(excs)):
                BSA_content = line[excs[j][0]:exc[j][1]]
                definition = f"exc{vers}"
                tab = excs[j][2]
                new_line = tab*" " + f"BSAException {definition} = {BSA_content};\n" 
                line = line.replace(BSA_content, definition)
                line = new_line + line
                lines[i] = line
                vers += 1

    return line

def debug_someRecid2short(lines):
    for i in range(len(lines)):
        line = lines[i]
        if("someRecid" in line):
            print(f"{i+1}-line: someRecid -> short")
            line = line.replace('"someRecid"', "(short) 1")
            lines[i] = line
        if("someRecId" in line):
            print(f"{i+1}-line: someRecId -> short")
            line = line.replace('"someRecId"', "(short) 1")
            lines[i] = line
        if("validRecid" in line):
            print(f"{i+1}-line: validRecid -> short")
            line = line.replace('"validRecid"', "(short) 1")
            lines[i] = line
        if("validRecId" in line):
            print(f"{i+1}-line: validRecId -> short")
            line = line.replace('"validRecId"', "(short) 1")
            lines[i] = line
    
    return lines

def debug_packageName(lines, path):
    if(len(lines) > 0):
        package_line = lines[0]

        path = path.replace("\\", "/")
        path_parts = path.split("/")
        path_parts = path_parts[:-1]

        true_package_name = "package "
        take_package = False
        for directory in path_parts:
            if(take_package):
                true_package_name += directory + "."

            if(directory == "test"):
                take_package = True

        if true_package_name.endswith("."):
            true_package_name = true_package_name[:-1]

        true_package_name += ";"

        if(package_line != true_package_name):
            lines[0] = true_package_name + "\n"
            print("1-line: package name corrected.") 
    return lines   

def debug_structure(lines):
    for i in range(len(lines)-1, 0, -1):
        line = lines[i].replace("\n", "")
        lines[i] = line 
        if(len(line) != 0):
            if(line[0] == "}"):
                return lines
            else:
                for j in range(i, -1, -1): # i to 0
                    line = lines[j]
                    if((len(line.strip()) == 0) or (lines.strip()[0] != "}")):
                        line = ""
                        lines[j] = line 
                    else:
                        line = line + "\n}"
                        lines[j] = line
                        print(f"{i+1}-line: structure fixed.")
                        return lines
    return lines  