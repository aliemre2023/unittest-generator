import sys 
import json
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QPushButton, QWidget, QHBoxLayout

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UNITTEST GENERATOR")

        self.paths = []
        self.run_type = 0
        self.run_prompt_maker = True
        self.run_jacoco_prompt = False

        self.initUI()
    
    def initUI(self):
        self.setGeometry(0, 0, 700, 900)
        self.setMinimumSize(700, 900)
        self.setMaximumSize(700, 900)

        self.setStyleSheet("background-color: lightyellow;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Input fileds
        self.project_path = QLineEdit(self)
        self.project_path.setPlaceholderText("Enter project path")
        self.project_path.setStyleSheet("background-color: lightgray; color: black;")
        layout.addWidget(self.project_path)

        self.src_path = QLineEdit(self)
        self.src_path.setPlaceholderText("Enter src path")
        self.src_path.setStyleSheet("background-color: lightgray; color: black;")
        layout.addWidget(self.src_path)

        self.test_path = QLineEdit(self)
        self.test_path.setPlaceholderText("Enter test path")
        self.test_path.setStyleSheet("background-color: lightgray; color: black;")
        layout.addWidget(self.test_path)

        self.push_button = QPushButton("Add to paths", self)
        self.push_button.setStyleSheet("background-color: lightblue;")
        self.push_button.clicked.connect(self.add_path_to_paths)
        layout.addWidget(self.push_button)


        properties_layout = QHBoxLayout()
        
        self.dwp = QPushButton("delete whole paths", self)
        self.dwp.setStyleSheet("background-color: lightgreen;")
        self.dwp.clicked.connect(self.delete_whole_paths)
        properties_layout.addWidget(self.dwp)

        self.dliop = QPushButton("delete last index of paths", self)
        self.dliop.setStyleSheet("background-color: lightgreen;")
        self.dliop.clicked.connect(self.delete_last_index_of_paths)
        properties_layout.addWidget(self.dliop)

        properties_layout.setContentsMargins(150, 0, 150, 0)
        layout.addLayout(properties_layout)


        button_layout = QHBoxLayout()

        self.run_prompt_maker_button = QPushButton("Prompt", self)
        self.run_prompt_maker_button.clicked.connect(lambda: self.set_run_type(1))
        button_layout.addWidget(self.run_prompt_maker_button)

        self.run_jacoco_prompt_button = QPushButton("Jacoco P", self)
        self.run_jacoco_prompt_button.clicked.connect(lambda: self.set_run_type(2))
        button_layout.addWidget(self.run_jacoco_prompt_button)
        
        button_layout.setContentsMargins(150, 0, 150, 0)
        layout.addLayout(button_layout)


        run_layout = QVBoxLayout()

        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.run)
        self.run_button.setStyleSheet("background-color: red;")
        run_layout.addWidget(self.run_button)
        run_layout.setContentsMargins(150, 0, 150, 0)
        layout.addLayout(run_layout)


        self.path_label = QLabel(self)
        self.path_label.setStyleSheet("color: black;")
        layout.addWidget(self.path_label)

        self.update_button_states()

    def add_path_to_paths(self):
        path1 = self.project_path.text()
        path2 = self.src_path.text()
        path3 = self.test_path.text()

        if path1 and path2 and path3:
            path = [path1, path2, path3]
            self.paths.append(path)
            self.update_label()

    def update_label(self):
        formatted_paths = "paths = [\n"
        for path_list in self.paths:
            formatted_paths += "    [\n"
            for path in path_list:
                formatted_paths += f"       \"{path}\",\n"
            formatted_paths += "    ],\n"
        formatted_paths += "]"

        self.path_label.setText(f"<pre>{formatted_paths}</pre>")
        
    def set_run_type(self, run_type):
        self.run_type = run_type
        if(run_type == 1):
            self.run_prompt_maker = True
            self.run_jacoco_prompt = False
        elif(run_type == 2):
            self.run_prompt_maker = False
            self.run_jacoco_prompt = True
        self.update_button_states()

    def update_button_states(self):
        if(self.run_prompt_maker):
            self.run_prompt_maker_button.setStyleSheet("background-color: green;")
            self.run_jacoco_prompt_button.setStyleSheet("background-color: gray;")
        elif(self.run_jacoco_prompt):
            self.run_prompt_maker_button.setStyleSheet("background-color: gray;")
            self.run_jacoco_prompt_button.setStyleSheet("background-color: green;")

    def run(self):
        paths_json = json.dumps(self.paths) # paths to json
        args = [
            "--run_prompt_maker" if self.run_prompt_maker else "--run_jacoco_prompter",
            "--paths", paths_json
        ]

        script_path = "main_forInterface.py"
        try:
            subprocess.run(["python", script_path] + args, check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occured: {e}")
    
    def delete_whole_paths(self):
        self.paths.clear()
        self.update_label()
    
    def delete_last_index_of_paths(self):
        if(len(self.paths) > 0):
            self.paths.pop()
            self.update_label()
        else:
            print("There is no element in paths.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = App()
    mainWindow.show()
    sys.exit(app.exec())