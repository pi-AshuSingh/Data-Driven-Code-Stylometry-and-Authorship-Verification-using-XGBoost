import os
import argparse
from src.data_loader import load_dataset, generate_dummy_dataset
from src.feature_extraction import extract_features
from src.model import StylometryModel

def main():
    parser = argparse.ArgumentParser(description="Code Stylometry and Authorship Verification using XGBoost")
    parser.add_argument("--dataset", type=str, default="dataset", help="Path to the dataset directory")
    parser.add_argument("--generate-dummy", action="store_true", help="Generate a dummy dataset if none exists")
    
    args = parser.parse_args()
    
    dataset_path = args.dataset
    
    # Generate dummy data if requested or if dataset doesn't exist and not explicitly provided
    if args.generate_dummy or (not os.path.exists(dataset_path) and dataset_path == "dataset"):
        generate_dummy_dataset(dataset_path)
        
    print(f"Loading data from '{dataset_path}'...")
    df = load_dataset(dataset_path)
    
    if df.empty:
        print("Dataset is empty. Exiting.")
        return
        
    print("Extracting features...")
    df_features = extract_features(df)
    
    print("Initializing model...")
    model = StylometryModel()
    
    print("Starting training pipeline...")
    model.train(df_features)

if __name__ == "__main__":
    main()
