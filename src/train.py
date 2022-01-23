# TODO: lütfen gibi nezaket kelimelerini atsın

###################### IMPORTING/INITILIZATION ######################
from os.path import dirname, isfile
from nltk.stem.lancaster import LancasterStemmer
from tensorflow.compat.v1 import reset_default_graph
from configparser import ConfigParser
from time import sleep
class numpy: from numpy import array
class tflearn: from tflearn import fully_connected, regression, DNN, input_data
class cl: from colorama import Fore, Style, Back, init
class nltk: from nltk import word_tokenize, download, data
class json: from json import loads

print("\n")
cl.init(autoreset=True) # Initiliaze colored terminal output

# Load the config file and intents
intents = json.loads(open("{0}/intents/testintents.json".format(dirname(__file__))).read())
config = ConfigParser()
config.read("{0}/config.ini".format(dirname(__file__)))

# Update nltk resources
print("*"*50 + "\n" + cl.Fore.YELLOW+'Updating NLTK resources'+cl.Fore.RESET + "\n" + "*"*50)
print(cl.Fore.GREEN + "Installing tokenizers/punkt.zip")
nltk.download('punkt')
print("*"*50 + "\n" + cl.Fore.GREEN+'All resources are up to date'+cl.Fore.RESET + "\n" + "*"*50)
sleep(1)

stemmer = LancasterStemmer()
###################### IMPORTING/INITILIZATION END ######################

###################### PARSING ######################
words = []
labels = []
docs_x = []
docs_y = [] # Where coresponding tags for patterns stored

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])
    if intent["tag"] not in labels:
        labels.append(intent["tag"])

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