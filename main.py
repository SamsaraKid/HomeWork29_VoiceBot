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
        voice = rec.listen(source, phrase_time_limit=5)  # запись того что с микрофона в течении 3 сек в переменную
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
        res, code = operationRecognize(msg)
        if res == 'error':
            match code:
                case 1:
                    action('пустое выражение. повторите ввод')
                case 2:
                    action('выражение начинается на знак. повторите ввод')
                case 3:
                    action('выражение оканчивается на знак. повторите ввод')
                case 4:
                    action('в выражении два знака подряд. повторите ввод')
                case 5:
                    action('в выражении два числа подряд. повторите ввод')
        else:
            action(str(res))
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


def calculate(a, oper, b):  # выполнение операций
    match oper:
        case '+':
            return a + b
        case '-':
            return a - b
        case 'x':
            return a * b
        case '/':
            return a / b


def operationRecognize(text):
    exp = []

    # заменяем разные символы и выражения на нужные
    text = text.replace(',', '.')
    text = text.replace('х', 'x')  # русскую на английскую
    text = text.replace('поделить', '/')
    text = text.replace('дробью', '/')
    text = text.replace('минус', '-')

    # если знак "прилип" к числу, ставим вокруг знака пробелы, можно корректно обрабатывать "три-вторых"
    if re.findall('\S\/|\/\S', text):
        text = text.replace('/', ' / ')

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
    if not exp:
        return 'error', 1

    if exp[0] == '-' and isinstance(exp[1], float):       # если выражение начинается с '-', и следующее число
        exp[1] = -exp[1]                                  # то следующее число делаем отрицательным
        exp.pop(0)                                        # а '-' выбрасываем
    elif exp[0] in ['+', 'x', '/']:                       # если первый элемент не число, то ошибка
        return 'error', 2

    # если последний элемент выражения знак, то ошибка
    if isinstance(exp[-1], str):
        return 'error', 3

    # распознаём отрицательные числа
    i = 1
    while i < len(exp):
        if exp[i] == '-' and isinstance(exp[i - 1], str) and isinstance(exp[i + 1], float): # если до '-' знак, а после число
            exp[i + 1] = -exp[i + 1]                                                        # то меняем знак числа
            exp.pop(i)                                                                      # а '-' выбрасываем
        else:
            i += 1

    # распознаём ошибки:
    expTemp = ' '.join(map(str, exp))
    if re.findall('[+-\/x]\s[+-\/x]\s', expTemp):         # два знака подряд
        return 'error', 4
    elif re.findall('\d\s\d', expTemp):                   # два числа подряд
        return 'error', 5

    # выполняем арифметические действия.
    # сначала все умножения и деления слева направо,
    # потом сложения и вычитания слева направо.
    # после нахождения очередного знака, выполняем его действие с соседними числами,
    # результат записываем в массив вместо знака, а соседние числа выкидываем из массива
    # всё это делаем пока в массиве есть нужный знак
    i = 1
    while 'x' in exp or '/' in exp:
        if exp[i] in ['x', '/']:
            exp[i] = calculate(exp[i - 1], exp[i], exp[i + 1])
            exp.pop(i + 1)
            exp.pop(i - 1)
        else:
            i += 1
    i = 1
    while '+' in exp or '-' in exp:
        if exp[i] in ['+', '-']:
            exp[i] = calculate(exp[i - 1], exp[i], exp[i + 1])
            exp.pop(i + 1)
            exp.pop(i - 1)
        else:
            i += 1

    # выводим результат. если целый, преобразуем его в int. если не целый, округляем до 2 цифр после запятой
    if exp[0] == int(exp[0]):
        exp[0] = int(exp[0])
    else:
        exp[0] = round(exp[0], 2)
    return exp[0], 0





while True:
    listen()


