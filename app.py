import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

from src.data_loader import load_dataset, generate_dummy_dataset
from src.feature_extraction import extract_features
from src.model import StylometryModel

# --- Configuration ---
st.set_page_config(page_title="Code Stylometry & Authorship Verification", layout="wide", page_icon="🕵️‍♂️")

# --- App State ---
if 'model' not in st.session_state:
    st.session_state.model = None
if 'features_df' not in st.session_state:
    st.session_state.features_df = None
if 'report' not in st.session_state:
    st.session_state.report = None

# --- Helper Functions ---
@st.cache_data
def load_and_extract(dataset_path):
    df = load_dataset(dataset_path)
    if df.empty:
        return df, pd.DataFrame()
    
    features_df = extract_features(df)
    return df, features_df

# --- Sidebar ---
st.sidebar.title("Configuration")
dataset_path = st.sidebar.text_input("Dataset Path", "dataset")

if st.sidebar.button("Generate Dummy Data"):
    with st.spinner("Generating..."):
        generate_dummy_dataset(dataset_path)
    st.sidebar.success("Dummy dataset generated!")

if st.sidebar.button("Train Model"):
    with st.spinner("Loading Data & Extracting Features..."):
        df, features_df = load_and_extract(dataset_path)
        
    if df.empty:
        st.sidebar.error("Dataset is empty! Generate dummy data or add real files.")
    else:
        with st.spinner("Training XGBoost Model..."):
            model = StylometryModel()
            _, report, accuracy = model.train(features_df, save_plots=True)
            
            st.session_state.model = model
            st.session_state.features_df = features_df
            st.session_state.report = report
            st.sidebar.success(f"Model Trained! Accuracy: {accuracy*100:.2f}%")

# --- Main App ---
st.title("🕵️‍♂️ Code Stylometry & Authorship Verification")
st.markdown("Verify code authorship using robust AST structural features and an XGBoost classifier.")

tab1, tab2, tab3 = st.tabs(["Prediction", "Model Metrics", "Feature Importance"])

# --- Tab 1: Prediction ---
with tab1:
    st.header("Test Authorship")
    st.markdown("Paste a Python snippet below to see who the model thinks wrote it.")
    
    code_input = st.text_area("Source Code", height=300, placeholder="def my_function():\n    pass")
    
    if st.button("Verify Author"):
        if st.session_state.model is None:
            st.error("Please train the model first using the sidebar!")
        elif not code_input.strip():
            st.warning("Please enter some code to test.")
        else:
            with st.spinner("Analyzing code style..."):
                # Create a temporary dataframe
                temp_df = pd.DataFrame([{'code': code_input, 'author': 'unknown'}])
                # Extract features
                feat_df = extract_features(temp_df)
                
                X_test = feat_df.drop(['code', 'author'], axis=1)
                
                # Predict
                author, probas = st.session_state.model.predict(X_test)
                
                st.success(f"**Predicted Author:** {author[0]}")
                
                # Show probabilities
                st.subheader("Confidence Scores")
                classes = st.session_state.model.label_encoder.classes_
                prob_dict = {classes[i]: probas[0][i] for i in range(len(classes))}
                
                # Bar chart for probabilities
                prob_df = pd.DataFrame(list(prob_dict.items()), columns=['Author', 'Probability']).set_index('Author')
                st.bar_chart(prob_df)

# --- Tab 2: Model Metrics ---
with tab2:
    st.header("Performance Metrics")
    
    if st.session_state.report is None:
        st.info("Train the model to view metrics.")
    else:
        st.subheader("Classification Report")
        report_df = pd.DataFrame(st.session_state.report).transpose()
        st.dataframe(report_df.style.background_gradient(cmap='Blues'))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if os.path.exists("results/confusion_matrix.png"):
                st.image(Image.open("results/confusion_matrix.png"), caption="Confusion Matrix", width="stretch")
                
        with col2:
            if os.path.exists("results/roc_curve.png"):
                st.image(Image.open("results/roc_curve.png"), caption="ROC Curve", width="stretch")
                
        if os.path.exists("results/pr_curve.png"):
            st.image(Image.open("results/pr_curve.png"), caption="Precision-Recall Curve", width="stretch")

# --- Tab 3: Feature Importance ---
with tab3:
    st.header("Feature Importance (Explainability)")
    
    if st.session_state.model is None:
        st.info("Train the model to view feature importance.")
    else:
        X = st.session_state.features_df.drop(['code', 'author'], axis=1)
        importance_scores = st.session_state.model.model.feature_importances_
        
        feat_imp_df = pd.DataFrame({
            'Feature': X.columns,
            'Importance': importance_scores
        }).sort_values(by='Importance', ascending=False)
        
        st.bar_chart(feat_imp_df.set_index('Feature'))
        st.markdown("**Note:** This shows which stylometric features (e.g., AST depth vs word frequency) the XGBoost model relied on most to make its decisions.")
