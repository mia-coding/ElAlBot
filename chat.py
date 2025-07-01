import random
# NLP/Neural Network Libraries
import nltk
from nltk.stem import WordNetLemmatizer
#nltk.download('punkt_tab')
#nltk.download('wordnet')
import datetime
import uuid
import json
import numpy as np

from tensorflow.keras.models import load_model

class chat:
        def __init__(self):
                self.run = False
                self.greetings = "Hi, welcome! What question do you have?"
                self.confused = "Sorry, I'm not sure how to answer that, maybe try to be more specific? Email elalbbgnsiah@gmail.com if you have any questions and for more information!"

                self.lemmatizer = WordNetLemmatizer()
                intents_file = open('intents.json').read()
                self.intents = json.loads(intents_file)
                try:
                        self.model = load_model('chatbot_model.keras')  # load the trained model
                        with open('words.json', 'r') as f:
                                self.words = json.load(f) #load words
                        with open('classes.json', 'r') as f:
                                self.classes = json.load(f) #load classes
                        print("AI Model and associated data loaded successfully!")
                except Exception as e:
                        print(f"Error loading AI model: {e}")
                        self.model = None  # Set to None if loading fails
                        self.words = []
                        self.classes = []

        def clean_up_sentence(self, sentence):
                sentence_words = nltk.word_tokenize(sentence)
                sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
                return sentence_words

        # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
        def bag_of_words(self, sentence, words, show_details=True):
                sentence_words = self.clean_up_sentence(sentence)
                bag = [0] * len(words)
                for s in sentence_words:
                        for i, w in enumerate(words):
                                if w == s:
                                        bag[i] = 1
                                        if show_details:
                                                print(f"found in bag: {w}")
                return np.array(bag)

        def predict_class(self, sentence, model, words, classes):
                if not model or not words or not classes:
                        return [{'intent': 'fallback', 'probability': 1.0}]  # Fallback if model not loaded

                p = self.bag_of_words(sentence, words, show_details=False)
                res = model.predict(np.array([p]))[0]
                ERROR_THRESHOLD = 0.3  # Adjust as needed
                results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
                if len(results) == 0: return []
                results.sort(key=lambda x: x[1], reverse=True)
                return_list = []
                for r in results:
                        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
                return return_list

        def get_response(self, intents_list, intents_json):
                if len(intents_list) == 0: return self.confused
                tag = intents_list[0]['intent']
                list_of_intents = intents_json['intents']
                for i in list_of_intents:
                        if i['tag'] == tag:
                                # Randomly select a response from the matched intent
                                result = np.random.choice(i['responses'])
                                break
                else:  # If no intent matches or fallback
                        result = self.confused
                return result

        def start(self):
                self.run = True
                print(self.greetings)
                while(self.run):
                        user_response = input().lower()
                        if(user_response=="exit" or user_response=="bye"):
                                self.run = False
                                break
                        print(self.return_bot_response(user_response))

        def return_bot_response(self, user_response):
                # get the user response and predict the intent
                intents_prediction = self.predict_class(user_response, self.model, self.words, self.classes)
                # according to the predict intent generate the response
                bot_response_text = self.get_response(intents_prediction, self.intents)
                return bot_response_text

if __name__ == '__main__':
        c = chat()
        c.start()