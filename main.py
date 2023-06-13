import random
import os
import re

from gtts import gTTS
import playsound
import speech_recognition as sr


films = ['терминатор', 'терминатор 2', 'рембо', 'пятый элемент']
hellows = ['hola', 'привет', 'здравствуйте', 'hi']


def listen():  # слушаем команду
    print('Скажите команду')
    rec = sr.Recognizer()  # включение модуля расшифровщика
    with sr.Microphone() as source:  # называем микрофон source
        voice = rec.listen(source, phrase_time_limit=6)  # запись того что с микрофона в течении 3 сек в переменную
    try:
        com = rec.recognize_google(voice, language='ru')  # расшифровывание звука в текст
        print('Вы сказали:', com)
        choose(com)
    except sr.UnknownValueError:
        print('Не могу распознать')
    except sr.RequestError:
        print('Ошибка гугла')
    except sr.WaitTimeoutError:
        print('Не дозвонились')
    # com = input('скажите команду\n')

    pass


def choose(msg):  # выбираем действие
    msg = msg.lower()
    if 'привет' in msg:
        h = random.choice(hellows)
        action(h)
    elif 'пока' in msg:
        action('до свидания')
        os.abort()
    elif 'как дела' in msg:
        action('норм')
    elif 'анекдот' in msg:
        action('купил мужик шляпу, а она ему как раз')
    elif 'фильм' in msg:
        r = random.choice(films)
        action(r)
    elif 'посчитай' in msg:
        if operationRecognize(msg) != 'error':
            action(str(operationRecognize(msg)))
        else:
            action('я вас не поняла, повторите')
    elif 'молодец' in msg:
        action('рада вам помочь')
    else:
        action(msg)
    pass


def action(say):  # выполняем действие
    print('Бот:', say)
    voice = gTTS(say, lang='ru')
    fname = '1.mp3'
    voice.save(fname)
    playsound.playsound(fname)
    os.remove(fname)
    pass


def operationRecognize(text):
    exp = []
    text = text.replace(',', '.')
    text = text.replace('х', 'x')  # русскую на английскую
    text = text.replace('поделить', '/')
    if re.findall('\S+x|x+\S', text):
        text = text.replace('x', ' x ')
    if re.findall('\S+/|/+\S', text):
        text = text.replace('/', ' / ')
    if re.findall('\S+\+|\++\S', text):
        text = text.replace('+', ' + ')
    if re.findall('\S+-|-+\S', text):
        text = text.replace('-', ' - ')
    text = text.split()
    for i in text:
        try:
            exp.append(float(i))
        except:
            pass
        if i in ['+', '-', 'x', '/']:
            exp.append(i)

    for i in range(len(exp)):
        if i % 2 == 0:
            if isinstance(exp[i], str):
                return 'error'
        else:
            if isinstance(exp[i], float):
                return 'error'
    if isinstance(exp[-1], str):
        return 'error'

    i = 0
    while 'x' in exp or '/' in exp and i < len(exp):
        if exp[i] == 'x':
            exp[i] = exp[i - 1] * exp[i + 1]
            exp.pop(i + 1)
            exp.pop(i - 1)
        elif exp[i] == '/':
            exp[i] = exp[i - 1] / exp[i + 1]
            exp.pop(i + 1)
            exp.pop(i - 1)
        else:
            i += 1
    i = 0
    while '+' in exp or '-' in exp and i < len(exp):
        if exp[i] == '+':
            exp[i] = exp[i - 1] + exp[i + 1]
            exp.pop(i + 1)
            exp.pop(i - 1)
        elif exp[i] == '-':
            exp[i] = exp[i - 1] - exp[i + 1]
            exp.pop(i + 1)
            exp.pop(i - 1)
        else:
            i += 1
    if exp[0] == int(exp[0]):
        exp[0] = int(exp[0])
    else:
        exp[0] = round(exp[0], 2)
    return exp[0]





while True:
    listen()
