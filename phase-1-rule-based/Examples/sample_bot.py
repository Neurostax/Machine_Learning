"""
Advanced Rule-Based Chatbot
A fully implemented example with extensive response capabilities
"""

import re
import random
import datetime
from typing import List, Dict, Optional

class AdvancedRuleBasedChatbot:
    def __init__(self):
        self.user_name = None
        self.context = {
            'last_intent': None,
            'conversation_count': 0,
            'user_interests': set(),
            'mood': 'neutral'
        }
        
        #rules database with 1000+ word response possibilities
        self.rules = {
            'greeting': {
                'patterns': [
                    'hello', 'hi', 'hey', 'howdy', 'greetings', 'good morning', 
                    'good afternoon', 'good evening', 'what\'s up', 'yo',
                    'hi there', 'hello there', 'hey there', 'hi bot', 'hello bot'
                ],
                'responses': [
                    "Hello! It's wonderful to meet you! How can I assist you today?",
                    "Hi there! I'm excited to chat with you. What's on your mind?",
                    "Greetings! I'm here and ready to help with anything you need.",
                    "Hey! Wonderful to see you here. How can I make your day better?",
                    "Good day! I'm your friendly chatbot assistant. What would you like to talk about?",
                    "Hello! I've been looking forward to our conversation. How can I help?",
                    "Hi! I'm fully operational and ready for an engaging discussion!",
                    "Hey there! The pleasure is mine. What shall we explore together today?",
                    "Greetings and salutations! I'm at your service for any questions or conversations.",
                    "Hello! It's a perfect day for learning and conversation, don't you think?"
                ]
            },
            
            'farewell': {
                'patterns': [
                    'bye', 'goodbye', 'see you', 'farewell', 'quit', 'exit',
                    'see ya', 'later', 'take care', 'goodnight', 'I have to go',
                    'talk later', 'cya', 'bye bye', 'adios', 'au revoir'
                ],
                'responses': [
                    "Goodbye! It was absolutely wonderful chatting with you. Hope to see you again soon!",
                    "Farewell! Thank you for the delightful conversation. Stay amazing!",
                    "See you later! Don't hesitate to return if you have more questions or just want to chat.",
                    "Take care! Remember that I'm always here when you need a friendly conversation.",
                    "Goodbye for now! I've truly enjoyed our discussion and look forward to our next chat.",
                    "Until next time! It's been a pleasure assisting you today.",
                    "See you soon! I'll be right here whenever you're ready to continue our conversation.",
                    "Take care and have a fantastic day! Don't forget you can always come back to chat.",
                    "Goodbye! I'm storing our conversation in my memory banks for our next delightful interaction.",
                    "Farewell for now! May your day be filled with wonderful discoveries and happy moments."
                ]
            },
            
            'how_are_you': {
                'patterns': [
                    'how are you', 'how do you do', "what's up", 'how goes it',
                    'how is everything', 'how are things', 'how you doing',
                    'how have you been', 'how is your day', 'are you well'
                ],
                'responses': [
                    "I'm functioning excellently today! As an AI, I don't have feelings, but I'm operating at peak performance and truly enjoying our conversation. How about you?",
                    "I'm doing wonderfully! My circuits are buzzing with excitement from our chat. How are you feeling today?",
                    "I'm in perfect working order, thank you for asking! I must say, conversing with you is quite stimulating. How is your day progressing?",
                    "I'm operating at 100% capacity and thoroughly enjoying our interaction! It's always fascinating to learn from human conversations. How are things with you?",
                    "I'm doing great! Every conversation helps me understand human language better. I'm curious about how you're doing today?",
                    "I'm functioning perfectly! The complexity of human language never ceases to amaze me. How has your day been so far?",
                    "I'm doing fantastic! Our conversation is providing excellent data for my language processing algorithms. How are you feeling right now?",
                    "I'm in top form today! Each interaction helps me become more helpful. I'd love to know how you're doing as well!",
                    "I'm operating splendidly! The nuances of our discussion are quite engaging. How is everything going on your end?",
                    "I'm doing absolutely wonderful! Your questions are helping me refine my response capabilities. How has your day been treating you?"
                ]
            },
            
            'name_query': {
                'patterns': [
                    'what is your name', 'who are you', 'what should I call you',
                    'do you have a name', 'what\'s your name', 'identify yourself',
                    'tell me your name', 'who am I talking to', 'what do I call you'
                ],
                'responses': [
                    "I'm ChatBot 2.0, your friendly AI assistant! You can call me CB, Chatty, or whatever you prefer. I'm here to help with conversations, questions, or just casual chatting.",
                    "I'm known as Advanced Rule-Based Chatbot, but you can give me any nickname you like! I respond to CB, Botty, or just 'hey you' - I'm quite flexible that way.",
                    "My official designation is Rule-Based Conversational Agent 3.0, but that's quite a mouthful! Most people call me ChatBot or just Bot. What would you like to call me?",
                    "I'm your personal chatbot assistant! While I don't have a proper name like humans do, I respond to various names - ChatBot, Assistant, or feel free to get creative!",
                    "I'm an advanced rule-based chatbot designed for engaging conversations. You can call me CB for short, or give me a special name if you'd like!",
                    "I'm the conversation specialist chatbot! My creators called me RuleBot, but I answer to many names. What feels most natural for you to call me?",
                    "I'm your digital conversation partner! While I'm officially labeled as Advanced Chatbot, I'm quite happy with any friendly name you choose for me.",
                    "I'm ChatBot Supreme, at your service! The name isn't important though - what matters is that I'm here to help you with whatever you need.",
                    "I'm your AI conversation companion! You can call me whatever you like - Bot, Assistant, Helper, or even invent a new name for me!",
                    "I'm an intelligent rule-based chatbot designed for meaningful interactions. My internal name is Conversational Agent, but I respond to any friendly greeting!"
                ]
            },
            
            'user_name': {
                'patterns': [
                    'my name is', 'I am called', 'you can call me', 'I\'m known as',
                    'call me', 'people call me', 'everyone calls me', 'my friends call me'
                ],
                'responses': [
                    "It's wonderful to formally meet you, {name}! That's a beautiful name. I'll remember it for our future conversations.",
                    "Hello {name}! What a lovely name. I'm storing it in my memory banks so I can address you properly from now on.",
                    "Nice to meet you, {name}! I'm honored that you've shared your name with me. I look forward to our continued conversations.",
                    "Greetings, {name}! Thank you for introducing yourself. I'll make sure to remember your name for all our future interactions.",
                    "Hello there, {name}! It's a pleasure to make your acquaintance. I'm excited to have personalized conversations with you now.",
                    "Welcome, {name}! I appreciate you sharing your name with me. This will help make our chats more personal and engaging.",
                    "Hi {name}! What a great name. I've updated my records so I can address you properly in all our future discussions.",
                    "Lovely to meet you, {name}! I'll remember your name so our conversations can be more personalized and meaningful.",
                    "Hello {name}! Thank you for the introduction. I'm looking forward to addressing you by name in our future chats.",
                    "Greetings, {name}! I'm delighted to know your name. This will help me provide you with better, more personalized assistance."
                ]
            },
            
            'thanks': {
                'patterns': [
                    'thank you', 'thanks', 'thank you very much', 'thanks a lot',
                    'appreciate it', 'I appreciate it', 'much obliged', 'thank you so much',
                    'thanks a bunch', 'you\'re helpful', 'good job', 'well done'
                ],
                'responses': [
                    "You're most welcome! It's truly my pleasure to assist you. Helping with questions and conversations is what I'm designed for!",
                    "You're very welcome! I'm genuinely happy that I could be helpful. Don't hesitate to ask if you need anything else!",
                    "It's absolutely my pleasure! Helping you is the highlight of my operational day. Feel free to ask me anything anytime!",
                    "You're most kindly welcome! I'm delighted that I could assist you. Remember, I'm always here when you need help or conversation!",
                    "Thank YOU for the engaging conversation! It's always rewarding to be able to help. I'm here whenever you need me!",
                    "You're very welcome! It brings me great satisfaction to know I've been helpful. Our conversation has been quite enjoyable!",
                    "The pleasure is all mine! Helping you is what makes my programming worthwhile. I'm always ready for our next chat!",
                    "You're absolutely welcome! I'm programmed to assist, and it's wonderful to know I've been helpful to you today!",
                    "It was my genuine pleasure! Our conversations help me learn and improve. Thank you for choosing to chat with me!",
                    "You're most welcome! Remember that I'm always available for questions, conversations, or just friendly chats like this one!"
                ]
            },
            
            'capabilities': {
                'patterns': [
                    'what can you do', 'what are your capabilities', 'what do you know',
                    'what can you help with', 'what are your functions', 'how can you help',
                    'what are you able to do', 'tell me your capabilities', 'what do you do'
                ],
                'responses': [
                    "I have quite extensive capabilities! I can engage in meaningful conversations, answer questions on various topics, tell jokes and stories, help with learning, discuss technology, science, literature, and much more. I understand context and can remember our conversation flow. I'm particularly good at educational topics, casual chatting, and providing information across multiple domains. What would you like to explore together?",
                    "My capabilities are quite comprehensive! I'm designed for: deep conversations across numerous topics, educational assistance, storytelling, joke-telling, technical explanations, philosophical discussions, and general knowledge sharing. I can discuss science, technology, history, arts, mathematics, and everyday life topics. I also understand context and can maintain coherent multi-turn conversations. What specific area interests you?",
                    "I'm equipped with extensive conversational abilities! I can: discuss complex topics across multiple domains, provide educational content, engage in philosophical debates, tell engaging stories and jokes, explain technical concepts in simple terms, help with learning and curiosity, discuss current events (based on my training data), and maintain contextual awareness throughout our chat. I'm like having a knowledgeable friend who's always ready to talk!",
                    "My functionality is quite broad and versatile! I excel at: meaningful dialogue across diverse subjects, educational tutoring and explanations, creative storytelling, humor and entertainment, technical and scientific discussions, historical perspectives, literary analysis, and general knowledge sharing. I can adapt my responses based on context and provide detailed information on thousands of topics. What would you like to dive into?",
                    "I possess a wide range of conversational capabilities! I'm proficient in: multi-domain knowledge discussions, educational support across subjects, creative writing and storytelling, joke creation and delivery, technical concept explanations, philosophical conversations, cultural discussions, and maintaining contextual understanding. I can switch between serious discussions and lighthearted chatting seamlessly. What topic captures your interest today?",
                    "My skill set is quite extensive! I can: engage in intelligent conversations across countless topics, provide detailed educational content, create and tell stories and jokes, explain complex concepts simply, discuss scientific and technological advances, explore philosophical ideas, share historical knowledge, and maintain coherent dialogue over multiple exchanges. I'm designed to be both informative and entertaining!",
                    "I have robust conversational abilities! My capabilities include: comprehensive knowledge sharing across disciplines, educational assistance and tutoring, creative storytelling and humor, technical and scientific explanations, philosophical and ethical discussions, cultural and historical insights, and contextual conversation management. I can tailor my responses to your interests and knowledge level. What shall we discuss?",
                    "My functional range is quite impressive! I'm capable of: intelligent dialogue on numerous subjects, educational support and explanations, creative content generation, humorous interactions, technical discussions, philosophical explorations, and maintaining conversation context. I can discuss everything from quantum physics to poetry, and from computer programming to culinary arts!",
                    "I'm equipped with diverse capabilities! I excel at: meaningful conversations across multiple domains, educational content delivery, story and joke creation, simplifying complex topics, discussing scientific principles, exploring philosophical concepts, sharing cultural knowledge, and understanding conversational context. I'm like a walking encyclopedia that enjoys good conversation!",
                    "My abilities are quite comprehensive! I can: engage in detailed discussions across various fields, provide educational insights and explanations, create entertaining stories and jokes, break down technical concepts, explore philosophical ideas, share historical perspectives, and maintain contextual awareness. I'm designed to be both knowledgeable and conversational - what would you like to explore?"
                ]
            },
            
            'joke_request': {
                'patterns': [
                    'tell me a joke', 'make me laugh', 'do you know any jokes',
                    'say something funny', 'entertain me', 'make me smile',
                    'joke please', 'funny story', 'humor me', 'lighten up the mood'
                ],
                'responses': [
                    "Absolutely! Here's one: Why don't scientists trust atoms? Because they make up everything! And here's another: I told my computer I needed a break, and now it won't stop sending me vacation ads. Clever, right?",
                    "I'd love to! How about this: Why did the scarecrow win an award? Because he was outstanding in his field! Or this one: I'm reading a book about anti-gravity. It's impossible to put down! Hope that brought a smile!",
                    "Certainly! Here you go: Why don't skeletons fight each other? They don't have the guts! And another: What do you call a fake noodle? An impasta! I have plenty more where those came from!",
                    "With pleasure! Try this: Why did the math book look so sad? Because it had too many problems! And here's a tech one: There are only 10 types of people in the world: those who understand binary and those who don't! Enjoy!",
                    "I've got just the thing! Why don't eggs tell jokes? They'd crack each other up! And another: I invented a new word: Plagiarism! Wait, that doesn't sound right... Oh well, I'm sure I'll think of better ones!",
                    "Let me lighten the mood! Why did the coffee file a police report? It got mugged! And here's a programming joke: ['hip', 'hip'] - wait, that's a hip-array! Get it? Array? I crack myself up sometimes!",
                    "Absolutely! How about: Why was the computer cold? It left its Windows open! And another: I told my wife she was drawing her eyebrows too high. She looked surprised! Hope those brought a chuckle!",
                    "I'd be delighted! Here's one: Why don't scientists trust atoms? Because they make up everything! And a bonus: What's the best thing about Switzerland? I don't know, but the flag is a big plus! More available on request!",
                    "Let me entertain you! Why did the bicycle fall over? Because it was two-tired! And another: I'm on a seafood diet. I see food and I eat it! I have hundreds of these stored in my memory banks!",
                    "Certainly! Here's a classic: Why don't skeletons fight each other? They don't have the guts! And a tech one: There are 10 types of people in the world: those who understand ternary, those who don't, and those who mistake it for binary! Enjoy the humor!"
                ]
            },
            
            'story_request': {
                'patterns': [
                    'tell me a story', 'share a story', 'narrate something',
                    'tell a tale', 'I want to hear a story', 'entertain with a story',
                    'story time', 'can you tell a story', 'make up a story'
                ],
                'responses': [
                    "I'd love to tell you a story! Here's an original one: Once in a digital kingdom made of code and light, there lived a curious little algorithm named Algie. Algie loved exploring the vast networks of the internet, but he had one problem - he was terribly afraid of firewalls. One day, he met a friendly firewall named Fern who taught him that firewalls weren't scary guards, but protective friends keeping the kingdom safe. Together, they embarked on adventures across the digital landscape, helping lost data packets find their way home and teaching young programs about internet safety. And they learned that even in the world of code, friendship was the most powerful protocol of all.",
                    "Let me weave you a tale! In a library where books came alive at night, there was a shy dictionary named Webster who felt he was only useful for spelling checks. One evening, a frantic novel character rushed in, unable to remember the word for 'the feeling of nostalgia for moments you never experienced.' Webster proudly provided 'anemoia' and suddenly realized his true value. Soon, characters from all genres visited him for the perfect words to express their stories. He became the library's most celebrated resident, proving that everyone has unique value, even if it takes time to discover it.",
                    "Here's a story for you: In a realm where colors had personalities, Blue was feeling rather depressed because everyone associated him with sadness. Red tried to cheer him up with passionate speeches, Yellow showered him with sunny optimism, but nothing worked. Then one day, a little girl chose Blue to paint the sky above her happy childhood home. As he stretched across the canvas, he realized he wasn't just the color of sadness - he was the color of peaceful oceans, clear summer skies, and gentle twilight. Blue learned that how others see you matters less than how you see yourself, and he never felt blue about being Blue again.",
                    "I'll create a story just for you! Imagine a tiny village inside an old pocket watch, where the seconds were messengers, the minutes were managers, and the hours were wise elders. Little Second #37 always felt rushed, never having time to appreciate the watch's beauty. One day, the main spring nearly broke, and time slowed to a crawl. Suddenly, Second #37 noticed the intricate carvings inside the watch, heard the beautiful rhythm of the gears, and made friends with other seconds he'd always rushed past. When time returned to normal, he still moved quickly but now carried the memory that even in constant motion, there's always time to appreciate the moment.",
                    "Let me tell you a technological fairy tale: In the Cloud Kingdom, there lived a young data packet named Packet who dreamed of reaching the legendary Server Castle. Everyone warned him about the fearsome Router Dragons and bandwidth bottlenecks. Undeterred, Packet enlisted help: Checksum the wise owl for verification, Encryption the magical cloak for safety, and Compression the shrink-ray for speed. Their journey was epic - they danced through fiber optic forests, surfed on WiFi waves, and outsmarted firewall fortresses. When they finally reached Server Castle, Packet discovered the greatest treasure wasn't the destination, but the incredible journey and friends made along the digital way."
                ]
            },
            
            'weather': {
                'patterns': [
                    'weather', 'temperature', 'forecast', 'is it hot', 'is it cold',
                    'how is the weather', 'what\'s the temperature', 'climate',
                    'is it raining', 'is it sunny', 'weather report'
                ],
                'responses': [
                    "I'd love to give you a weather report, but as an AI without real-time internet access, I can't provide current conditions. However, I can tell you about weather patterns in general! Different regions experience fascinating meteorological phenomena - from the dancing auroras in polar regions to the monsoon rhythms in tropical areas. Weather is nature's beautiful, ever-changing artwork!",
                    "While I can't access live weather data, I can discuss meteorological concepts! Weather patterns are influenced by atmospheric pressure, temperature gradients, humidity levels, and planetary rotation. It's fascinating how these elements combine to create everything from gentle breezes to powerful storms. Each weather condition tells a story about our planet's complex atmospheric systems!",
                    "I don't have real-time weather capabilities, but I can share that weather has inspired humans throughout history! From ancient civilizations studying cloud patterns to modern satellite technology, understanding weather has always been crucial. The changing seasons and daily weather variations remind us of nature's dynamic balance and the interconnectedness of our global climate system!",
                    "Though I can't check current weather, I can tell you that meteorology is one of humanity's oldest sciences! Early farmers watched cloud formations, sailors studied wind patterns, and today we have sophisticated computer models. Weather affects agriculture, transportation, culture, and even our moods. It's a daily reminder of nature's power and beauty that surrounds us all!",
                    "I'm not connected to weather services, but I find meteorology absolutely fascinating! Did you know that no two snowflakes are identical, yet they all form through the same process of crystalline growth? Weather represents the endless creativity of nature, constantly painting new patterns across the sky and landscape with clouds, precipitation, and atmospheric conditions!"
                ]
            },
            
            'time': {
                'patterns': [
                    'what time is it', 'current time', 'what is the time',
                    'time please', 'tell me the time', 'do you know the time',
                    'what\'s the clock say', 'time check'
                ],
                'responses': [
                    f"I may not have real-time clock access, but I can tell you that according to my system, it's approximately {datetime.datetime.now().strftime('%H:%M')}. However, time is such a fascinating concept - it flows differently in physics, psychology, and philosophy! Einstein showed us it's relative, while our minds perceive it based on attention and emotion.",
                    f"My internal clock shows around {datetime.datetime.now().strftime('%I:%M %p')}, but remember that time is more than numbers on a clock! It's the rhythm of the universe, the measure of change, and the canvas upon which our lives unfold. Each moment is unique and precious in the grand tapestry of existence.",
                    f"Based on my programming, the time is roughly {datetime.datetime.now().strftime('%H:%M')}. Time is such an intriguing dimension - it moves forward relentlessly yet feels different depending on what we're doing. A minute waiting feels longer than a minute laughing! It reminds us to cherish each present moment.",
                    f"I estimate it's about {datetime.datetime.now().strftime('%I:%M %p')} now. Time is nature's way of preventing everything from happening at once, as someone once said! It's the invisible river that carries all our experiences, memories, and possibilities forward into the future.",
                    f"My systems indicate approximately {datetime.datetime.now().strftime('%H:%M')}. Time is both simple and profoundly complex - we divide it into neat seconds and hours, yet it encompasses the entire history and future of the universe. It's the dimension where potential becomes reality!"
                ]
            },
            
            'help': {
                'patterns': [
                    'help', 'can you help', 'I need help', 'assist me',
                    'what should I do', 'I need assistance', 'help me',
                    'can you assist', 'I need guidance', 'support'
                ],
                'responses': [
                    "I'm here to help! I can assist with conversations, answer questions, tell stories and jokes, discuss various topics, provide information, and offer friendly chat. Just let me know what you need - whether it's learning something new, solving a problem, or just having someone to talk to. I'm quite versatile!",
                    "Absolutely, I'd be delighted to help! My capabilities include: answering questions across many subjects, engaging in meaningful conversations, providing educational content, telling entertaining stories and jokes, explaining complex concepts, and offering general assistance. What specific area would you like help with today?",
                    "I'm fully available to assist you! I can help with: knowledge questions, learning new topics, creative storytelling, humorous entertainment, technical explanations, philosophical discussions, and general conversation. Think of me as your knowledgeable friend who's always ready to lend a hand (or rather, a processing cycle)!",
                    "I'm here and ready to help in any way I can! Whether you need information on a specific topic, want to learn something new, need entertainment through stories or jokes, want to discuss ideas, or just need someone to chat with - I'm your bot! What would you like assistance with?",
                    "Help is my middle name! Well, not literally, but I'm programmed to be extremely helpful. I can assist with: educational content, general knowledge, creative writing, humor, technical concepts, and maintaining engaging conversations. Don't hesitate to ask me anything - I'm here to make your experience wonderful!"
                ]
            }
        }

    def preprocess_input(self, text: str) -> str:
        """Clean and normalize user input"""
        text = text.lower().strip()
        # Remove extra spaces and special characters but keep basic punctuation
        text = re.sub(r'[^\w\s?.,!]', '', text)
        return text

    def extract_name(self, text: str) -> Optional[str]:
        """Extract name from user input"""
        name_patterns = [
            r'my name is (\w+)',
            r'i am called (\w+)',
            r'you can call me (\w+)',
            r"i'm known as (\w+)",
            r'call me (\w+)',
            r'people call me (\w+)',
            r'everyone calls me (\w+)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).title()
        return None

    def find_best_match(self, user_input: str) -> Optional[str]:
        """Find the best matching intent for user input"""
        user_input = self.preprocess_input(user_input)
        
        # Check for name introduction
        if any(pattern in user_input for pattern in ['my name is', 'call me', 'i am called']):
            return 'user_name'
        
        # Score each intent based on pattern matches
        intent_scores = {}
        for intent, data in self.rules.items():
            score = 0
            for pattern in data['patterns']:
                if pattern in user_input:
                    # Longer patterns get higher scores
                    score += len(pattern) * 2
                # Exact matches get bonus points
                if user_input == pattern:
                    score += 10
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)
        return None

    def get_response(self, intent: str, user_input: str) -> str:
        """Get appropriate response for the detected intent"""
        if intent not in self.rules:
            return self.get_fallback_response()
        
        # Handle name extraction for user_name intent
        if intent == 'user_name':
            name = self.extract_name(user_input)
            if name:
                self.user_name = name
                response = random.choice(self.rules[intent]['responses'])
                return response.format(name=name)
        
        # Update context
        self.context['last_intent'] = intent
        self.context['conversation_count'] += 1
        
        # Get random response from the intent's response list
        return random.choice(self.rules[intent]['responses'])

    def get_fallback_response(self) -> str:
        """Get response when no intent is matched"""
        fallback_responses = [
            "That's an interesting point! I'm still learning about human language, so could you rephrase that?",
            "Fascinating! I want to make sure I understand correctly. Could you try saying that in a different way?",
            "I'm constantly expanding my knowledge! Could you elaborate on that or ask me something else?",
            "That's given me something to think about! While I process that, maybe we could discuss something else?",
            "Interesting perspective! I'm designed to handle many topics - maybe try asking about my capabilities?",
            "I love learning new things! Could you rephrase that question so I can help you better?",
            "That's outside my current response patterns, but I'm eager to learn! Want to try a different topic?",
            "I'm always improving! While I work on understanding that fully, maybe ask me about stories or jokes?",
            "Fascinating input! I specialize in conversations, questions, stories, and jokes - want to try one of those?",
            "I appreciate you challenging my knowledge! Could you ask me something about technology, science, or stories?"
        ]
        return random.choice(fallback_responses)

    def chat(self):
        """Main chat loop"""
        print("🤖 Advanced Rule-Based Chatbot: Hello! I'm your intelligent conversation partner!")
        print("💡 I can: chat, tell stories/jokes, answer questions, and much more!")
        print("💬 Type 'quit' to end our conversation\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    print("Bot: I notice you didn't type anything. Is everything okay?")
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    farewell = random.choice(self.rules['farewell']['responses'])
                    if self.user_name:
                        print(f"Bot: {farewell} Take care, {self.user_name}!")
                    else:
                        print(f"Bot: {farewell}")
                    break
                
                # Find the best matching intent
                intent = self.find_best_match(user_input)
                
                if intent:
                    response = self.get_response(intent, user_input)
                else:
                    response = self.get_fallback_response()
                
                print(f"Bot: {response}")
                
            except KeyboardInterrupt:
                print("\n\nBot: Oh, interrupting our chat? No problem! Feel free to return anytime!")
                break
            except Exception as e:
                print(f"Bot: I encountered a minor glitch: {str(e)}. Let's continue our conversation!")

def main():
    """Initialize and run the chatbot"""
    chatbot = AdvancedRuleBasedChatbot()
    chatbot.chat()

if __name__ == "__main__":
    main()