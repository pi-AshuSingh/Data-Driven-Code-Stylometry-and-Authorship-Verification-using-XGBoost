import pandas as pd
import numpy as np

def extract_features(df):
    """
    Extract stylometric features from the raw code.
    Currently extracts basic lexical and layout features.
    
    Args:
        df: Pandas DataFrame with a 'code' column.
        
    Returns:
        Pandas DataFrame with extracted features.
    """
    if df.empty:
        return df

    # Example features:
    # 1. Total lines of code
    df['loc'] = df['code'].apply(lambda x: len(x.splitlines()))
    
    # 2. Average line length
    df['avg_line_length'] = df['code'].apply(
        lambda x: np.mean([len(line) for line in x.splitlines()]) if x.splitlines() else 0
    )
    
    # 3. Number of comments (assuming # for Python)
    df['num_comments'] = df['code'].apply(lambda x: x.count('#'))
    
    # 4. Number of blank lines
    df['blank_lines'] = df['code'].apply(
        lambda x: sum(1 for line in x.splitlines() if not line.strip())
    )
    
    # 5. Use of tabs vs spaces (ratio)
    df['tabs_count'] = df['code'].apply(lambda x: x.count('\t'))
    df['spaces_count'] = df['code'].apply(lambda x: x.count(' '))
    
    # You can expand this to include more sophisticated features like:
    # - AST depth
    # - TF-IDF of character n-grams
    # - Keyword frequencies (def, class, for, while, etc.)
    # - Cyclomatic complexity
    
    return df
