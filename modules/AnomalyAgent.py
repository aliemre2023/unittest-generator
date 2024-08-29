def fix_tryCatchBrackets(file_path):
    file_r = open(file_path, "r", encoding="utf-8")
    java_code = file_r.read()
    file_r.close()

    java_line = java_code.split("\n")
    for line in java_line[::-1]:
        if("try" in line):
            try_indentation = len(line) - len(line.lstrip())
    
    catch_index = java_code.find("catch")

    # Ensure catch block ends with '}'
    if(catch_index != -1):
        stack = []

        i = catch_index
        while(i < len(java_code)):
            if(java_code[i] == "{"):
                stack.append('{')
            elif(java_code[i] == "}"):
                if stack:
                    stack.pop()
                else:
                    print("ERROR: Closed parenthesis without opening")
                    return False
            i += 1
        
        if stack:
            # If stack is not empty, add clasing '}' at the end of the file
            java_code += "\n" + " " * try_indentation + "}"
            print("WARNING: try-catch indentation fixed")
        
        file_w = open(file_path, "w", encoding="utf-8")
        file_w.write(java_code)
        file_w.close()
    
    return False

def fix_badBrackets(file_path):
    '''
    fix the situations like;
    }
    }
    or
    } 
        }
    '''
    lines = []
    with open(file_path, "r") as file:
        lines = file.readlines()

    i = 0
    while i < len(lines) - 1:
        line = lines[i].rstrip()
        next_line = lines[i+1].rstrip()

        if("}" in line and "}" in next_line):
            curr_indent = len(line) - len(line.lstrip())
            next_indent = len(next_line) - len(next_line.lstrip())

            # Correct the basic anomalie
            if(next_indent >= curr_indent):
                next_line = (int(curr_indent - len("    "))) * " " + next_line.lstrip()
                lines[i+1] = next_line
                with open(file_path, "w", encoding="utf-8") as corrected_file:
                    corrected_file.writelines(lines)
                print("WARNING: Bracket issue fixed")
        i += 1
    
    return False

def stop_sameResponse(file_path):
    '''
    Stiuations for copilot generate same response (it goes to loop)
    '''
    lines = []
    with open(file_path, "r") as file:
        lines = file.readlines()

    if(len(lines) > 1000):
        # Look file content
        print("ERROR: Possible producing the same response")
        return True

def stop_independentIndentations(file_path):
    '''
    Situations for independent indentations
    '''
    lines = []
    with open(file_path, "r") as file:
        lines = file.readlines()

    tabs = []
    for line in lines:
        if(len(line) - len(line.lstrip()) != 1): # 1 represent blank line
            tabs.append(int((len(line) - len(line.lstrip())) / 4)) # 4 is \t's length

    for j in range(len(tabs) - 1):
        curr_tab = tabs[j]
        next_tab = tabs[j+1]
        if not (curr_tab == next_tab or curr_tab-1 == next_tab or curr_tab+1 == next_tab):
            print("ERROR: Independent indentations")
            return True
              
    return False

def anomaly_agent(file_path):
    if(
        fix_tryCatchBrackets(file_path) or
        fix_badBrackets(file_path) or
        stop_sameResponse(file_path) or
        stop_independentIndentations(file_path)
    ): return True
    return False