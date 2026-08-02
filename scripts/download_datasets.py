import os
import zipfile
import shutil

try:
    from kaggle.api.kaggle_api_extended import KaggleApi
except OSError:
    print("WARNING: Kaggle API credentials not found!")
    print("Please place your kaggle.json file in ~/.kaggle/kaggle.json")
    print("You can create a new API token from your Kaggle Account Settings.")
    exit(1)

def download_and_extract(dataset_slug, download_path):
    print(f"Downloading {dataset_slug}...")
    api = KaggleApi()
    api.authenticate()
    
    # Download dataset
    api.dataset_download_files(dataset_slug, path=download_path, unzip=False)
    
    # Find the downloaded zip
    zip_name = dataset_slug.split('/')[-1] + '.zip'
    zip_path = os.path.join(download_path, zip_name)
    
    if os.path.exists(zip_path):
        print(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(download_path)
        os.remove(zip_path)
        print(f"Extraction complete for {dataset_slug}.")
    else:
        print(f"Warning: Could not find zip file for {dataset_slug}")

def organize_ai4code(base_path):
    """Samples AI4Code (Jupyter Notebooks) and organizes them by a pseudo-author."""
    # AI4Code doesn't have authors, just a lot of notebooks.
    # We will sample 100 notebooks and assign them to 2 pseudo-authors for stylistic testing.
    print("Organizing a small sample of AI4Code...")
    import glob
    import random
    
    source_dir = os.path.join(base_path, "train")
    if not os.path.exists(source_dir):
        return
        
    notebooks = glob.glob(os.path.join(source_dir, "*.json"))
    random.seed(42)
    random.shuffle(notebooks)
    
    # Take 50 notebooks for Author_A, 50 for Author_B
    sample = notebooks[:100]
    
    for i, nb in enumerate(sample):
        author_dir = os.path.join(base_path, "Author_Notebooks_A" if i < 50 else "Author_Notebooks_B")
        os.makedirs(author_dir, exist_ok=True)
        shutil.copy(nb, os.path.join(author_dir, os.path.basename(nb)))
        
    print("AI4Code sample organized.")

if __name__ == "__main__":
    DATASET_DIR = "dataset/kaggle_data"
    os.makedirs(DATASET_DIR, exist_ok=True)
    
    # 1. GPT Java GCJ Source Code (GPT vs Human)
    # dataset_slug: m710323363/gpt-java-gcj-source-code
    try:
        download_and_extract('m710323363/gpt-java-gcj-source-code', os.path.join(DATASET_DIR, "gpt_java_gcj"))
    except Exception as e:
        print(f"Failed to download GPT Java GCJ: {e}")

    # 2. Google AI4Code (Python Notebooks)
    try:
        ai4code_dir = os.path.join(DATASET_DIR, "ai4code")
        print("Downloading google-ai4code...")
        
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        
        api.competition_download_files('google-ai4code', path=ai4code_dir)
        
        # Extract the competition zip
        zip_path = os.path.join(ai4code_dir, 'google-ai4code.zip')
        if os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(ai4code_dir)
            os.remove(zip_path)
            
        organize_ai4code(ai4code_dir)
    except Exception as e:
        print(f"Failed to download AI4Code: {e}")

    # 3. Standard Google Code Jam Dataset
    # Since there are many, we use a popular pre-processed one for authorship
    try:
        download_and_extract('crawford/google-code-jam-dataset', os.path.join(DATASET_DIR, "gcj_standard"))
    except Exception as e:
        print(f"Failed to download standard GCJ: {e}")

    print(f"\nAll downloads finished! Data saved to {DATASET_DIR}")
    print("Note: The Streamlit app can now point to this folder.")
