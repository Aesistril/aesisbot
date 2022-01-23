from sys import argv
from gtts import gTTS

def asistArgs():
    if argv[len(argv)-1] == 'asist':
        asistArgs = argv[len(argv)-2]
    else: asistArgs = {}
    return eval(asistArgs)

def talk(string):
    import json
    from os.path import dirname, abspath, join
    from os import system, remove
    config = open(abspath(join(dirname( __file__ ), '..', 'settings.json'))).read()
    config = json.loads(config)
    tts = gTTS(string, lang=config['lang'])
    tts.save('temp.mp3')
    system('mpg123 temp.mp3')
    remove('temp.mp3')