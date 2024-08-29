from bs4 import BeautifulSoup
import pandas as pd
import os
import shutil

curr_path = "C:/path/to/unittest-generator/jacoco-interpreter/"

def extract_and_rate_spans(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Store content by category
    content_dict = {
        'nc': [],
        'fc': [],
        'bnc': [],
        'pc': [],
        'nc-bnc': [],
        'nc-fc': [],
        'fc-bnc': [],
        'fc-pc': [],
        'bnc-pc': [],
        'nc-fc-bnc': [],
        'nc-fc-pc': [],
        'fc-bnc-pc': [],
        'nc-fc-bnc-pc': []
    }

    # Extract span elements and categorize them
    for span in soup.find_all('span', class_=True):
        classes = span['class']
        span_id = span.get('id', 'unknown')
        # 0 index is L char
        line_content = f"{span_id[0]}{(span_id[1:]).zfill(3)} -> {span.get_text()}"

        # Determine the category
        categories = set(classes)
        # 'not covered' is priority, only one to use for now
        if 'nc' in categories:
            category = 'nc'
        elif 'fc' in categories:
            if 'bnc' in categories:
                category = 'fc-bnc'
            elif 'pc' in categories:
                category = 'fc-pc'
            else:
                category = 'fc'
        elif 'bnc' in categories:
            if 'pc' in categories:
                category = 'bnc-pc'
            else:
                category = 'bnc'
        elif 'pc' in categories:
            category = 'pc'
        else:
            category = 'unknown'

        # Handle all possible combinations
        if category == 'unknown':
            continue

        content_dict[category].append(line_content)
    
    parts = html_file.split("/")
    folder_name = parts[-1].split("\\")[-1]
    file_name = folder_name.split(".")[0]
    saved_path = parts[4] + "/" + parts[-1].split("\\")[0]
    dottes = saved_path.split(".")
    
    for category, contents in content_dict.items():
        if (contents and "service" in dottes):
            os.makedirs(os.path.join(curr_path, f"jacoco-coverage-lines/{saved_path}/{file_name}"), exist_ok=True)
            with open(f"jacoco-coverage-lines/{saved_path}/{file_name}/{category}.txt", 'w', encoding='utf-8') as file:
                file.write("\n".join(contents))

if __name__ == "__main__":
    #### There are lots of path to changei so I add that
    projects = ["aProject"]
    ####
    Projects = [p.capitalize() for p in projects]

    for project, Project in zip(projects, Projects):
        jacoco_file_path = f"c:/path/to/site/jacoco/report/{project}"
        file_paths = []

        if os.path.exists(curr_path + f"jacoco_coverage_lines/{project}/"):
            shutil.rmtree(curr_path + f"jacoco_coverage_lines/{project}/" )
    
        for root, dirs, files in os.walk(jacoco_file_path):
            for file in files:
                if((f"this.is.a.specializetion" in root) and 
                   not (f"this.is.an.specializetion" in root) and
                   file.endswith(".java.html")):
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)

        for path in file_paths :
            extract_and_rate_spans(path)
        
        print("Covered files extracted.")