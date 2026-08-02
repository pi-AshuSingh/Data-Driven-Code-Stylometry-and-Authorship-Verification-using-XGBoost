import ast
import pandas as pd
import numpy as np

class ASTFeatureExtractor(ast.NodeVisitor):
    def __init__(self):
        self.node_counts = {}
        self.max_depth = 0
        self.current_depth = 0
        
    def generic_visit(self, node):
        node_type = type(node).__name__
        self.node_counts[node_type] = self.node_counts.get(node_type, 0) + 1
        
        self.current_depth += 1
        if self.current_depth > self.max_depth:
            self.max_depth = self.current_depth
            
        super().generic_visit(node)
        self.current_depth -= 1

def extract_features(df):
    """
    Extract stylometric features from the raw code.
    Extracts lexical, layout, and advanced AST structural features.
    
    Args:
        df: Pandas DataFrame with a 'code' column.
        
    Returns:
        Pandas DataFrame with extracted features.
    """
    if df.empty:
        return df

    features_list = []
    
    for code in df['code']:
        features = {}
        
        # 1. Lexical & Layout Features
        lines = code.splitlines()
        features['loc'] = len(lines)
        features['avg_line_length'] = np.mean([len(line) for line in lines]) if lines else 0
        features['num_comments'] = code.count('#')
        features['blank_lines'] = sum(1 for line in lines if not line.strip())
        features['tabs_count'] = code.count('\t')
        features['spaces_count'] = code.count(' ')
        
        # 2. AST Structural Features
        try:
            tree = ast.parse(code)
            extractor = ASTFeatureExtractor()
            extractor.visit(tree)
            
            features['ast_max_depth'] = extractor.max_depth
            features['ast_num_functions'] = extractor.node_counts.get('FunctionDef', 0)
            features['ast_num_classes'] = extractor.node_counts.get('ClassDef', 0)
            features['ast_num_loops'] = extractor.node_counts.get('For', 0) + extractor.node_counts.get('While', 0)
            features['ast_num_if'] = extractor.node_counts.get('If', 0)
            features['ast_num_returns'] = extractor.node_counts.get('Return', 0)
            features['ast_num_imports'] = extractor.node_counts.get('Import', 0) + extractor.node_counts.get('ImportFrom', 0)
            
        except Exception:
            # Fallback if code is not valid Python
            features['ast_max_depth'] = 0
            features['ast_num_functions'] = 0
            features['ast_num_classes'] = 0
            features['ast_num_loops'] = 0
            features['ast_num_if'] = 0
            features['ast_num_returns'] = 0
            features['ast_num_imports'] = 0
            
        features_list.append(features)
        
    # Combine original df with new features
    features_df = pd.DataFrame(features_list)
    result_df = pd.concat([df, features_df], axis=1)
    
    return result_df
