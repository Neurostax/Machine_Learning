"""
Data Preparation for ML Chatbot
Handles dataset loading, preprocessing, and splitting
"""

import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class IntentDataPreprocessor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None
        self.df = None
        self.label_encoder = LabelEncoder()
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        
    def load_data(self):
        """Load intent data from JSON file"""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        return self.data
    
    def preprocess_text(self, text):
        """Clean and preprocess text data"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize and remove stopwords
        tokens = text.split()
        tokens = [token for token in tokens if token not in self.stop_words]
        
        # Apply stemming
        tokens = [self.stemmer.stem(token) for token in tokens]
        
        return ' '.join(tokens)
    
    def create_training_data(self):
        """Create training data from intents"""
        if not self.data:
            self.load_data()
            
        patterns = []
        labels = []
        
        for intent in self.data['intents']:
            for pattern in intent['patterns']:
                # Preprocess each pattern
                processed_pattern = self.preprocess_text(pattern)
                patterns.append(processed_pattern)
                labels.append(intent['tag'])
        
        # Create DataFrame
        self.df = pd.DataFrame({
            'text': patterns,
            'label': labels
        })
        
        # Encode labels
        encoded_labels = self.label_encoder.fit_transform(labels)
        
        return patterns, encoded_labels
    
    def split_data(self, test_size=0.2, random_state=42):
        """Split data into training and test sets"""
        if self.df is None:
            self.create_training_data()
            
        X = self.df['text']
        y = self.df['label']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        return X_train, X_test, y_train, y_test
    
    def get_label_mapping(self):
        """Get mapping between encoded labels and original tags"""
        return dict(zip(
            self.label_encoder.classes_, 
            range(len(self.label_encoder.classes_))
        ))
    
    def get_class_distribution(self):
        """Get distribution of classes in the dataset"""
        if self.df is not None:
            return self.df['label'].value_counts()
        return None

# Example usage
if __name__ == "__main__":
    preprocessor = IntentDataPreprocessor('intents.json')
    X, y = preprocessor.create_training_data()
    X_train, X_test, y_train, y_test = preprocessor.split_data()
    
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Number of classes: {len(preprocessor.label_encoder.classes_)}")
    print("Class distribution:")
    print(preprocessor.get_class_distribution())