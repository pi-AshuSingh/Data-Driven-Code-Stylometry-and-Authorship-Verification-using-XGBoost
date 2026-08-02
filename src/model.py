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
        
        # Limit to top 50 authors if there are too many (speeds up training & fixes unreadable graphs)
        if len(author_counts) > 50:
            print(f"Dataset has {len(author_counts)} authors. Keeping top 50 most prolific authors for faster training...")
            valid_authors = author_counts.head(50).index
        else:
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
        
        sns.set_theme(style="whitegrid")
        n_classes = len(self.label_encoder.classes_)
        
        # 1. Confusion Matrix (Presentation Quality)
        plt.figure(figsize=(12, 10))
        cm = confusion_matrix(y_test, y_pred)
        
        # Only annotate if there are few classes to avoid clutter
        show_annot = n_classes <= 15
        
        sns.heatmap(cm, annot=show_annot, fmt='d', cmap='Blues',
                    xticklabels=self.label_encoder.classes_ if show_annot else False,
                    yticklabels=self.label_encoder.classes_ if show_annot else False,
                    cbar_kws={'label': 'Number of predictions'})
        
        plt.title('Code Stylometry: Authorship Confusion Matrix', fontsize=16, pad=15)
        plt.ylabel('True Author', fontsize=12)
        plt.xlabel('Predicted Author', fontsize=12)
        if show_annot:
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig('results/confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. ROC Curve (With Micro & Macro Averaging for Multi-class)
        plt.figure(figsize=(10, 8))
        
        if n_classes == 2:
            fpr, tpr, _ = roc_curve(y_test, y_proba[:, 1])
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, lw=2, color='darkorange', label=f'ROC curve (AUC = {roc_auc:0.3f})')
        else:
            # Compute micro-average ROC curve and ROC area
            # Binarize the output
            from sklearn.preprocessing import label_binarize
            y_test_bin = label_binarize(y_test, classes=range(n_classes))
            
            fpr_micro, tpr_micro, _ = roc_curve(y_test_bin.ravel(), y_proba.ravel())
            roc_auc_micro = auc(fpr_micro, tpr_micro)
            
            plt.plot(fpr_micro, tpr_micro, color='deeppink', linestyle=':', linewidth=4,
                     label=f'Micro-average ROC (AUC = {roc_auc_micro:0.3f})')
            
            # Plot only the top 3 best performing classes to keep graph readable
            auc_scores = []
            for i in range(n_classes):
                fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
                auc_scores.append((i, auc(fpr, tpr), fpr, tpr))
                
            auc_scores.sort(key=lambda x: x[1], reverse=True)
            
            colors = ['aqua', 'darkorange', 'cornflowerblue']
            for idx, (i, roc_auc, fpr, tpr) in enumerate(auc_scores[:3]):
                author_name = self.label_encoder.classes_[i]
                plt.plot(fpr, tpr, lw=2, color=colors[idx % len(colors)],
                         label=f'Class {author_name} (AUC = {roc_auc:0.3f})')
                
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontsize=12)
        plt.ylabel('True Positive Rate', fontsize=12)
        plt.title('Receiver Operating Characteristic (ROC)', fontsize=16, pad=15)
        plt.legend(loc="lower right", fontsize=10, frameon=True, shadow=True)
        plt.tight_layout()
        plt.savefig('results/roc_curve.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 3. Precision-Recall Curve
        plt.figure(figsize=(10, 8))
        if n_classes == 2:
            precision, recall, _ = precision_recall_curve(y_test, y_proba[:, 1])
            plt.plot(recall, precision, lw=2, color='green', label='PR Curve')
            plt.legend(loc='lower left')
        else:
            # Micro-average PR curve
            precision_micro, recall_micro, _ = precision_recall_curve(y_test_bin.ravel(), y_proba.ravel())
            plt.plot(recall_micro, precision_micro, color='gold', linestyle=':', linewidth=4,
                     label='Micro-average PR Curve')
            
            for idx, (i, _, _, _) in enumerate(auc_scores[:3]):
                author_name = self.label_encoder.classes_[i]
                precision, recall, _ = precision_recall_curve(y_test_bin[:, i], y_proba[:, i])
                plt.plot(recall, precision, lw=2, color=colors[idx % len(colors)],
                         label=f'Class {author_name}')
            plt.legend(loc='lower left', fontsize=10, frameon=True, shadow=True)
            
        plt.xlabel('Recall', fontsize=12)
        plt.ylabel('Precision', fontsize=12)
        plt.title('Precision-Recall Curve', fontsize=16, pad=15)
        plt.tight_layout()
        plt.savefig('results/pr_curve.png', dpi=300, bbox_inches='tight')
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
