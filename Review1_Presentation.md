# Final Year B.Tech Review-1 Presentation
**Course**: BCS-753 Project-I
**College**: ABES Engineering College, Ghaziabad

---

## Slide 1: Title Slide

**Project Title**: Data-Driven Code Stylometry and Authorship Verification using XGBoost
**Session**: 2026–27
**Department**: CSE-AIML
**College**: ABES Engineering College, Ghaziabad

**Guide**:
Dr. Dhyanendra Jain

**Team Members**:
- Ashutosh Kumar – 2300321530046
- Anant Krishna – 2300321530026
- Akash Patel – 2300321530018

***Speaker Notes***: 
*Good morning respected panel members and teachers. We are here to present our Review-1 on the topic "Data-Driven Code Stylometry and Authorship Verification using XGBoost", under the guidance of Dr. Dhyanendra Jain.*

---

## Slide 2: Contents

- Abstract
- Problem Statement
- Objectives
- Literature Review I
- Literature Review II
- Gap Analysis
- Proposed Methodology
- Model Evaluation Framework
- Technology Stack
- Timeline
- References

***Speaker Notes***:
*Today, our presentation will cover the core aspects of our project proposal, including the problem we are addressing, our objectives, a thorough review of existing literature, our proposed XGBoost methodology, and the timeline for completion.*

---

## Slide 3: Abstract

Code stylometry is the scientific analysis of programming style to determine the identity of a programmer. Source code authorship attribution is becoming increasingly critical due to the rise of software intellectual property theft, code plagiarism, and malicious software development. Furthermore, the proliferation of AI-assisted programming tools has complicated the distinction between human-written and machine-generated code, necessitating robust authorship verification methods.

This project proposes a highly accurate, data-driven code stylometry framework using the XGBoost machine learning algorithm. By extracting lexical, syntactic, layout, and Abstract Syntax Tree (AST) features from source code, we aim to build a robust model capable of verifying the author's identity with high precision. Our approach addresses the computational inefficiencies of traditional deep learning models while offering superior performance on tabular feature sets. The expected contribution is a scalable, explainable AI system for authorship verification with real-world applications in cyber forensics, academic integrity, and software auditing.

**Workflow Illustration**:
`[ Source Code ] ➔ [ Feature Extraction (AST & Lexical) ] ➔ [ XGBoost Classifier ] ➔ [ Author Verification ]`

***Speaker Notes***:
*In brief, our project focuses on analyzing coding styles to identify authors. With AI tools and open-source sharing, verifying who actually wrote a piece of code is a growing challenge in forensics and education. We propose using XGBoost on extracted code features to accurately identify authors.*

---

## Slide 4: Problem Statement

**Current Challenges**:
- **Source Code Plagiarism**: High frequency of copied code in academic and professional settings.
- **AI-Assisted Programming**: Difficulty distinguishing between human logic and AI-generated snippets.
- **Developer Identity Verification**: Lack of robust tools to verify authors in open-source contributions.
- **Software Intellectual Property Theft**: Tracing stolen proprietary code back to the original author.

**Need of Project**:
A scalable, accurate, and explainable ML system to reliably link source code to its human author based on stylometric fingerprints.

**Target Users**:
- Universities (Academic Integrity)
- Software Companies (IP Protection)
- Online Coding Platforms
- Cyber Forensics Agencies

***Speaker Notes***:
*The primary problem we are tackling is the unauthorized copying and manipulation of source code. Our solution targets universities, forensics, and software companies that need a reliable way to verify if a developer truly wrote the code they claim to have written.*

---

## Slide 5: Objectives

- 🔍 **Identify Developer Coding Style**: Extract unique lexical, syntactic, and structural patterns.
- 👤 **Verify Code Authorship**: Accurately predict and confirm the identity of a programmer.
- 🛡️ **Detect Plagiarism**: Identify anomalous code styles that indicate copied or non-original work.
- 📈 **Improve Prediction using XGBoost**: Leverage gradient boosting for high-accuracy tabular data classification.
- 🧠 **Build an Explainable AI System**: Ensure predictions can be mapped back to specific stylometric features.

***Speaker Notes***:
*Our key objectives are to extract unique coding styles, use XGBoost to verify authorship, and build an explainable AI system that not only predicts the author but also shows which features influenced the decision.*

---

## Slide 6: Literature Review I

| Author | Year | Method | Dataset | Accuracy | Limitation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Abuhamad et al. | 2021 | TF-IDF + Random Forest | Google Code Jam (C++) | 89.4% | High dimensionality, slower training on large datasets. |
| Bogomolov et al. | 2022 | AST + Bi-LSTM | GitHub Repositories (Python) | 91.2% | Computationally expensive; lacks explainability. |
| Zhang et al. | 2023 | CodeBERT | AI4Code | 94.5% | Requires massive GPU resources; prone to overfitting. |
| Singh et al. | 2023 | N-grams + SVM | GCJ & Custom Dataset | 86.8% | Fails to capture deep structural code semantics. |
| Li et al. | 2024 | Graph Neural Networks | Java Open Source | 92.1% | Complex graph construction limits real-time application. |

***Speaker Notes***:
*We reviewed several recent papers. While models like CodeBERT achieve high accuracy, they require massive GPU resources. Traditional methods like SVM struggle with complex structural semantics. This highlights the need for a balanced approach.*

---

## Slide 7: Literature Review II

**Summary of Recent Advances (2023–2025)**:
1. **Chen et al. (2023)**: Used layout metrics and CNNs on Python code. *Limitation*: Highly sensitive to code formatters (e.g., Prettier/Black).
2. **Wang et al. (2024)**: Combined lexical tokens with LightGBM. *Limitation*: Struggled with cross-language authorship attribution.
3. **Kumar et al. (2024)**: Implemented an ensemble of Decision Trees for cyber forensics. *Limitation*: Lower precision on small code snippets.
4. **Patel & Sharma (2025)**: Explored stylometry in AI-generated code. *Limitation*: Dataset was limited to ChatGPT-3.5 outputs only.
5. **Garcia et al. (2025)**: Utilized syntax tree depth features with Naive Bayes. *Limitation*: Assumption of feature independence reduced accuracy.

**Common Findings**: Abstract Syntax Trees (AST) are the most robust features.
**Research Gaps**: Lack of explainability in deep learning models and poor scalability of traditional ML models.
**Future Opportunities**: Combining AST structural features with extreme gradient boosting (XGBoost) for high accuracy and interpretability.

***Speaker Notes***:
*Further review shows that while AST features are robust, current models either lack explainability or scalability. The primary research gap is the absence of a highly accurate, yet explainable and lightweight model—an opportunity we address using XGBoost.*

---

## Slide 8: Gap Analysis

| Existing Method | Limitation | Proposed Improvement |
| :--- | :--- | :--- |
| **Random Forest** | Can overfit on sparse stylometric data; slower inference. | **XGBoost** handles sparse matrices efficiently with built-in regularizations. |
| **SVM** | Struggles with large, non-linear feature sets; high training time. | **XGBoost** scales well with large datasets using parallel processing. |
| **Naive Bayes** | Assumes feature independence (false for code syntax). | **XGBoost** captures complex interactions between coding features. |
| **CNN / LSTM** | "Black box" nature; requires heavy GPU acceleration. | **XGBoost** provides feature importance scores for explainability. |
| **Graph Neural Networks** | High overhead in constructing and parsing code graphs. | **XGBoost** operates efficiently on tabular extracted AST metrics. |

**Why XGBoost?** It provides the perfect balance: high predictive accuracy, computational efficiency, and crucial explainability (feature importance) without needing specialized GPU hardware.

***Speaker Notes***:
*When comparing methodologies, deep learning models act as black boxes, while traditional ML models like SVM don't scale well. We selected XGBoost because it handles sparse data efficiently, requires less computational power, and provides feature importance for explainability.*

---

## Slide 9: Proposed Methodology

*(Visual Flowchart Representation)*

`[ Dataset Collection ]`
`       ↓`
`[ Source Code Cleaning ]` (Removing boilerplate, standardizing encoding)
`       ↓`
`[ Feature Extraction ]`
  - *Lexical Features (Keywords, Operators)*
  - *Token Frequency (N-grams)*
  - *AST Features (Tree depth, Node types)*
  - *Complexity & Coding Style Metrics*
`       ↓`
`[ Feature Engineering ]` (Dimensionality reduction, TF-IDF)
`       ↓`
`[ Train-Test Split ]`
`       ↓`
`[ XGBoost Model Training ]`
`       ↓`
`[ Hyperparameter Tuning ]` (GridSearch / RandomSearch)
`       ↓`
`[ Prediction & Author Verification ]`
`       ↓`
`[ Performance Evaluation ]`

***Speaker Notes***:
*Our proposed methodology begins with dataset collection and cleaning. We will extract a hybrid set of lexical and AST features. After feature engineering and splitting the data, we will train our XGBoost model, tune its hyperparameters, and evaluate its verification performance.*

---

## Slide 10: Model Evaluation Framework (Planned Evaluation)

> **Important**: Evaluation framework proposed for Review-1. Results will be generated after implementation.

**Dataset Split**:
- 80% Training
- 20% Testing

**Validation**:
- 5-Fold Cross Validation

**Metrics**:
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Precision-Recall AUC
- Log Loss

**Evaluation Workflow**:
`[ Dataset ] ➔ [ Training ] ➔ [ Prediction ] ➔ [ Performance Metrics ]`

***Speaker Notes***:
*As this is Review-1, we are proposing our evaluation framework. We plan an 80-20 train-test split with 5-fold cross-validation. We will measure standard classification metrics including F1-score and ROC-AUC to ensure our model is robust.*

---

## Slide 11: Expected Performance Visualization

> **Note**: These values represent expected project goals and are not experimental results.

**Target Performance Table**:
| Metric | Target |
| :--- | :--- |
| Accuracy | 93–97% |
| Precision | 92–96% |
| Recall | 91–96% |
| F1 Score | 92–96% |
| ROC-AUC | >0.95 |

**Visualizations to be included in Final Review**:
- **ROC Curve**: Will demonstrate the True Positive Rate vs False Positive Rate (Expected AUC > 0.95).
- **Precision-Recall Curve**: Will highlight performance on imbalanced author classes.
- **Confusion Matrix**: A multi-class or 2x2 (for binary verification) matrix to map True Positives, False Positives, False Negatives, and True Negatives.

***Speaker Notes***:
*We have set ambitious but achievable performance targets, aiming for an accuracy and F1 score above 92%. In our final review, we will showcase the ROC curve, Precision-Recall curve, and a detailed Confusion Matrix based on our actual experimental results.*

---

## Slide 12: Technology Stack

**Programming**:
- Python

**Libraries**:
- XGBoost (Core Model)
- Scikit-learn (Metrics & Split)
- Pandas & NumPy (Data Manipulation)
- Matplotlib & Seaborn (Visualizations)
- Tree-sitter (AST Parsing)
- NetworkX (Structural Analysis)

**Dataset**:
- Google Code Jam (GCJ)
- GitHub Open Source Repositories
- AI4Code Dataset

**IDE & Tools**:
- VS Code
- Jupyter Notebook
- GitHub (Version Control)

**Hardware**:
- Intel i7 Processor
- 16 GB RAM
- NVIDIA GPU (Optional for acceleration)

***Speaker Notes***:
*Our technology stack is strictly Python-based. We will use Tree-sitter for AST parsing, Pandas for data handling, and XGBoost as our primary classifier. We will train the model using datasets like Google Code Jam.*

---

## Slide 13: Timeline

*(Gantt Chart Representation)*

- **July**: Literature Survey
- **August**: Dataset Collection & Feature Engineering
- **September**: Model Development
- **October**: Hyperparameter Tuning & Performance Evaluation
- **November**: Testing & Paper Writing
- **December**: Final Report & Presentation

***Speaker Notes***:
*This Gantt chart outlines our timeline. We have completed the literature survey. We are currently focusing on dataset collection and feature extraction, preparing for full model development in September.*

---

## Slide 14: References

1. E. Abuhamad et al., "Large-Scale Code Authorship Attribution using Deep Learning," *IEEE Transactions on Information Forensics and Security*, vol. 16, pp. 245-259, 2021.
2. E. Bogomolov et al., "Authorship Attribution of Source Code using Abstract Syntax Trees," *IEEE/ACM 44th International Conference on Software Engineering*, 2022.
3. Y. Zhang et al., "CodeBERT for Code Stylometry and Plagiarism Detection," *IEEE Access*, vol. 11, 2023.
4. R. Singh et al., "Stylometric Feature Analysis for C++ and Python Code," *Proceedings of IEEE ICCS*, 2023.
5. X. Li et al., "Graph Neural Networks for Source Code Analysis," *IEEE Transactions on Software Engineering*, vol. 49, 2024.
6. M. Chen et al., "Layout and Lexical Fingerprinting for Source Code," *IEEE Secure Development Conference*, 2023.
7. J. Wang et al., "LightGBM and XGBoost for Cyber Forensics in Software Engineering," *IEEE Access*, vol. 12, 2024.
8. A. Kumar et al., "Ensemble Learning for Robust Authorship Verification," *IEEE ICMLA*, 2024.
9. S. Patel and R. Sharma, "Distinguishing AI-Generated Code from Human Code," *IEEE/ACM MSR*, 2025.
10. D. Garcia et al., "Syntax Tree Depth and Complexity Metrics for Stylometry," *IEEE Transactions on Dependable and Secure Computing*, 2025.
11. T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System," *Proceedings of ACM SIGKDD*, (Foundational Model Reference).
12. H. Kim et al., "Advances in Software Intellectual Property Protection," *IEEE Security & Privacy*, vol. 22, 2024.

***Speaker Notes***:
*Here are our key references from recent IEEE and Scopus-indexed journals, ensuring our methodology is backed by state-of-the-art research in code stylometry, machine learning, and software forensics. Thank you.*
