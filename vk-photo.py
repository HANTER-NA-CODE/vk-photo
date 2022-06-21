'''*******************************************************   БИБЛИОТЕКИ  **************************************************************'''

import sqlite3
from requests import get, post
from os import system 
from time import sleep





'''********************************************************   ЦВЕТА   *****************************************************************'''

white   = '\033[38;5;255m'     # белый
gray    = '\033[38;5;246m'     # серый
text    = '\033[38;5;181m'     # цвет для обычного текста || типо оранжевого
text2   = '\033[38;5;225m'     # цвет для обычного текста || типо розового
blue    = '\033[38;5;27m'      # синий
red     = '\033[38;5;196m'     # красный
green   = '\033[38;5;47m'      # зелённый
purple  = '\033[38;5;200m'     # фиолетовый
purple2 = '\033[38;5;164m'     # фиолетовый2
sbros   = '\033[0m'            # сбросить настройки




'''*****************************************************   БАЗА ДАННЫХ   **************************************************************'''

conn = sqlite3.connect('token.db') #база данных
cur = conn.cursor() #курсор бд

cur.execute("""CREATE TABLE IF NOT EXISTS user(token TEXT)""")
conn.commit()





'''**********************************************************   vk.py   **************************************************************'''

def auth(token, vers):
    global TOKEN, VERSION
    TOKEN = token
    VERSION = vers


def vk(METHOD, **params):
    PARAMS = ''
    for argument, meaning in params.items():
        PARAMS += argument + '=' + str(meaning) + '&'

    response = get(f"https://api.vk.com/method/{METHOD}?{PARAMS}access_token={TOKEN}&v={VERSION}").json()
    try:
        return response['response']
    except:
        print(response)



'''**********************************************************   БАННЕР   **************************************************************'''

def banner():
    system("cls")
    print(f"{blue}       _     {purple}     { white }          "); sleep(0.02)
    print(f"{blue}      | | __ {purple} P   { white } --^--^-- "); sleep(0.02)
    print(f"{blue} __   |_ / / {purple} H   {purple2}  HANTER  "); sleep(0.02)
    print(f"{blue} \ \  / / /  {purple} O   {purple2}    NA    "); sleep(0.02)
    print(f"{blue}  \ \/ /  \  {purple} T   {purple2}   CODE   "); sleep(0.02)
    print(f"{blue}   \__/_|\_\ {purple} O   { white } <------> "); sleep(0.02)





'''******************************************************   СМЕНИТЬ ТОКЕН   **************************************************************'''

def sm_token():
    print()
    print(f"{text}  получить {red}access token"); sleep(0.02)
    print(f"{text}  можно по ссылке {red}https://vkhost.github.io\n")
    print(f"{red}  [{white}0{red}]{text} для отмены\n\n"); sleep(0.02)
    pok = input(f"{green} token: {text2}"); print(f"{white}")
    if pok == '0':
        pass
    else:
        cur.execute(f"INSERT INTO user VALUES('{pok}')")
        conn.commit()
    banner()
    return menu()






'''*********************************************************   MAIN   *****************************************************************'''

def main():
    #проверка токена
    try:
        cur.execute(f"SELECT token FROM user")
        li = cur.fetchall()
        auth(token = li[-1][0], vers = 5.131)
        user = vk('account.getProfileInfo')['id']
    except:
        print()
        print(f' {red}ОШИБКА {white}скорее всего неверный токен или нет доступа в интернет\n')
        input(f" {green}введите что-нибудь, чтобы вернуться в меню: {text2}")
        banner()
        return menu()
    
    #подменю
    print(); sleep(0.02)
    print(f" {red}[{white}1{red}]{text} создать новый альбом"); sleep(0.02)
    print(f" {red}[{white}2{red}]{text} использовать уже существующий альбом"); sleep(0.02)
    print(f" {red}[{white}0{red}]{text} назад"); sleep(0.02)
    print(f'{white}'); sleep(0.02)
    def vibr():
        global albom
        pok = input(f"{green} выбери вариант: {text2}"); print(f'{white}')


        if pok == '1':
            try:
                albom = vk('photos.createAlbum', title= input(f' {green}название для нового альбома: {text2}'))
            except:
                print()
                print(f'{red} ОШИБКА {white}скорее всего неверный токен или нет доступа в интернет\n')
                input(f"{green} введите что-нибудь, чтобы вернуться в меню: {text2}")
                banner()
                return menu()

        elif pok == '2':
            albomes = vk('photos.getAlbums')['items']
            alboms = []
            maxs = 0

            for i in range(len(albomes)):
                alboms.append(
                    {
                        'rowid': i + 1,
                        'id': albomes[i]['id'],
                        'title': albomes[i]['title']
                    }
                )
                if len(str(i + 1)) > maxs:
                    maxs = len(str(i + 1))

            print(f'{purple}        альбомы   \n'); sleep(0.02)
            for i in alboms:
                print(f'{text}   ' + str(i['rowid']) + ' '*(maxs+1 -len(str(i['rowid']))) + f'{sbros}| ' + f'{text2}' + str(i['title'])); sleep(0.02)
            print(sbros)

            def rowid():
                while True:
                    rowid = input(f"{green} номер альбома: {text}")
                    
                    for i in alboms:
                        if str(i['rowid']) == rowid:
                            return i['id']
                    
                    print(f'\n {red}ОШИБКА {white}такого альбома не существует\n')

            albom = rowid()

        elif pok == '0':
            banner()
            return menu()

        else:
            print(f'{red} ОШИБКА{white} скорее всего вы что то неправильно ввели\n')
            return vibr() 
    vibr()

    print()
    def pyt():
        while True:
            pyt = input(f"{green} путь к фотке {gray}(расположение на устройстве){green}: {text2}")
            try:
                f = open(pyt, 'rb')
                f.close()
                return pyt
            except:
                print(f'\n {red}ОШИБКА{white} неверный путь\n')
            
    pyt = pyt()


    print()
    count = int(input(f"{green} количество фоток: {text2}"))
    print()
    sek = int(input(f"{green} задержка в секундах между отпрвками фоток: {text2}"))
    print()

    def main2(count, count2):
        while True:
            try:
                for i in range(count2, count):
                    i += 1
                    server = vk('photos.getUploadServer', album_id= str(albom))
                    url = server['upload_url']                              #ссылка для загрузки файла
                    response = post(url, files={'file': open(pyt, 'rb')})   #загрузка файла
                    file = response.json()                                  #ответ сервера
                    save = vk('photos.save',
                            album_id=    str(albom),               
                            server=      str(file['server']),      
                            photos_list= str(file['photos_list']), 
                            hash=        str(file['hash']),        )

                    heh = len(str(count)) + 1 
                    
                    
                    he = save[0]['id']
                    #print(f'{white}' + str(i) + ' '*(heh - len(str(i))) + f'{gray}---' + f'{green} успех' + f'{white}')
                    print(f'\r {green}загруженно {text2}{i}{white} / {purple2}{count}          {gray}стоп [ctrl + c]', end='')
                    sleep(sek)
                break
            except KeyboardInterrupt:
                print(); sleep(0.02)
                print(f"\n {red}[{white}0{red}]{text} для выхода"); sleep(0.02)
                print(); sleep(0.02)
                pok = input(f"{green} введите что-нибудь для продолжения: {text2}")

                if pok == '0':
                    return 0
                else:
                    print()
                    count2 = i - 1
                    i2 = i - 2
                    print(f'\r {green}загруженно {text2}{i2}{white} / {purple2}{count}           {gray}стоп [ctrl + c]', end='')
    print(f'\r {green}загруженно {text2}0{white} / {purple2}{count}           {gray}стоп [ctrl + c]', end='')
    main2(count, 0)
    print(sbros, end='')








'''***********************************************************   МЕНЮ   *****************************************************************'''

def menu():
    print(); sleep(0.02)
    print(f" {red}[{white}1{red}]{text} запустить"); sleep(0.02)
    print(f" {red}[{white}2{red}]{text} сменить токен"); sleep(0.02)
    print(f" {red}[{white}0{red}]{text} закрыть"); sleep(0.02)
    print(f"{white}"); sleep(0.02)
    def vibr():
        pok = input(f"{green} выбери вариант: {text2}"); print(f"{white}")
        if pok == '1':
            banner()
            return main()
        elif pok == '2':
            banner()
            return sm_token()
        elif pok == '0':
            return 0
        else:
            print(f'{red} ОШИБКА{white} скорее всего вы что то неправильно ввели\n')
            return vibr()
    vibr()






'''******************************************************   ВЫЗОВ МЕНЮ   ***************************************************************'''

banner()
menu()
