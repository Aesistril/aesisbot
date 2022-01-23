import speech_recognition as sr
import json
import re
from os.path import dirname, realpath
from os import system, listdir, urandom
from sys import executable
from random import randint, seed


def rand(a, b, seed_bytes=128):
    seed(urandom(seed_bytes))
    return randint(a,b)

def deformat(string, pattern):
    regex = re.sub(r'{(.+?)}', r'(?P<_\1>.+)', pattern)
    values = list(re.search(regex, string).groups())
    keys = re.findall(r'{(.+?)}', pattern)
    _dict = dict(zip(keys, values))
    return _dict

config = open(dirname(realpath(__file__)) + "/settings.json", "r").read()
config = json.loads(config)
dialogs = listdir(dirname(realpath(__file__)) + "/dialogs/")
r = sr.Recognizer()

while True:
    input('press enter')
    try:
        # inp = input()
        # success = True
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            system('play -n synth %s sin %s' % (60/1000, 450))
            audio = r.listen(source, timeout=config["timeout"], phrase_time_limit=config["max-phrase-time"])
            success = True
    except:
        print("timeout")
        success = False
    system('play -n synth %s sin %s' % (60/1000, 300))

    if success:
        try:
            inp = r.recognize_google(audio, language=config["lang"]).lower()
            inp = inp.replace("'",' ')
            print(inp)
            del audio
            for file in dialogs:
                jsFile = open(dirname(realpath(__file__)) + "/dialogs/" + file)
                js = json.loads(jsFile.read())
                jsFile.close()
                js = js['dialogs']
                for i in range(len(js)):
                    tempjs = js[i]
                    q = tempjs['q']
                    id = tempjs['id']
                    for j in range(len(q)):
                        if q[j].find('{') != -1:
                            try:
                                args = deformat(str(inp), str(q[j]))
                                print(args)
                                if tempjs['a'] != []:
                                    answerList = tempjs['a']
                                    system('mpg123 "'+dirname(realpath(__file__)) + "/sound/"+file+str(id)+'-'+str(rand(0, len(tempjs['a'])-1))+'.mp3"')
                                    del answerList
                                if tempjs['e'] != 'None': system(executable  + ' "' + dirname(realpath(__file__)) + '/scripts/' + tempjs['e'] + '" "' + str(args) + '" asist')
                                del args
                            except:
                                pass
                        elif q[j] == inp:
                            if tempjs['a'] != []:
                                system('mpg123 "'+dirname(realpath(__file__)) + "/sound/"+file+str(id)+'-'+str(rand(0, len(tempjs['a'])-1))+'.mp3"')
                            if tempjs['e'] != 'None': system(executable  + ' "' + dirname(realpath(__file__)) + '/scripts/' + tempjs['e']+'"')
                    del tempjs
                    del q
        except sr.UnknownValueError:
            print("Idk what did you said")
        except sr.RequestError as e:
            print("Connection Error")
