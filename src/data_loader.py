import os
import glob
import pandas as pd

def load_dataset(dataset_path):
    """
    Load source code files from a directory structure where each subdirectory
    corresponds to an author (class label).
    
    Example structure:
    dataset/
        author1/
            file1.py
            file2.py
        author2/
            file3.py
    
    Returns a pandas DataFrame with 'code' and 'author' columns.
    """
    data = []
    
    if not os.path.exists(dataset_path):
        print(f"Warning: Dataset path '{dataset_path}' does not exist.")
        return pd.DataFrame(columns=['code', 'author'])

    for author_dir in os.listdir(dataset_path):
        author_path = os.path.join(dataset_path, author_dir)
        if os.path.isdir(author_path):
            # Iterate through all files in author directory
            for filepath in glob.glob(os.path.join(author_path, '*.*')):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        code_content = f.read()
                        data.append({'code': code_content, 'author': author_dir})
                except Exception as e:
                    print(f"Error reading file {filepath}: {e}")
                    
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
