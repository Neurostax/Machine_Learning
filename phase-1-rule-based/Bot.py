# bot.py
class SimpleChatbot:
    def __init__(self):
        self.rules = {
            'greeting': {
                'patterns': ['hello', 'hi', 'hey', 'hola'],
                'responses': ['Hello!', 'Hi there!', 'Hey!']
            },
            'farewell': {
                'patterns': ['bye', 'goodbye', 'see you', 'quit'],
                'responses': ['Goodbye!', 'See you later!', 'Bye! Take care!']
            },
            'how_are_you': {
                'patterns': ['how are you', 'how do you do', "what's up"],
                'responses': ["I'm just a bot, but I'm functioning well!", "All systems operational!"]
            }
        }
    
    def respond(self, message):
        message = message.lower().strip()
        
        # Your code here: Implement pattern matching
        # Hint: Check if any pattern from each intent is in the message
        
        return "I'm not sure how to respond to that."

# Test your bot
if __name__ == "__main__":
    bot = SimpleChatbot()
    print("Chatbot: Hello! Type 'quit' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = bot.respond(user_input)
        print(f"Bot: {response}")