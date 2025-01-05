import os

def create_repo_structure(root_dir):
    structure = {
        "data": ["raw", "processed", "external"],
        "notebooks": ["EDA.ipynb", "FeatureEngineering.ipynb", "Modeling.ipynb", "Submission.ipynb"],
        "src": ["utils.py", "preprocessing.py", "modeling.py", "evaluation.py"],
        "submission": ["sample_submission.csv", "submissions.csv"],
        "reports": ["figures", "README.md"],
        "root_files": ["requirements.txt", "README.md", ".gitignore"]
    }

    for folder, items in structure.items():
        if folder == "root_files":
            for file_name in items:
                open(os.path.join(root_dir, file_name), 'w').close()
        else:
            folder_path = os.path.join(root_dir, folder)
            os.makedirs(folder_path, exist_ok=True)
            for item in items:
                if '.' in item:  # It's a file
                    open(os.path.join(folder_path, item), 'w').close()
                else:  # It's a subdirectory
                    os.makedirs(os.path.join(folder_path, item), exist_ok=True)

    # Add .gitignore content
    gitignore_content = """__pycache__/
*.pyc
*.pyo
*.pyd
data/raw/*
data/processed/*
repo_structure.py
submission/*
"""
    with open(os.path.join(root_dir, ".gitignore"), 'w') as gitignore_file:
        gitignore_file.write(gitignore_content)

if __name__ == "__main__":
    root_directory = "price_optimization"
    os.makedirs(root_directory, exist_ok=True)
    create_repo_structure(root_directory)
    print(f"Repository structure created under: {root_directory}")
