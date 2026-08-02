import os
import glob
import json
import pandas as pd

def load_dataset(dataset_path):
    """
    Load source code files from a directory structure where each subdirectory
    corresponds to an author (class label).
    
    Supports:
    - Raw source code files (.py, .java, .cpp, etc.)
    - Jupyter Notebooks (.ipynb, .json format like AI4Code)
    
    Returns a pandas DataFrame with 'code' and 'author' columns.
    """
    data = []
    
    if not os.path.exists(dataset_path):
        print(f"Warning: Dataset path '{dataset_path}' does not exist.")
        return pd.DataFrame(columns=['code', 'author'])

    def process_file(filepath, author_name):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                if filepath.endswith('.ipynb') or filepath.endswith('.json'):
                    try:
                        notebook = json.load(f)
                        code_cells = []
                        if 'cells' in notebook:
                            for cell in notebook['cells']:
                                if cell.get('cell_type') == 'code':
                                    source = cell.get('source', [])
                                    code_cells.append("".join(source) if isinstance(source, list) else source)
                        elif 'cell_type' in notebook and 'source' in notebook:
                            for cell_id, ctype in notebook['cell_type'].items():
                                if ctype == 'code':
                                    code_cells.append(notebook['source'].get(cell_id, ""))
                        code_content = "\n".join(code_cells)
                    except json.JSONDecodeError:
                        f.seek(0)
                        code_content = f.read()
                else:
                    code_content = f.read()
                    
                if code_content.strip():
                    data.append({'code': code_content, 'author': author_name})
        except Exception:
            pass

    for item in os.listdir(dataset_path):
        item_path = os.path.join(dataset_path, item)
        if os.path.isdir(item_path):
            # It's a directory
            for filepath in glob.glob(os.path.join(item_path, '*.*')):
                basename = os.path.basename(filepath)
                # If GCJ format inside a folder
                if "_0000" in basename and basename.endswith('.java'):
                    actual_author = basename.split("_0000")[0]
                else:
                    actual_author = item
                process_file(filepath, actual_author)
        elif os.path.isfile(item_path):
            # It's a flat file
            basename = os.path.basename(item_path)
            if "_0000" in basename and basename.endswith('.java'):
                actual_author = basename.split("_0000")[0]
            else:
                actual_author = "unknown"
            process_file(item_path, actual_author)
                    
    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} files from {len(df['author'].unique()) if not df.empty else 0} authors.")
    return df

def generate_dummy_dataset(dataset_path="dataset", num_authors=3, files_per_author=5):
    """
    Helper function to generate a dummy dataset for testing if none exists.
    """
    os.makedirs(dataset_path, exist_ok=True)
    
    for i in range(num_authors):
        author_name = f"author_{i+1}"
        author_dir = os.path.join(dataset_path, author_name)
        os.makedirs(author_dir, exist_ok=True)
        
        for j in range(files_per_author):
            file_path = os.path.join(author_dir, f"script_{j+1}.py")
            with open(file_path, "w", encoding="utf-8") as f:
                # Add some variations in stylometry depending on author
                if i == 0:
                    f.write(f"# Author 1 uses lots of comments\n# And long variables\nlong_variable_name_{j} = {j * 10}\nprint(long_variable_name_{j})\n")
                elif i == 1:
                    f.write(f"x={j}\ny={j*2}\nprint(x+y)\n")
                else:
                    f.write(f"def my_func_{j}():\n    ''' Docstring '''\n    return {j}\n\nmy_func_{j}()\n")
                    
    print(f"Dummy dataset generated at {dataset_path}")
