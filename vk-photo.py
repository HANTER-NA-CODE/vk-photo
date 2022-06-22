'''*******************************************************   БИБЛИОТЕКИ  **************************************************************'''

import sqlite3                  # база данных (бд)
from requests import get, post  # http запросы
from os import system           # взаимодействие с системой
from time import sleep          # таймер





'''********************************************************   ЦВЕТА   *****************************************************************'''

white   = '\033[38;5;255m'     # белый
gray    = '\033[38;5;246m'     # серый
text    = '\033[38;5;181m'     # выод текста || типа оранжевого
text2   = '\033[38;5;225m'     # ввод текста || типа розового
blue    = '\033[38;5;27m'      # синий
red     = '\033[38;5;196m'     # красный
green   = '\033[38;5;47m'      # зелённый
purple  = '\033[38;5;200m'     # фиолетовый
purple2 = '\033[38;5;164m'     # фиолетовый2
sbros   = '\033[0m'            # сбросить настройки




'''*****************************************************   БАЗА ДАННЫХ   **************************************************************'''

conn = sqlite3.connect('token.db')  # создание бд
cur = conn.cursor()                 # курсор бд

cur.execute("""CREATE TABLE IF NOT EXISTS user(token TEXT)""")  # создание таблицы в бд
conn.commit()                                                   # сохранение изменений бд





'''**********************************************************   Vk API   **************************************************************'''

def auth(token, vers):     # авторизация вк
    global TOKEN, VERSION  # глобальное объявление переменных
    TOKEN = token          # токен вк 
    VERSION = vers         # версия апи


def vk(METHOD, **params):  # метод апи вк
    PARAMS = ''            # праметры метода 
    for argument, meaning in params.items():
        PARAMS += argument + '=' + str(meaning) + '&'

    response = get(f"https://api.vk.com/method/{METHOD}?{PARAMS}access_token={TOKEN}&v={VERSION}").json()  # API запрос
    try:
        return response['response']  # возвращает ответ сервера
    except:
        print(red)       # красный текст
        print(response)  # вывод ошибки
        print(sbros)     # сброс цвета



'''**********************************************************   БАННЕР   **************************************************************'''

def banner():
    system("clear")                                                             # *очищает терминал*
    print(f"{blue}       _     {purple}     { white }          "); sleep(0.02)  #        _                    
    print(f"{blue}      | | __ {purple} P   { white } --^--^-- "); sleep(0.02)  #       | | __  P    --^--^-- 
    print(f"{blue} __   |_ / / {purple} H   {purple2}  HANTER  "); sleep(0.02)  #  __   |_ / /  H     HANTER  
    print(f"{blue} \ \  / / /  {purple} O   {purple2}    NA    "); sleep(0.02)  #  \ \  / / /   O       NA    
    print(f"{blue}  \ \/ /  \  {purple} T   {purple2}   CODE   "); sleep(0.02)  #   \ \/ /  \   T      CODE   
    print(f"{blue}   \__/_|\_\ {purple} O   { white } <------> "); sleep(0.02)  #    \__/_|\_\  O    <------> 





'''******************************************************   СМЕНИТЬ ТОКЕН   **************************************************************'''

def sm_token():
    print();                                                           sleep(0.02)  #   получить access token
    print(f"{text}  получить {red}access token");                      sleep(0.02)  #   можно по ссылке https://vkhost.github.io
    print(f"{text}  можно по ссылке {red}https://vkhost.github.io\n"); sleep(0.02)  #   
    print(f"{red}  [{white}0{red}]{text} для отмены\n\n");             sleep(0.02)  #   [0] для отмены

    #  ввод токена
    pok = input(f"{green} token: {text2}")                                          #  token: 

    if pok == '0':  # выход
        pass
    else:
        cur.execute(f"INSERT INTO user VALUES('{pok}')")  # ввод токена в бд
        conn.commit()                                     # сохранение изменений бд

    banner()       # баннер 
    return menu()  # возвращение в меню






'''*********************************************************   MAIN   *****************************************************************'''

def main():
    
    #=============================  проверка токена  ==============================
    try:
        cur.execute(f"SELECT token FROM user")  # открытие базы данных
        token = cur.fetchall()[-1][0]           # получение токена
        auth(token= token, vers= 5.131)         # авторизация вк
        vk('account.getProfileInfo')['id']      # проверка токена
    except:
        print()                                                                                 #  ОШИБКА скорее всего неверный токен или нет доступа в интернет
        print(f' {red}ОШИБКА {white}скорее всего неверный токен или нет доступа в интернет\n')  #
        input(f" {green}введите что-нибудь, чтобы вернуться в меню: {text2}")                   #  введите что-нибудь, чтобы вернуться в меню: 

        banner()       # баннер 
        return menu()  # возвращение в меню
    
    #============================== какой альбом использовать ==============================
    print();                                                                    sleep(0.02)  # 
    print(f" {red}[{white}1{red}]{text} создать новый альбом");                 sleep(0.02)  # [1] создать новый альбом
    print(f" {red}[{white}2{red}]{text} использовать уже существующий альбом"); sleep(0.02)  # [2] использовать уже существующий альбом
    print(f" {red}[{white}0{red}]{text} назад");                                sleep(0.02)  # [0] назад
    print(f'{white}');                                                          sleep(0.02)  # 

    def vibr():
        global albom
        pok = input(f"{green} выбери вариант: {text2}")

        #==============================  новый альбом  ==============================
        if pok == '1':
            try:
                albom = vk('photos.createAlbum', title= input(f' {green}название для нового альбома: {text2}'))  # создание нового альбома
            except:
                print()                                                                                 #  ОШИБКА скорее всего неверный токен или нет доступа в интернет
                print(f'{red} ОШИБКА {white}скорее всего неверный токен или нет доступа в интернет\n')  #
                input(f"{green} введите что-нибудь, чтобы вернуться в меню: {text2}")                   #  введите что-нибудь, чтобы вернуться в меню: 

                banner()       # баннер 
                return menu()  # возвращение в меню

        #==============================  список альбомов  ==============================
        elif pok == '2':
            albomes = vk('photos.getAlbums')['items']  # получение списка альбомов пользователя
            alboms = []                                # список с json данными об альбомах
            maxs = 0                                   # максимальная длина rowid альбомов

            for i in range(len(albomes)):              # заполняет список alboms
                alboms.append({ 'rowid': i + 1,
                                'id': albomes[i]['id'],
                                'title': albomes[i]['title'] })

                if len(str(i + 1)) > maxs:             # максимальная длина rowid
                    maxs = len(str(i + 1))
            
            print()                                                                                                                                    #        альбомы 
            print(f'{purple}        альбомы   \n'); sleep(0.02)                                                                                        # 
            for i in alboms:                                                                                                                           #   1 | lovely
                print(f'{text}   ' + str(i['rowid']) + ' '*(maxs+1 -len(str(i['rowid']))) + f'{sbros}| ' + f'{text2}' + str(i['title'])); sleep(0.02)  #   2 | banner
            #                                                                                                                                          #   3 | cutie
            #*****************************  выбор альбома  ==============================                                                              #   4 | uwu                 
            def rowid():
                while True:
                    rowid = input(f"{green} номер альбома: {text}")                                  # номер альбома:
                    
                    for i in alboms:
                        if str(i['rowid']) == rowid:
                            return i['id']
                    
                    print(f'\n {red}ОШИБКА {white}такого альбома не существует\n')  # ОШИБКА такого альбома не существует

            albom = rowid()

        #==============================  выход  ==============================
        elif pok == '0':
            banner()       # баннер 
            return menu()  # возвращение в меню

        #==============================   перезапуск функции  ==============================
        else:
            print(f'{red} ОШИБКА{white} скорее всего вы что то неправильно ввели\n')
            return vibr() 
    vibr()
    print()

    #==============================  путь к фотке  ==============================
    def pyt():
        while True:
            pyt = input(f"{green} путь к фотке {gray}(расположение на устройстве){green}: {text2}")  # путь к фотке (расположение на устройстве):
            try:
                f = open(pyt, 'rb')  # открывет файл по указанному пути
                f.close()            # закрывает файл
                return pyt
            except:                                              # если не смог открыть файл то:
                print(f'\n {red}ОШИБКА{white} неверный путь\n')  # ОШИБКА неверный путь
            
    pyt = pyt() 
    print()

    #==============================  количество фоток  ==============================
    count = int(input(f"{green} количество фоток: {text2}"))  # количество фоток: 
    print()

    #==============================  задержка  ==============================
    sek = int(input(f"{green} задержка в секундах между отпрвками фоток: {text2}"))                  # задержка в секундах между отпрвками фоток: 
    print()

    #==============================  загрузка  ==============================
    print(f'\r {green}загруженно {text2}0{white} / {purple2}{count}           {gray}стоп [ctrl + c]', end='')                    # загруженно 0 / 1000           стоп [ctrl + c]
    def main2(count, count2):
        while True:
            try:
                for i in range(count2, count):
                    i += 1
                    url = vk('photos.getUploadServer', album_id= str(albom))['upload_url'] #ссылка для загрузки фотографии
                    response = post(url, files={'file': open(pyt, 'rb')}).json()           #загрузка фотографии
                    vk('photos.save',                                                      #сохранение фотографии
                        album_id=    albom,               
                        server=      response['server'],      
                        photos_list= response['photos_list'], 
                        hash=        response['hash']       )

                    print(f'\r {green}загруженно {text2}{i}{white} / {purple2}{count}          {gray}стоп [ctrl + c]', end='')   # загруженно 0 / 1000           стоп [ctrl + c]
                    sleep(sek)  # задержка
                break
            #==============================  стоп  ==============================
            except KeyboardInterrupt:
                print();                                            sleep(0.02)      #
                print(f"\n {red}[{white}0{red}]{text} для выхода"); sleep(0.02)      # [0] для выхода
                print();                                            sleep(0.02)      #
                pok = input(f"{green} введите что-нибудь для продолжения: {text2}")  # введите что-нибудь для продолжения: 

                if pok == '0':
                    return 0  # закрыть код
                else:
                    print()
                    count2 = i - 1
                    print(f'\r {green}загруженно {text2}{i}{white} / {purple2}{count}           {gray}стоп [ctrl + c]', end='')  # загруженно 0 / 1000           стоп [ctrl + c]
            #==============================  неизвестная ошибка  ==============================
            except:
                count2 = i - 1
                print(f'\n {red}ОШИБКА{white} неизвестная ошибка\n')
                sleep(0.5)

    main2(count, 0)
    print(sbros, end='')  # сброс цвета терминала








'''***********************************************************   МЕНЮ   *****************************************************************'''

def menu():
    print();                                             sleep(0.02)        # 
    print(f" {red}[{white}1{red}]{text} запустить");     sleep(0.02)        # [1] запустить
    print(f" {red}[{white}2{red}]{text} сменить токен"); sleep(0.02)        # [2] сменить токен
    print(f" {red}[{white}0{red}]{text} закрыть");       sleep(0.02)        # [0] закрыть
    print(f"{white}");                                   sleep(0.02)        #
    def vibr():
        pok = input(f"{green} выбери вариант: {text2}"); print(f"{white}")  #  выбери вариант: 
        if pok == '1':
            banner()           # баннер 
            return main()      # основной код (main)
        elif pok == '2':
            banner()           # баннер
            return sm_token()  # смена токена
        elif pok == '0':
            return 0           # закрыть код
        else:
            print(f'{red} ОШИБКА{white} скорее всего вы что то неправильно ввели\n')  # ОШИБКА скорее всего вы что то неправильно ввели
            return vibr()  # перезапуск выбора
    vibr()






'''******************************************************   ВЫЗОВ МЕНЮ   ***************************************************************'''

banner()  # баннер
menu()    # меню
