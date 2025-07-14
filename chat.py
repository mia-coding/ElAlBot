import random
# NLP/Neural Network Libraries
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
nltk.download('punkt_tab')
nltk.download('wordnet')
import json
import numpy as np
import os
import sys

class chat:
        def __init__(self):
                self.run = False
                self.greetings = "Hi, welcome! What question do you have?"
                self.confused = "Sorry, I'm not sure how to answer that, maybe try to be more specific? Email elalbbgnsiah@gmail.com if you have any questions and for more information!"

                self.lemmatizer = WordNetLemmatizer()

        # Load intents only once
                intents_file_path = os.path.join(os.path.dirname(__file__), 'intents.json')
                with open(intents_file_path, 'r', encoding='utf-8') as f:
                        self.intents = json.load(f)

                self.model = None
                self.words = []
                self.classes = []

                self.load_ai_model()
                print("Chatbot initialized.") # Indicate that setup is done

        def load_ai_model(self):
                # Paths to model and associated data files
                model_path = os.path.join(os.path.dirname(__file__), 'chatbot_model.tflite') # Expect TFLite model
                words_path = os.path.join(os.path.dirname(__file__), 'words.json')
                classes_path = os.path.join(os.path.dirname(__file__), 'classes.json')

                try:
                        if not os.path.exists(model_path):
                                raise FileNotFoundError(f"Model file not found: {model_path}")
                        if not os.path.exists(words_path):
                                raise FileNotFoundError(f"Words file not found: {words_path}")
                        if not os.path.exists(classes_path):
                                raise FileNotFoundError(f"Classes file not found: {classes_path}")

                # Load TFLite model
                        self.model = tf.lite.Interpreter(model_path=model_path)
                        self.model.allocate_tensors()
                        self.input_details = self.model.get_input_details()
                        self.output_details = self.model.get_output_details()

                        if not self.input_details or not self.output_details:
                                raise ValueError("TFLite model input/output details could not be retrieved.")

                        # Load words and classes
                        with open(words_path, 'r', encoding='utf-8') as f:
                                self.words = json.load(f)
                        with open(classes_path, 'r', encoding='utf-8') as f:
                                self.classes = json.load(f)

                        print("AI Model and associated data loaded successfully!")

                except FileNotFoundError as e:
                        print(f"Error: Required model or data file not found: {e}. Please ensure 'chatbot_model.tflite', 'words.json', and 'classes.json' are in the same directory as chatbot.py.")
                        self.model = None # Ensure model is None if any file is missing
                        self.words = []
                        self.classes = []
                        # Model failed to load.
                        sys.exit(1)

                except Exception as e:
                        print(f"Error loading AI model or data: {e}")
                        self.model = None
                        self.words = []
                        self.classes = []
                        sys.exit(1) # Exit if loading fails

        def clean_up_sentence(self, sentence):
                sentence_words = nltk.word_tokenize(sentence)
                sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
                return sentence_words

        # Optimized bag_of_words: using `np.isin` for potentially faster matching
        def bag_of_words(self, sentence, words):
                sentence_words = self.clean_up_sentence(sentence)
                # Create a boolean array indicating presence, then convert to int
                bag = np.isin(np.array(words), sentence_words).astype(int)
                return bag

        def predict_class(self, sentence):
                if not self.model:
                        print("Warning: Model not loaded, returning fallback.")
                        return [{'intent': 'fallback', 'probability': 1.0}]

                p = self.bag_of_words(sentence, self.words)
                input_data = np.array([p], dtype=self.input_details[0]['dtype']) # Ensure dtype matches model
                self.model.set_tensor(self.input_details[0]['index'], input_data)
                self.model.invoke()
                res = self.model.get_tensor(self.output_details[0]['index'])[0]

                ERROR_THRESHOLD = 0.4
                results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
                if len(results) == 0:
                        return []

                results.sort(key=lambda x: x[1], reverse=True)
                return_list = []
                for r in results:
                        return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
                        return return_list

        def get_response(self, intents_list):
                if len(intents_list) == 0:
                        return self.confused

                tag = intents_list[0]['intent']
                list_of_intents = self.intents['intents']
                for intent_data in list_of_intents:
                        if intent_data['tag'] == tag:
                                # Randomly select a response
                                result = np.random.choice(intent_data['responses'])
                                break
                else:  # If no intent matches or fallback
                        result = self.confused
                return result

        def return_bot_response(self, user_input):
                # get the user response and predict the intent
                intents_prediction = self.predict_class(user_input)
                # according to the predict intent generate the response
                bot_response_text = self.get_response(intents_prediction)
                return bot_response_text

# Create a single global instance of the chatbot to ensure model is loaded only once
chatbot_instance = None

def get_chatbot_instance():
        global chatbot_instance
        if chatbot_instance is None:
                print("Initializing chatbot_instance...")
                chatbot_instance = chat()
        return chatbot_instance

if __name__ == '__main__':

        cb = get_chatbot_instance()

        print(cb.greetings)
        print("Type 'exit' or 'bye' to quit.")
        while True:
                user_response = input("You: ").lower()
                if user_response in ["exit", "bye"]:
                        print("Bot: Goodbye!")
                        break
                print(f"Bot: {cb.return_bot_response(user_response)}")