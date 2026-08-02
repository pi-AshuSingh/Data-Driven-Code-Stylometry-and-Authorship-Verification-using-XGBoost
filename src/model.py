import os
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.metrics import roc_curve, auc, precision_recall_curve

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
        y = self.label_encoder.fit_transform(df['author'])
        X = df.drop(['code', 'author'], axis=1)
        return X, y
        
    def train(self, df, save_plots=True):
        """
        Trains the XGBoost model and optionally saves evaluation plots.
        """
        if df.empty:
            print("Empty dataframe, cannot train.")
            return None, None, 0.0
            
        # Filter out authors with fewer than 2 files to allow stratified splitting
        author_counts = df['author'].value_counts()
        valid_authors = author_counts[author_counts >= 2].index
        df = df[df['author'].isin(valid_authors)].copy()
        
        if len(df['author'].unique()) < 2:
            print("Not enough authors with >= 2 files to train.")
            return None, None, 0.0
            
        X, y = self.prepare_data(df)
        
        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y if len(pd.Series(y).value_counts()) > 1 else None
        )
        
        print("Training XGBoost model...")
        self.model.fit(X_train, y_train)
        
        print("Evaluating model...")
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.4f}")
        
        report = classification_report(
            y_test, 
            y_pred, 
            target_names=self.label_encoder.classes_,
            zero_division=0,
            output_dict=True
        )
        
        if save_plots:
            self._save_visualizations(y_test, y_pred, y_proba)
            
        return self.model, report, accuracy
        
    def _save_visualizations(self, y_test, y_pred, y_proba):
        os.makedirs("results", exist_ok=True)
        
        # 1. Confusion Matrix
        plt.figure(figsize=(8, 6))
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=self.label_encoder.classes_,
                    yticklabels=self.label_encoder.classes_)
        plt.title('Confusion Matrix')
        plt.ylabel('True Author')
        plt.xlabel('Predicted Author')
        plt.tight_layout()
        plt.savefig('results/confusion_matrix.png')
        plt.close()
        
        # 2. ROC Curve (Multi-class approximation by macro-averaging)
        plt.figure(figsize=(8, 6))
        n_classes = len(self.label_encoder.classes_)
        
        if n_classes == 2:
            fpr, tpr, _ = roc_curve(y_test, y_proba[:, 1])
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, lw=2, label=f'ROC curve (area = {roc_auc:0.2f})')
        else:
            # Multi-class simplified visualization
            for i in range(n_classes):
                # Binarize labels for one-vs-rest
                y_bin = (y_test == i).astype(int)
                fpr, tpr, _ = roc_curve(y_bin, y_proba[:, i])
                roc_auc = auc(fpr, tpr)
                plt.plot(fpr, tpr, lw=2, label=f'Class {self.label_encoder.classes_[i]} (area = {roc_auc:0.2f})')
                
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig('results/roc_curve.png')
        plt.close()

        # 3. Precision-Recall Curve
        plt.figure(figsize=(8, 6))
        if n_classes == 2:
            precision, recall, _ = precision_recall_curve(y_test, y_proba[:, 1])
            plt.plot(recall, precision, lw=2)
        else:
            for i in range(n_classes):
                y_bin = (y_test == i).astype(int)
                precision, recall, _ = precision_recall_curve(y_bin, y_proba[:, i])
                plt.plot(recall, precision, lw=2, label=f'Class {self.label_encoder.classes_[i]}')
            plt.legend()
            
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.tight_layout()
        plt.savefig('results/pr_curve.png')
        plt.close()

    def predict(self, df_features):
        """
        Predicts authorship for a given set of features.
        Returns predicted author and probabilities.
        """
        preds = self.model.predict(df_features)
        probas = self.model.predict_proba(df_features)
        
        predicted_authors = self.label_encoder.inverse_transform(preds)
        return predicted_authors, probas
