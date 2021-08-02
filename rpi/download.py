from os import listdir
from os.path import dirname, realpath
from gtts import gTTS
import json

config = open(dirname(realpath(__file__)) + "/settings.json", "r").read()
config = json.loads(config)
dialogs = listdir(dirname(realpath(__file__)) + "/dialogs/")

for file in dialogs:
    jsFile = open(dirname(realpath(__file__)) + "/dialogs/" + file)
    js = json.loads(jsFile.read())
    jsFile.close()
    js = js['dialogs']
    for i in range(len(js)):
        tempjs = js[i]
        answers = tempjs['a']
        id = tempjs['id']
        for a in range(len(answers)):
            tts = gTTS(answers[a], lang=config['lang'])
            print(file+str(id)+'-'+str(a)+'.mp3 indiriliyor')
            tts.save(dirname(realpath(__file__)) + "/sound/"+file+str(id)+'-'+str(a)+'.mp3')