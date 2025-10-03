"""
ML-Powered Chatbot
Main chatbot application using trained ML model
"""

import json
import random
import joblib
import numpy as np
from data_preparation import IntentDataPreprocessor
from model_training import IntentClassifierTrainer
import re

class MLChatbot:
    def __init__(self, intents_file, model_file=None, vectorizer_file=None):
        self.intents_file = intents_file
        self.model_file = model_file
        self.vectorizer_file = vectorizer_file
        
        # Load intents data
        self.preprocessor = IntentDataPreprocessor(intents_file)
        self.intents_data = self.preprocessor.load_data()
        self.intents = self.intents_data['intents']
        
        # Initialize model and vectorizer
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        
        # Context tracking
        self.context = {}
        self.conversation_history = []
        
        # Load or train model
        if model_file and vectorizer_file:
            self.load_model(model_file, vectorizer_file)
        else:
            self.train_model()
    
    def train_model(self):
        """Train the intent classification model"""
        print("Training ML model...")
        
        # Prepare data
        X, y = self.preprocessor.create_training_data()
        X_train, X_test, y_train, y_test = self.preprocessor.split_data()
        self.label_encoder = self.preprocessor.label_encoder
        
        # Train models
        trainer = IntentClassifierTrainer()
        trainer.train_models(X_train, y_train)
        trainer.evaluate_models(X_test, y_test)
        trainer.get_best_model()
        
        self.model = trainer.best_model
        self.vectorizer = self.model.named_steps['tfidf']
        
        print("Model training completed!")
    
    def load_model(self, model_file, vectorizer_file):
        """Load pre-trained model and vectorizer"""
        try:
            self.model = joblib.load(model_file)
            self.vectorizer = joblib.load(vectorizer_file)
            self.label_encoder = self.preprocessor.label_encoder
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Training new model instead...")
            self.train_model()
    
    def preprocess_input(self, text):
        """Preprocess user input using the same method as training"""
        return self.preprocessor.preprocess_text(text)
    
    def predict_intent(self, user_input):
        """Predict intent from user input"""
        if not self.model:
            raise ValueError("Model not loaded or trained")
        
        # Preprocess input
        processed_input = self.preprocess_input(user_input)
        
        # Predict intent
        prediction = self.model.predict([processed_input])[0]
        confidence = np.max(self.model.predict_proba([processed_input]))
        
        # Convert back to intent tag
        intent_tag = self.label_encoder.inverse_transform([prediction])[0]
        
        return intent_tag, confidence, processed_input
    
    def get_response(self, intent_tag, confidence_threshold=0.6):
        """Get response for predicted intent"""
        if confidence_threshold and confidence < confidence_threshold:
            return self.get_fallback_response()
        
        for intent in self.intents:
            if intent['tag'] == intent_tag:
                response = random.choice(intent['responses'])
                return response
        
        return self.get_fallback_response()
    
    def get_fallback_response(self):
        """Get response when intent is not recognized"""
        fallback_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "That's interesting! Could you tell me more?",
            "I'm still learning. Could you try asking in a different way?",
            "I want to make sure I understand correctly. Could you elaborate?",
            "That's outside my current knowledge. Maybe ask me something else?",
            "I'm designed to help with various topics. Could you try rephrasing?",
            "I appreciate your message! Could you provide more context?",
            "I'm here to assist you. Could you clarify what you mean?",
            "That's given me something to think about! Want to try another topic?",
            "I'm constantly learning. Could you ask me something different?"
        ]
        return random.choice(fallback_responses)
    
    def update_context(self, user_input, intent_tag, response):
        """Update conversation context"""
        self.conversation_history.append({
            'user_input': user_input,
            'intent': intent_tag,
            'response': response,
            'timestamp': np.datetime64('now')
        })
        
        # Keep only last 10 messages
        if len(self.conversation_history) > 10:
            self.conversation_history.pop(0)
    
    def chat(self):
        """Main chat loop"""
        print("🤖 ML-Powered Chatbot: Hello! I'm now using Machine Learning!")
        print("💡 I can understand your intent and respond appropriately")
        print("💬 Type 'quit' to end our conversation\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    print("Bot: I notice you didn't type anything. Is everything okay?")
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("Bot: Thank you for chatting! I'm learning from every conversation!")
                    break
                
                # Predict intent and get response
                intent_tag, confidence, processed_input = self.predict_intent(user_input)
                response = self.get_response(intent_tag)
                
                # Update context
                self.update_context(user_input, intent_tag, response)
                
                # Display response with confidence (for educational purposes)
                print(f"Bot: {response}")
                print(f"    [Detected: {intent_tag} | Confidence: {confidence:.2f}]")
                
            except KeyboardInterrupt:
                print("\n\nBot: Thanks for the conversation! Come back anytime!")
                break
            except Exception as e:
                print(f"Bot: I encountered an error: {str(e)}")
                print("Let's continue our conversation!")
    
    def evaluate_on_test_set(self):
        """Evaluate model performance on test set"""
        from sklearn.metrics import accuracy_score, classification_report
        
        X_train, X_test, y_train, y_test = self.preprocessor.split_data()
        y_pred = self.model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        y_test_labels = self.label_encoder.inverse_transform(y_test)
        y_pred_labels = self.label_encoder.inverse_transform(y_pred)
        
        print(f"Model Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test_labels, y_pred_labels))
        
        return accuracy

# Example usage
if __name__ == "__main__":
    # Initialize chatbot (will train if no model files provided)
    chatbot = MLChatbot(
        intents_file='intents.json',
        model_file='best_intent_classifier.joblib',
        vectorizer_file='tfidf_vectorizer.joblib'
    )
    
    # Start chatting
    chatbot.chat()
    
    # Optional: Evaluate model performance
    # chatbot.evaluate_on_test_set()