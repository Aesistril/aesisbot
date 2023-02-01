#!/usr/bin/env python3

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

# TODO: Remove kind words like "please" (I think stemmer does this but I'm not sure)

###################### ENVIRONMENT CHECKING ######################
from os.path import dirname, isfile
class platform: from platform import system

# Check if running from source
chksrc = open("{0}/chksrc".format(dirname(__file__)))
if chksrc.read() == "nv3OBJk6ZZkdTJkqqOEQ654y58uJYpF5WhSYTWOMqMLIQBq5AxmWmU7uwMajEin3SaCgdT0xmer9BUM02aiznJlJt0H8HFNH5sdE":
    srcrun = True
else: srcrun = False

# This is just nonsense. Did I really think like: "Yeah refusing to run that will definitely improve the UX"
# Get the OS name
# useros = platform.system()
# if useros != 'Linux' and useros != 'Windows':
#     print("Sorry, we only support Linux. There is plans on supporting BSD. macOS will probably not get supported but you can open a pull request if you can get it working on macOS")
#     exit(-1)

###################### ENVIRONMENT CHECKING END ######################

###################### USER INPUT ######################
import argparse
# Get the command line arguments
parser = argparse.ArgumentParser(description="Parse the intent files and train the AI model for Aesisbot")
# parser.add_argument('inputfile', metavar="<intents file>", type=str, help="Location of intents file with the dialogs in it. (must be json)")
parser.add_argument('-m', '--monochrome', action="store_true", help="Don't use colored output")
parser.add_argument('-p', '--no-parse', help='Use old .pickle files instead of parsing intents again')
parser.add_argument('-o', '--output', type=str, metavar="<output directory>", help='Output directory to save trained models and parsed intents (default: if installed /usr/share/aesisbot/model/<model name>, if running from source src/model/<model name>')
args = parser.parse_args()
###################### USER INPUT END ######################

###################### IMPORTING/INITILIZATION ######################
from nltk.stem.lancaster import LancasterStemmer
from tensorflow.compat.v1 import reset_default_graph
from configparser import ConfigParser
from time import sleep
class pickle: from pickle import dump
class numpy: from numpy import array
class tflearn: from tflearn import fully_connected, regression, DNN, input_data
class cl: from colorama import Fore, Style, Back, init
class nltk: from nltk import word_tokenize, download, data
class json: from json import loads
class os: from os import listdir

print("\n"*2) # Leave some space after tensorflow warning
cl.init(autoreset=True) # Initiliaze colored terminal output

# Load the config file
config = ConfigParser()
config.read("{0}/config.ini".format(dirname(__file__)))

# Update nltk resources
print("*"*50 + "\n" + cl.Fore.YELLOW+'Updating NLTK resources'+cl.Fore.RESET + "\n" + "*"*50)
print(cl.Fore.GREEN + "Installing tokenizers/punkt.zip")
nltk.download('punkt')
print("*"*50 + "\n" + cl.Fore.GREEN+'All resources are up to date'+cl.Fore.RESET + "\n" + "*"*50)

stemmer = LancasterStemmer()
###################### IMPORTING/INITILIZATION END ######################

###################### PARSING ######################
words = []
labels = []
docs_x = []
docs_y = [] # Where coresponding tags for patterns stored

def tokenize():
    global intents, docs_x, docs_y, words, labels# Use all global variables
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern, language=config["LANG"]["lang-long"])
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

# Import intents.json from each directory and parse them
for directory in os.listdir("{0}/modules/".format(dirname(__file__))): 
    try: # Check if directory is empty of json file is invalid (fuck you)
        intents = json.loads(open("{0}/modules/{1}/intents.json".format(dirname(__file__), directory)).read()) # load intents
        tokenize()
    except Exception as err: # for debugging
        pass

words = [stemmer.stem(w.lower()) for w in words if w != "?"] # Remove all connectives, adjuncts, formatives etc.
words = sorted(list(set(words))) # Delete duplicate words

labels = sorted(labels)

training = []
output = []
out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []
    wrds = [stemmer.stem(w.lower()) for w in doc]
    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)
    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1
    training.append(bag)
    output.append(output_row)

# convert lists to numpy array for Tensorflow
training = numpy.array(training)
output = numpy.array(output)
# save parsed/tokenized intents
with open("{0}/model/parse.pickle".format(dirname(__file__)), "wb") as f:
        pickle.dump((words, labels, training, output), f)
###################### PARSING END ######################

###################### AI TRAINING ######################
reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8) # 8 neurons for hidden layer
net = tflearn.fully_connected(net, 8) # 2nd hidden layer
net = tflearn.fully_connected(net, len(output[0]), activation="softmax") # Output layer, softmax option for giving probability
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=int(config["AI"]["epoch"]), batch_size=8, show_metric=True) # Train the ai
model.save("{0}/model/model.tflearn".format(dirname(__file__))) # save the model
###################### AI TRAINING END ######################
