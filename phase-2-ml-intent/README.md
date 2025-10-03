# In this Phase 2, we'll add Machine Learning to automatically understand user intent!

### `/phase-1-rule-based/requirements.txt`



## 🤖 Phase 2: ML-Powered Intent Classification

### `/phase-2-ml-intent/README.md`


# Phase 2: ML-Powered Intent Classification

## 🎯 Learning Objectives
- Understand NLP preprocessing techniques
- Learn about feature extraction (Bag-of-Words, TF-IDF)
- Build and train intent classification models
- Compare different ML algorithms

## 📖 Theory Overview

### Moving Beyond Rules
Rule-based systems don't scale well. ML helps by:
- **Learning patterns** from data automatically
- **Generalizing** to unseen inputs
- **Handling variations** in user language

### NLP Pipeline
1. **Text Preprocessing**
   - Tokenization
   - Lowercasing
   - Removing stopwords/punctuation
   - Stemming/Lemmatization

2. **Feature Extraction**
   - **Bag-of-Words (BoW)**: Word frequency vectors
   - **TF-IDF**: Term Frequency-Inverse Document Frequency
   - **Word Embeddings** (next phase)

3. **Classification Algorithms**
   - Naive Bayes
   - Support Vector Machines (SVM)
   - Logistic Regression

## 🛠️ Implementation

### Dataset Structure
We'll use intent-based datasets:
```json
{
    "intents": [
        {
            "tag": "greeting",
            "patterns": ["hello", "hi", "hey there", "good morning"],
            "responses": ["Hello!", "Hi!", "Hey! How can I help?"]
        }
    ]
}





```

# 📋 Assignment
Part 1: Compare ML Algorithms
Compare three different classifiers:

Naive Bayes

SVM

Logistic Regression

Report on:

Accuracy scores

Training time

Prediction speed




# Part 2: Build a Customer Service Bot
Create a dataset with these intents:

product_inquiry

shipping_info

return_policy

complaint

support_request
