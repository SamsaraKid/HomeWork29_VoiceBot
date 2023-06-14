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

    # заменяем разные символы и выражения на нужные
    text = text.replace(',', '.')
    text = text.replace('х', 'x')  # русскую на английскую
    text = text.replace('поделить', '/')
    text = text.replace('минус', '-')
    text = text.replace('число пи', '3.14')

    # если знак "прилип" к числу, ставим вокруг знака пробелы
    if re.findall('\S+x|x+\S', text):
        text = text.replace('x', ' x ')
    if re.findall('\S+/|/+\S', text):
        text = text.replace('/', ' / ')
    if re.findall('\S+\+|\++\S', text):
        text = text.replace('+', ' + ')
    if re.findall('\S+-|-+\S', text):
        text = text.replace('-', ' - ')

    # разделяем получившуюся строку на массив
    text = text.split()

    # из массива выбираем числа и знаки, числа переводим во float. выставляем числа и знаки в новом массиве по порядку
    for i in text:
        try:
            exp.append(float(i))
        except:
            pass
        if i in ['+', '-', 'x', '/']:
            exp.append(i)

    # если в массиве пусто, то выражения нет, ошибка
    if exp == []:
        return 'error'


    if exp[0] == '-' and isinstance(exp[1], float):                                                    # если выражение начинается со знака '-', и следующее число
        exp[1] = -exp[1]                                                                               # то следующее число делаем отрицательным
        exp.pop(0)                                                                                     # а знак '-' выбрасываем


    i = 1
    while i < len(exp):
        if i % 2 == 0:
            if isinstance(exp[i], str):                                                                 # если на чётном месте знак
                if exp[i] == '-' and isinstance(exp[i - 1], str) and isinstance(exp[i + 1], float):     # если этот знак '-' и предыдущее тоже знак и следующее число
                    exp[i + 1] = -exp[i + 1]                                                            # то следующее число делаем отрицательным
                    exp.pop(i)                                                                          # а знак '-' выбрасываем
                    i -= 1                                                                              # и сдвигаем счётчик назад
                else:                                                                                   # в остальных случаях выражение ошибочно
                    return 'error'
        else:
            if isinstance(exp[i], float):                                                               # если на нечётном месте число
                return 'error'                                                                          # то выражение ошибочно
        i += 1


    # если последний элемент выражения знак, то ошибка
    if isinstance(exp[-1], str):
        return 'error'

    # for i in range(len(exp)):
    #     if i % 2 == 0:
    #         if isinstance(exp[i], str):
    #             return 'error'
    #     else:
    #         if isinstance(exp[i], float):
    #             return 'error'


    # выполняем арифметические действия.
    # сначала все умножения и деления слева направо,
    # потом сложения и вычитания слева направо.
    # после нахождения очередного знака, выполняем его действие с соседними числами,
    # результат записываем в массив вместо знака, а соседние числа выкидываем из массива
    # всё это делаем пока в массиве есть нужный знак, или пока не достигнем конца массива
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
