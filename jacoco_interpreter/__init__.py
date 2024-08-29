jacoco_outputs = "C:/Users/N68213/Desktop/unittest-generator/jacoco_interpreter/jacoco-coverage-lines/"

def path_extracter(root, file):
    extracted_path = jacoco_outputs
    folders = root.split("/")
    repo_name = ""
    for i in range(len(folders)):
        if(folders[i] == "git"):
            repo_name = folders[i+1]
            break
    extracted_path += repo_name + "/"

    for i in range(len(folders)):
        if(folders[i] == "com"):
            while(i < len(folders)-2):
                extracted_path += folders[i] + "."
                i += 1
            extracted_path += folders[i]
        
    clean_file = file.split(".")[0]
    extracted_path += "/" + clean_file

    return extracted_path