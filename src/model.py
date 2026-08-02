import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

class StylometryModel:
    def __init__(self):
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=4,
            random_state=42
        )
        self.label_encoder = LabelEncoder()
        
    def prepare_data(self, df):
        """
        Prepares the feature matrix X and target vector y.
        """
        # Drop raw code and author to get features only
        # We also need to encode the author labels to integers
        y = self.label_encoder.fit_transform(df['author'])
        X = df.drop(['code', 'author'], axis=1)
        
        return X, y
        
    def train(self, df):
        """
        Trains the XGBoost model.
        """
        if df.empty:
            print("Empty dataframe, cannot train.")
            return None, None
            
        X, y = self.prepare_data(df)
        
        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y if len(pd.Series(y).value_counts()) > 1 else None
        )
        
        print("Training XGBoost model...")
        self.model.fit(X_train, y_train)
        
        print("Evaluating model...")
        y_pred = self.model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.4f}")
        
        # Using zero_division=0 to handle cases where classes are not predicted
        report = classification_report(
            y_test, 
            y_pred, 
            target_names=self.label_encoder.classes_,
            zero_division=0
        )
        print("\nClassification Report:\n", report)
        
        return self.model, report
        
    def predict(self, df_features):
        """
        Predicts authorship for a given set of features.
        """
        preds = self.model.predict(df_features)
        return self.label_encoder.inverse_transform(preds)
