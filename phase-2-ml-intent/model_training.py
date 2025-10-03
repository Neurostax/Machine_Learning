"""
Model Training for Intent Classification
Trains and evaluates multiple ML algorithms
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score, GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import time

class IntentClassifierTrainer:
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.vectorizer = None
        self.results = {}
        
    def create_pipelines(self):
        """Create ML pipelines with different algorithms"""
        self.models = {
            'naive_bayes': Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=5000,
                    ngram_range=(1, 2),
                    stop_words='english',
                    min_df=2,
                    max_df=0.8
                )),
                ('classifier', MultinomialNB(alpha=0.1))
            ]),
            
            'svm': Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=5000,
                    ngram_range=(1, 2),
                    stop_words='english',
                    min_df=2,
                    max_df=0.8
                )),
                ('classifier', SVC(
                    kernel='linear',
                    C=1.0,
                    probability=True,
                    random_state=42
                ))
            ]),
            
            'logistic_regression': Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=5000,
                    ngram_range=(1, 2),
                    stop_words='english',
                    min_df=2,
                    max_df=0.8
                )),
                ('classifier', LogisticRegression(
                    C=1.0,
                    max_iter=1000,
                    random_state=42,
                    multi_class='ovr'
                ))
            ]),
            
            'random_forest': Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=5000,
                    ngram_range=(1, 2),
                    stop_words='english',
                    min_df=2,
                    max_df=0.8
                )),
                ('classifier', RandomForestClassifier(
                    n_estimators=100,
                    random_state=42,
                    max_depth=10
                ))
            ])
        }
    
    def train_models(self, X_train, y_train):
        """Train all models and measure training time"""
        self.create_pipelines()
        self.results = {}
        
        for name, model in self.models.items():
            print(f"Training {name}...")
            start_time = time.time()
            
            model.fit(X_train, y_train)
            
            training_time = time.time() - start_time
            self.results[name] = {
                'model': model,
                'training_time': training_time
            }
            
            print(f"  {name} trained in {training_time:.2f} seconds")
    
    def evaluate_models(self, X_test, y_test):
        """Evaluate all models on test data"""
        for name in self.models.keys():
            model = self.results[name]['model']
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            self.results[name]['accuracy'] = accuracy
            self.results[name]['predictions'] = y_pred
            
            print(f"{name.upper():<20} Accuracy: {accuracy:.4f}")
    
    def get_best_model(self):
        """Select the best performing model"""
        best_accuracy = 0
        best_model_name = None
        
        for name, result in self.results.items():
            if result['accuracy'] > best_accuracy:
                best_accuracy = result['accuracy']
                best_model_name = name
        
        if best_model_name:
            self.best_model = self.results[best_model_name]['model']
            print(f"\nBest model: {best_model_name} with accuracy: {best_accuracy:.4f}")
            return self.best_model
        
        return None
    
    def detailed_classification_report(self, X_test, y_test, label_encoder):
        """Generate detailed classification report for best model"""
        if self.best_model:
            y_pred = self.best_model.predict(X_test)
            
            # Convert encoded labels back to original names
            y_test_labels = label_encoder.inverse_transform(y_test)
            y_pred_labels = label_encoder.inverse_transform(y_pred)
            
            print("\nDetailed Classification Report:")
            print(classification_report(y_test_labels, y_pred_labels))
            
            return classification_report(y_test_labels, y_pred_labels, output_dict=True)
        return None
    
    def plot_confusion_matrix(self, X_test, y_test, label_encoder, figsize=(12, 10)):
        """Plot confusion matrix for best model"""
        if self.best_model:
            y_pred = self.best_model.predict(X_test)
            y_test_labels = label_encoder.inverse_transform(y_test)
            y_pred_labels = label_encoder.inverse_transform(y_pred)
            
            cm = confusion_matrix(y_test_labels, y_pred_labels, 
                                labels=label_encoder.classes_)
            
            plt.figure(figsize=figsize)
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                       xticklabels=label_encoder.classes_,
                       yticklabels=label_encoder.classes_)
            plt.title('Confusion Matrix')
            plt.xlabel('Predicted')
            plt.ylabel('Actual')
            plt.xticks(rotation=45)
            plt.yticks(rotation=0)
            plt.tight_layout()
            plt.show()
    
    def save_model(self, filepath):
        """Save the best model to disk"""
        if self.best_model:
            joblib.dump(self.best_model, filepath)
            print(f"Model saved to {filepath}")
        else:
            print("No model to save. Train a model first.")
    
    def save_vectorizer(self, filepath):
        """Save the TF-IDF vectorizer to disk"""
        if self.best_model:
            vectorizer = self.best_model.named_steps['tfidf']
            joblib.dump(vectorizer, filepath)
            print(f"Vectorizer saved to {filepath}")

# Example usage
if __name__ == "__main__":
    from data_preparation import IntentDataPreprocessor
    
    # Load and prepare data
    preprocessor = IntentDataPreprocessor('intents.json')
    X_train, X_test, y_train, y_test = preprocessor.split_data()
    
    # Train models
    trainer = IntentClassifierTrainer()
    trainer.train_models(X_train, y_train)
    trainer.evaluate_models(X_test, y_test)
    trainer.get_best_model()
    
    # Generate detailed reports
    trainer.detailed_classification_report(X_test, y_test, preprocessor.label_encoder)
    trainer.plot_confusion_matrix(X_test, y_test, preprocessor.label_encoder)
    
    # Save the best model
    trainer.save_model('best_intent_classifier.joblib')
    trainer.save_vectorizer('tfidf_vectorizer.joblib')