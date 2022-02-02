#!/usr/bin/python3

# Copyright (C) 2022 Yiğit Ayaz

# This file is part of Aesisbot.

# Aesisbot is free software: you can redistribute it and/or modify it under the terms 
# of the GNU General Public License as published by the Free Software Foundation, 
# either version 3 of the License, or (at your option) any later version.

# Aesisbot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with Aesisbot. 
# If not, see <https://www.gnu.org/licenses/>. 

###################### IMPORTING/INITILIZATION ######################
from os.path import dirname
from tensorflow.compat.v1 import reset_default_graph
from nltk.stem.lancaster import LancasterStemmer
from random import choice
class os: from os import system, listdir
class pickle: from pickle import load
class tflearn: from tflearn import fully_connected, regression, DNN, input_data
class subprocess: from subprocess import call
class cl: from colorama import Fore, Style, Back, init
class nltk: from nltk import word_tokenize
class numpy: from numpy import array, argmax
class json: from json import loads

print("\n")
print("""The programs included with the Aesisbot are free software;
the exact distribution terms for each program are described in the
individual files in <aesisbot source code>/src/licenses/ or 
/usr/share/aesisbot/licenses/ directory.

Aesisbot comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
""")

cl.init(autoreset=True)

# Load the pickle file if it exists; if not, retrain the AI
try:
    print(cl.Fore.GREEN+"Looking for the variable data")
    with open("{0}/model/parse.pickle".format(dirname(__file__)), "rb") as f:
        words, labels, training, output = pickle.load(f)
        print(cl.Fore.GREEN+"Successfully loaded the variable data")
except:
    print("*"*50 + "\n"+cl.Fore.YELLOW+"Can't find the variable data, AI might be affected\nfrom this as well, retraining the AI\n"+cl.Fore.RESET+"*"*50 + "\n")
    os.system("{0}/train.py".format(dirname(__file__)))
    print("*"*50 + "\n"+cl.Fore.GREEN+"Training completed! Loading the data...\n"+cl.Fore.RESET+"*"*50)
    with open("{0}/model/parse.pickle".format(dirname(__file__)), "rb") as f:
        words, labels, training, output = pickle.load(f)
        print(cl.Fore.GREEN+"Successfully loaded the variable data")

reset_default_graph()

# Construct the neural network for AI
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8) # 8 neurons for hidden layer
net = tflearn.fully_connected(net, 8) # 2nd hidden layer
net = tflearn.fully_connected(net, len(output[0]), activation="softmax") # Output layer, softmax option for giving probability
model = tflearn.DNN(net)

# Load the AI model if it exists; if not, retrain the model
try:
    print(cl.Fore.GREEN+"Looking for the AI training data")
    model.load("{0}/model/model.tflearn".format(dirname(__file__)))
    print(cl.Fore.GREEN+"Successfully loaded the training data")
except:
    print("*"*50 + "\n"+cl.Fore.YELLOW+"Can't find the AI training data, retraining the AI\n"+cl.Fore.RESET+"*"*50 + "\n")
    subprocess.call("{0}/train.py".format(dirname(__file__)))
    print("*"*50 + "\n"+cl.Fore.GREEN+"Training completed! Loading the data..."+cl.Fore.RESET+"*"*50 + "\n")
    model.load("{0}/model/model.tflearn".format(dirname(__file__)))
    with open("{0}/model/parse.pickle".format(dirname(__file__)), "rb") as f:
        words, labels, training, output = pickle.load(f)
    print(cl.Fore.GREEN+"Successfully loaded the training data")

# Import intents.json from each directory and join them together
intents = {'intents': []}
for directory in os.listdir("{0}/modules/".format(dirname(__file__))): 
    try: # Check if directory is empty of json file is invalid (fuck you)
        intents_file = json.loads(open("{0}/modules/{1}/intents.json".format(dirname(__file__), directory)).read()) # load intents
        for i in intents_file["intents"]: # join intents together
            intents["intents"].append(i)
    except Exception as err: # for debugging
        pass
###################### IMPORTING/INITILIZATION END ######################

stemmer = LancasterStemmer()
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)


def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        for tg in intents["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        print(choice(responses))

chat()