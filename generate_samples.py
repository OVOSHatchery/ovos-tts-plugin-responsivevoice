from responsive_voice import get_voices
from os.path import join, dirname


def lang2voice():
    voice_clazzes = get_voices()
    voices = {}
    for voice in voice_clazzes:
        lang = voice_clazzes[voice]().lang.split("_#")[0].lower().replace(
            "_", "-").replace("service", "sv")
        lang2 = lang.split("-")[0]
        if lang not in voices:
            voices[lang] = []
        if lang2 not in voices:
            voices[lang2] = []
        if voice not in voices[lang]:
            voices[lang].append(voice)
        if voice not in voices[lang2]:
            voices[lang2].append(voice)
        # special cases
        if lang == "ca-es":
            lang = "es-ca"
            lang2 = lang.split("-")[0]
            if lang not in voices:
                voices[lang] = []
            if lang2 not in voices:
                voices[lang2] = []
            if voice not in voices[lang]:
                voices[lang].append(voice)
            if voice not in voices[lang2]:
                voices[lang2].append(voice)
    return voices


voices = get_voices()

sentence = "Hello world, this is a demo of text to speech"
en_voices = lang2voice()["en"]
for voice_name in en_voices:
    engine = voices[voice_name]()
    mp3_file = join(dirname(__file__), "samples", voice_name + ".mp3")
    #engine.get_mp3(sentence, mp3_file)

sentence = "Olá mundo, esta é uma demonstração de conversão de texto em voz"
pt_voices = lang2voice()["pt-pt"]
for voice_name in pt_voices:
    engine = voices[voice_name]()
    mp3_file = join(dirname(__file__), "samples", voice_name + ".mp3")
    #engine.get_mp3(sentence, mp3_file)

sentence = "Hola mundo, esta es una demostración de texto a voz"
es_voices = lang2voice()["es-es"]
for voice_name in es_voices:
    engine = voices[voice_name]()
    mp3_file = join(dirname(__file__), "samples", voice_name + ".mp3")
    #engine.get_mp3(sentence, mp3_file)

