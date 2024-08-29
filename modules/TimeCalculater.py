import os
import sys
sys.path.append("..")
from modules.__init__ import *
from modules.PromptMaker import specialize_file, specialize_situation, prompter


def time_calculater(paths):
    prompts = []
    prompts = prompter(prompts ,"does not matter")
    processed_file = 0
    determined_list = ["a", "b"]

    for project_path, src_path, test_path in paths:
        if(os.path.exists(project_path + src_path)):
            for root, dirs, files in os.walk(project_path + test_path):
                if(root[-1] != "/"): root = root + "/"

                i = 0
                while(i < len(files)):
                    file = files[i]
                    i += 1

                    j = 0
                    while(j < len(prompts)):
                        prompt = prompts[j]
                        j += 1

                        if(specialize_file(root, file)): # dys file should not consider
                            # Construct full paths for source and test files
                            src_file_path = os.path.join(root, file)
                            base_name, ext = os.path.splitext(file)
                            test_file_path = os.path.join(root.replace("src", "test"), base_name + f"_v{j}_" + "Test" + ext)

                            if not os.path.exists(test_file_path):
                                processed_file += 1
                            if(specialize_situation(test_file_path=test_file_path, src_file_name=src_file_path, determined_list=determined_list)):                              
                                processed_file += 1
    minutes = processed_file * 80 / 60
    print(f"Service File Count: {processed_file}\nEstimated time: {minutes} minutes.")