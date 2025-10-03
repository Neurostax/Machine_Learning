# Phase 1: Rule-Based Chatbot

## 🎯 Learning Objectives
- Understand the basics of chatbot architecture
- Learn pattern matching and response selection
- Build a functional chatbot without ML

## 📖 Theory Overview

### What is a Rule-Based Chatbot?
A rule-based chatbot follows predetermined rules and patterns to generate responses. It uses:
- **Pattern Matching**: If user input matches X, then respond with Y
- **Decision Trees**: Simple if-else logic flows
- **No Learning**: Rules are manually created

### Key Components
1. **Input Processing**: Clean and normalize user text
2. **Pattern Matching**: Find matching rules
3. **Response Selection**: Choose appropriate response
4. **Output Generation**: Return the response

## 🛠️ Implementation

### Basic Architecture
```python
class RuleBasedChatbot:
    def __init__(self):
        self.rules = {
            'greeting': {
                'patterns': ['hello', 'hi', 'hey', 'howdy'],
                'responses': ['Hello!', 'Hi there!', 'Hey! How can I help?']
            },
            'farewell': {
                'patterns': ['bye', 'goodbye', 'see you', 'quit'],
                'responses': ['Goodbye!', 'See you later!', 'Bye!']
            }
        }
    
    def find_match(self, user_input):
        user_input = user_input.lower().strip()
        for intent, data in self.rules.items():
            for pattern in data['patterns']:
                if pattern in user_input:
                    return intent
        return None

## Start by first visiting the Example folder 
In the examples folder , Go through the .md file  documentation understand how a rule based chatbot works and the run the example to interact with it .

## 🎯 Fully Working Example explanation in examples folder

### Advanced Rule-Based Chatbot
We've provided a complete, fully functional chatbot in `sample_bot.py` that demonstrates:

**Features:**
- 12 different intent categories
- 1000+ words of response possibilities
- Context awareness (remembers your name)
- Natural language processing with regex
- Fallback responses for unknown inputs
- Error handling and graceful degradation

**Key Learning Points:**
1. **Pattern Matching**: How to match user input to predefined patterns
2. **Response Selection**: Random selection from multiple appropriate responses
3. **Context Management**: Remembering user information across conversations
4. **Input Processing**: Cleaning and normalizing user input
5. **Extensibility**: Easy to add new intents and responses

### Running the Example
```bash
python sample_bot.py


### After running and seeing how it works you can try to implement the logic on the code Bot.py 


# 💻 Hands-On Exercise
## Exercise 1: Basic Rule Bot
Create a simple chatbot that can handle:

Greetings (hello, hi, hey)

Farewells (bye, goodbye)

Simple questions (how are you, what's your name)