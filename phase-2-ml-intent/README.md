# In this Phase 2, we'll add Machine Learning to automatically understand user intent!

```
 /phase-1-rule-based/requirements.txt
```


## 🤖 Phase 2: ML-Powered Intent Classification
```
 /phase-2-ml-intent/README.md
```
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

# In this phase we use porterstemmer to show you how stemming works  though it's not the best

🎯 The Core Problem: Word Variation
Natural language is messy! Humans use different forms of the same word:

"walk", "walking", "walked", "walks"

"happy", "happier", "happiest", "happiness"

"compute", "computer", "computation", "computing"

Without stemming, our chatbot would treat these as completely different words, missing important semantic connections.


🧠 The Stemming Solution
Stemming reduces words to their root form, allowing our model to recognize that different variations of a word convey similar meaning:

Original Word	Stemmed Form	Meaning Preserved
"walking"	"walk"	✅
"walked"	"walk"	✅
"walks"	"walk"	✅
"happiness"	"happi"	✅
"happier"	"happi"	✅



📊 Impact on Model Performance
Before Stemming:

```
Vocabulary Size: ~2,000 words
Pattern: "I am walking" → ["i", "am", "walking"]
Pattern: "I walked yesterday" → ["i", "walked", "yesterday"]
Pattern: "She walks daily" → ["she", "walks", "daily"]

```
Result: Model treats "walking", "walked", "walks" as unrelated words

After Stemming:
```
Vocabulary Size: ~1,200 words (40% reduction!)
Pattern: "I am walking" → ["i", "am", "walk"]
Pattern: "I walked yesterday" → ["i", "walk", "yesterday"]
Pattern: "She walks daily" → ["she", "walk", "daily"]
```

Result: Model recognizes all walking-related patterns as similar

🚀 Key Benefits in Our Chatbot
1. Reduced Vocabulary Size
40-50% smaller vocabulary = faster training & inference

Less memory usage

More efficient pattern matching

2. Improved Pattern Recognition

# User might say:
```
"Can you help me with walking?"
"I need help with walked exercises"
"Walking assistance required"
```
# All get stemmed to:
```
["help", "walk"] → Triggers appropriate intent
```

3. Better Generalization
The model learns that:

"I love walking in the park"

"I walked to school today"

"She walks every morning"

All express the same core concept of walking, making the chatbot more robust to different phrasing.

4. Handling Unknown Variations
Even if the training data only contains "walking", stemming ensures the model can understand "walked" and "walks" in user inputs.


⚖️ Trade-offs
Pros ✅	Cons ❌
Smaller vocabulary	Some meaning loss
Better generalization	Over-stemming issues
Faster processing	Language-specific
Robust to variations	Not perfect for all cases



# Why We will Upgrade from PorterStemmer to Lemmatization in Phase 3

🔄 Evolution from Phase 2 to Phase 3
Phase 2: PorterStemmer (Simple but Aggressive)
python


from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
```
"running" → "run"
"happily" → "happili"  # ❌ Not a real word
"better" → "better"    # ❌ No change
"went" → "went"        # ❌ No change (can't handle irregular verbs)
```
# In the next phase 
## Phase 3: WordNet Lemmatizer (Intelligent and Linguistic)

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Examples:
```
"running" → "run"      # ✅
"happily" → "happy"    # ✅ Real word
"better" → "good"      # ✅ Handles comparatives
"went" → "go"          # ✅ Handles irregular verbs
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
