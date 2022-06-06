'''*******************************************************   БИБЛИОТЕКИ  **************************************************************'''

from cgitb import grey
import sqlite3
from requests import get, post
from os import system as terminal
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
    global TOKEN, version
    TOKEN = token
    version = vers


def method(METHOD, PARAMS = ''):
    return get(f"https://api.vk.com/method/{METHOD}?{PARAMS}&access_token={TOKEN}&v={version}").json()





'''**********************************************************   БАННЕР   **************************************************************'''

def banner():
    terminal("clear")
    print(f"{blue}       _     { white }          "); sleep(0.02)
    print(f"{blue}      | | __ { white } --^--^-- "); sleep(0.02)
    print(f"{blue} __   |_ / / {purple2}  HANTER  "); sleep(0.02)
    print(f"{blue} \ \  / / /  {purple2}    NA    "); sleep(0.02)
    print(f"{blue}  \ \/ /  \  {purple2}   CODE   "); sleep(0.02)
    print(f"{blue}   \__/_|\_\ { white } <------> "); sleep(0.02)





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
    menu()
    return 0






'''*********************************************************   MAIN   *****************************************************************'''

def main():
    #проверка токена
    try:
        cur.execute(f"SELECT token FROM user")
        li = cur.fetchall()
        auth(token = li[-1][0], vers = 5.131)
        user = method('account.getProfileInfo')['response']['id']
    except:
        print()
        print(f'{red} ОШИБКА {white}скорее всего неверный токен или нет доступа в интернет\n')
        input(f"{green} введите что-нибудь, чтобы вернуться в меню: {text2}")
        banner()
        menu()
        return 0
    
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
                albom = method('photos.createAlbum', 'title=' + input(f'{green} название для нового альбома: {text2}'))['response']
            except:
                print()
                print(f'{red} ОШИБКА {white}скорее всего неверный токен или нет доступа в интернет\n')
                input(f"{green} введите что-нибудь, чтобы вернуться в меню: {text2}")
                banner()
                menu()
                return 0
        elif pok == '2':
            alboms = method('photos.getAlbums')['response']

            print(f'{red}   айди альбома         {green} название альбома\n'); sleep(0.02)
            for i in alboms['items']:
                print(f'{red}' + '   ' + str(i['id']) + ' '*(15-len(str(i['id']))) + f'{gray}' + ' ---   ' + f'{green}' + str(i['title'])); sleep(0.02)
            print('\033[0m')

            pok = input(f"{green} айди нужного альбома: {text2}")
            albom = {'id': int(pok)}
        elif pok == '0':
            banner()
            menu()
            return True
        else:
            print(f'{red} ОШИБКА{white} скорее всего вы что то неправильно ввели\n')
            vibr()
            return 0
    if vibr():
        return 0

    print()
    pyt = input(f"{green} путь к фотке {gray}(расположение на устройстве){green}: {text2}")
    print()
    count = input(f"{green} количество фоток: {text2}")
    print()
    sek = int(input(f"{green} задержка в секундах между отпрвками фоток: {text2}"))
    print()
    for i in range(int(count)):
        i += 1
        server = method('photos.getUploadServer', 'album_id=' + str(albom['id']))['response']
        url = server['upload_url']                              #ссылка для загрузки файла
        response = post(url, files={'file': open(pyt, 'rb')})   #загрузка файла
        file = response.json()                                  #ответ сервера
        save = method('photos.save',
                      'album_id'    + '=' + str(albom['id'])         + '&' +
                      'server'      + '=' + str(file['server'])      + '&' +
                      'photos_list' + '=' + str(file['photos_list']) + '&' +
                      'hash'        + '=' + str(file['hash'])              )

        heh = len(str(count)) + 1 
        
        try:
            he = save['response'][0]['id']
            print(f'{white}' + str(i) + ' '*(heh - len(str(i))) + f'{gray}---' + f'{green} успех' + f'{white}')
        except:
            print(f'{white}' + str(i) + ' '*(heh - len(str(i))) + f'{gray}---' + f'{red} error {save["error"]["error_code"]} {white}< {save["error"]["error_msg"]} >')

        sleep(sek)







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
            main()
            return 0
        elif pok == '2':
            banner()
            sm_token()
            return 0
        elif pok == '0':
            pass
            return 0
        else:
            print(f'{red} ОШИБКА{white} скорее всего вы что то неправильно ввели\n')
            vibr()
            return 0
    vibr()






'''******************************************************   ВЫЗОВ МЕНЮ   ***************************************************************'''

def huy():
    try:
        banner()
        menu()
        return 0
    except:
        print()
        print(f'\n{white} неизвестная {red}ОШИБКА\n\n')
        input(f"{green} введите что-нибудь, чтобы вернуться в меню: {text2}")
        print(f'{sbros}')
        huy()
        return 0

huy()
