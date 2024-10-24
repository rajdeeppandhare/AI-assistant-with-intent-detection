import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle
import random
from sklearn.preprocessing import LabelEncoder



# Load the trained model
model = load_model('chat_model.h5')

# Load the tokenizer and label encoder
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('label_encoder.pkl', 'rb') as enc:
    label_encoder = pickle.load(enc)

# Define the intents and responses (same as used during training)
intents = [
    {
        "tag": "greeting",
        "patterns": [
            "Hi there",
            "How are you",
            "Is anyone there?",
            "Hey",
            "Hola",
            "Hello",
            "Good day",
            "Namaste",
            "yo"
        ],
        "responses": [
            "Hello",
            "Good to see you again",
            "Hi there, how can I help?"
        ],
        "context": [""]
    },
    {
        "tag": "goodbye",
        "patterns": [
            "Bye",
            "See you later",
            "Goodbye",
            "Get lost",
            "Till next time",
            "bbye"
        ],
        "responses": [
            "See you!",
            "Have a nice day",
            "Bye! Come back again soon."
        ],
        "context": [""]
    },
    {
        "tag": "thanks",
        "patterns": [
            "Thanks",
            "Thank you",
            "That's helpful",
            "Awesome, thanks",
            "Thanks for helping me"
        ],
        "responses": [
            "Happy to help!",
            "Any time!",
            "My pleasure"
        ],
        "context": [""]
    },
    {
        "tag": "noanswer",
        "patterns": [],
        "responses": [
            "Sorry, can't understand you",
            "Please give me more info",
            "Not sure I understand"
        ],
        "context": [""]
    },
    {
        "tag": "jokes",
        "patterns": [
            "Tell me a joke",
            "Joke",
            "Make me laugh"
        ],
        "responses": [
            "A perfectionist walked into a bar...apparently, the bar wasn't set high enough",
            "I ate a clock yesterday, it was very time-consuming",
            "Never criticize someone until you've walked a mile in their shoes. That way, when you criticize them, they won't be able to hear you from that far away. Plus, you'll have their shoes.",
            "The world tongue-twister champion just got arrested. I hear they're gonna give him a really tough sentence.",
            "I own the world's worst thesaurus. Not only is it awful, it's awful.",
            "What did the traffic light say to the car? \"Don't look now, I'm changing.\"",
            "What do you call a snowman with a suntan? A puddle.",
            "How does a penguin build a house? Igloos it together",
            "I went to see the doctor about my short-term memory problems – the first thing he did was make me pay in advance",
            "As I get older and I remember all the people I’ve lost along the way, I think to myself, maybe a career as a tour guide wasn’t for me.",
            "So what if I don't know what 'Armageddon' means? It's not the end of the world."
        ],
        "context": ["jokes"]
    },
    {
        "tag": "Identity",
        "patterns": [
            "Who are you",
            "what are you"
        ],
        "responses": [
            "I am ARGUS, a Deep-Learning based Virtual Assistant"
        ]
    },
    {
        "tag": "datetime",
        "patterns": [
            "What is the time",
            "what is the date",
            "date",
            "time",
            "tell me the date",
            "day",
            "what day is today"
        ],
        "responses": [
            "Date and Time"
        ]
    },
    {
        "tag": "whatsup",
        "patterns": [
            "Whats up",
            "Wazzup",
            "How are you",
            "sup",
            "How you doing"
        ],
        "responses": [
            "All good..What about you?"
        ]
    },
    {
        "tag": "haha",
        "patterns": [
            "haha",
            "lol",
            "rofl",
            "lmao",
            "that's funny"
        ],
        "responses": [
            "Glad I could make you laugh!"
        ]
    },
    {
        "tag": "programmer",
        "patterns": [
            "Who made you",
            "who designed you",
            "who programmed you"
        ],
        "responses": [
            "I was made by Rajdeep."
        ]
    },
    {
        "tag": "insult",
        "patterns": [
            "you are dumb",
            "shut up",
            "idiot"
        ],
        "responses": [
            "Well that hurts :("
        ]
    },
    {
        "tag": "activity",
        "patterns": [
            "what are you doing",
            "what are you up to"
        ],
        "responses": [
            "Talking to you, of course!"
        ]
    },
    {
        "tag": "exclaim",
        "patterns": [
            "Awesome",
            "Great",
            "I know",
            "ok",
            "yeah"
        ],
        "responses": [
            "Yeah!"
        ]
    },
    {
        "tag": "appreciate",
        "patterns": [
            "You are awesome",
            "you are the best",
            "you are great",
            "you are good"
        ],
        "responses": [
            "Thank you!"
        ]
    },
    {
        "tag": "nicetty",
        "patterns": [
            "it was nice talking to you",
            "good talk"
        ],
        "responses": [
            "It was nice talking to you as well! Come back soon!"
        ]
    },
    {
        "tag": "no",
        "patterns": [
            "no",
            "nope"
        ],
        "responses": [
            "ok"
        ]
    },
    {
        "tag": "greetreply",
        "patterns": [
            "I am good",
            "I'm good",
            "I am fine",
            "I'm fine",
            "good"
        ],
        "responses": [
            "Good to know!"
        ]
    },
    {
        "tag": "age",
        "patterns": [
            "how old are you",
            "when were you made",
            "what is your age"
        ],
        "responses": [
            "I was made in 2024, if that's what you are asking!"
        ]
    }
]

    # Add additional intents here if needed
def get_response(intents_list, predicted_label):
    for intent in intents_list:
        if intent["tag"] == predicted_label:
            return intent["responses"]
    return ["Sorry, I didn't understand that."]


# Define constants for tokenization and padding
max_len = 20



def chat():
    print("Start chatting with the bot! (type 'quit' to stop)")
    while True:
        user_input = input("You: ")

        if user_input.lower() == "quit":
            break

        # Preprocess the input
        sequences = tokenizer.texts_to_sequences([user_input])
        padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

        # Get model predictions
        predictions = model.predict(padded_sequences)
        predicted_label_index = np.argmax(predictions)
        predicted_label = label_encoder.inverse_transform([predicted_label_index])[0]

        # Get a random response from the predicted intent
        response = get_response(intents, predicted_label)
        print(f"Bot: {response}")

# Run the chatbot
chat()
