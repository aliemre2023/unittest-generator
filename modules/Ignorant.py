import xml.etree.ElementTree as ET
import os

def parse_junit_report(report_path):
    tree = ET.parse(report_path)
    root = tree.getroot()

    failed_tests = []

    for testcase in root.finall(".//testcase"):
        test_class = testcase.get("class_name")
        test_name = testcase.get("name")

        error_element = testcase.find("error")
        failure_element = testcase.find("failure")

        if(error_element is not None):
            message = error_element.get.text.strip()
            truncated_message = ""
            if(len(message) > 250): 
                truncated_message = message[:250] + "..."
            else:
                truncated_message = message
            failed_tests.append((test_class, test_name, "error", truncated_message))
        if(failure_element is not None):
            message = failure_element.get.text.strip()
            truncated_message = ""
            if(len(message) > 250): 
                truncated_message = message[:250] + "..."
            else:
                truncated_message = message
            failed_tests.append((test_class, test_name, "failure", truncated_message))
    
    return failed_tests

def update_test_file(failed_test, test_dir):
    test_class = failed_test[0]
    test_name = failed_test[1]
    output_type = failed_test[2]
    output_message = failed_test[3]

    file_path = os.path.join(test_dir, test_class.replace(".", "/") + ".java")
    if(not os.path.isfile(file_path)):
        print(f"File {file_path} does not exist")
        return
    
    lines = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # @Ignore method
    '''
    lines[0] += "\nimport org.junit.Ignore"
    file.writelines(lines)
    with open(file_path, "w", encoding="utf-8") as file:
        in_test_method = False
        for line in lines:
            if(f"public void {test_name}()" in line):
                in_test_method = True
                file.write(f'\t@Ignore("{output_type} test ignored (autonomously)")\n\t/*{output_message}*/\n')
            if(in_test_method and line.strip() == "}"):
                in_test_method = False
            file.write(line)
    '''
    

    with open(file_path, "w", encoding="utf-8") as file:
        in_test_method = False

        for i in range(len(lines)):
            line = lines[i]
            if(f"public void {test_name}()" in line):
                in_test_method = True
                lines[i-1] = f"\t/* {output_type}\n{output_message}\n\t*/\n" + "//" + lines[i-1]

                while(i < len(lines) and (not ((lines[i].strip() == "}") and ((len(lines[i].rstrip()) - len(lines[i].strip()))) == 4))):
                    lines[i] = "//" + lines[i]
                    i += 1
                if(i < len(lines) and not (len(lines[i].rstrip()) - len(lines[i].strip())) == 0):
                    lines[i] = "//" + lines[i]

                file.writelines(lines)
                break

def comment_deleter(failed_test, test_dir):
    test_class = failed_test[0]
    test_name = failed_test[1]
    output_type = failed_test[2]
    output_message = failed_test[3]

    file_path = os.path.join(test_dir, test_class.replace(".", "/") + ".java")
    if(not os.path.isfile(file_path)):
        print(f"File {file_path} does not exist")
        return
    
    lines = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    with open(file_path, "w", encoding="utf-8") as file:
        in_test_method = False

        for i in range(len(lines)):
            line = lines[i]
            if(f"public void {test_name}()" in line):
                in_test_method = True
                if(lines[i-1][:2] == "//"): lines[i-2] = lines[i-1][2:]

                while(i < len(lines) and (not ((lines[i].strip() == "}") and ((len(lines[i].rstrip()) - len(lines[i].strip()))) == 4))):
                    lines[i] = lines[i][2:]
                    i += 1
                if(lines[i][2:] == "//"): lines[i] = lines[i][2:]

                file.writelines(lines)
                break

if __name__ == "__main__":
    #####
    choose = 1
    report_path = "junit_reports/example_report.xml"
    test_dir = "C:/example/path/"
    #####
    
    failed_tests = parse_junit_report(report_path)

    for failed_test in failed_tests:
        if(choose == 1):
            update_test_file(failed_test, test_dir)
            print(f"Updates {failed_test[0]} to ignore test {failed_test[1]}")
        else:
            comment_deleter(failed_test, test_dir)
            print(f"Comments deleted.")