'''*******************************************************   БИБЛИОТЕКИ  **************************************************************'''

import sqlite3
from requests import get, post
from os import system as terminal
from time import sleep





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
    return get(f"https://api.vk.com/method/{METHOD}?{PARAMS}&access_token={TOKEN}&v={version}").json()['response']





'''**********************************************************   БАННЕР   **************************************************************'''

def banner():
    terminal("clear")
    print("\033[34m   ___    ___   ___    ___   __ --- __    \033[35m        "); sleep(0.02)
    print("\033[34m   \  \  /  /   \  \  /  /  |  |  /   |   \033[00m ------ "); sleep(0.02)
    print("\033[34m    \  \/  /     \  \/  /   |  | /    |   \033[35m HANTER "); sleep(0.02)
    print("\033[34m     \    /       \    /    |  |/     |   \033[35m   NA   "); sleep(0.02)
    print("\033[34m     /    \        /  /     |     /|  |   \033[35m  CODE  "); sleep(0.02)
    print("\033[34m    /  /\  \      /  /      |    / |  |   \033[00m ------ "); sleep(0.02)
    print("\033[34m   /__/  \__\    /__/       |__ /  |__|   \033[35m        "); sleep(0.02)
    print("\033[34m                                          \033[35m        "); sleep(0.02)





'''******************************************************   СМЕНИТЬ ТОКЕН   **************************************************************'''

def sm_token():
    print("\033[93m  получить \033[91maccess token"); sleep(0.02)
    print("\033[93m  можно по ссылке \033[91mhttps://vkhost.github.io\n")
    print("\033[91m  [\033[0m0\033[91m]\033[93m для отмены\n\n"); sleep(0.02)
    pok = input("\033[92m token: \033[96m"); print("\033[0m")
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
        user = method('account.getProfileInfo')['id']
    except:
        print()
        print('\033[91m ОШИБКА\033[0m скорее всего неверный токен или нет доступа в интернет\n')
        input("\033[92m введите что-нибудь, чтобы вернуться в меню: \033[96m")
        banner()
        menu()
        return 0
    
    #подменю
    print(); sleep(0.02)
    print(" \033[91m[\033[0m1\033[91m]\033[93m создать новый альбом"); sleep(0.02)
    print(" \033[91m[\033[0m2\033[91m]\033[93m использовать уже существующий"); sleep(0.02)
    print(" \033[91m[\033[0m0\033[91m]\033[93m назад"); sleep(0.02)
    print("\033[0m"); sleep(0.02)
    def vibr():
        global albom
        pok = input("\033[92m выбери вариант: \033[96m"); print("\033[0m")

        if pok == '1':
            try:
                albom = method('photos.createAlbum', 'title=' + input('\033[92m название для нового альбома: \033[96m'))
            except:
                print()
                print('\033[91m ОШИБКА\033[0m скорее всего неверный токен или нет доступа в интернет\n')
                input("\033[92m введите что-нибудь, чтобы вернуться в меню: \033[96m")
                banner()
                menu()
                return 0
        elif pok == '2':
            alboms = method('photos.getAlbums')

            print('\033[91m   айди альбома         \033[92m название альбома\n'); sleep(0.02)
            for i in alboms['items']:
                print('\033[91m' + '   ' + str(i['id']) + ' '*(15-len(str(i['id']))) + '\033[35m' + ' ---   ' + '\033[92m' + str(i['title'])); sleep(0.02)
            print('\033[0m')

            pok = input("\033[92m айди нужного альбома: \033[96m")
            albom = {'id': int(pok)}
        elif pok == '0':
            banner()
            menu()
            return True
        else:
            print('\033[91m ОШИБКА\033[0m скорее всего вы что то неправильно ввели\n')
            vibr()
            return 0
    if vibr():
        return 0

    pyt = input("\033[92m путь к фотке (расположение фотки на устройстве): \033[96m")
    print()
    count = input("\033[92m количество фоток: \033[96m")
    print()
    sek = int(input("\033[92m задержка в секундах между отпрвками фоток: \033[96m"))
    print()
    for i in range(int(count)):
        server = method('photos.getUploadServer', 'album_id=' + str(albom['id'])) 
        url = server['upload_url']                              #ссылка для загрузки файла
        response = post(url, files={'file': open(pyt, 'rb')})   #загрузка файла
        file = response.json()                                  #ответ сервера
        method('photos.save',
               'album_id='    + str(albom['id'])         + '&' +
               'server='      + str(file['server'])      + '&' +
               'photos_list=' + str(file['photos_list']) + '&' +
               'hash='        + str(file['hash'])              )
        sleep(sek)







'''***********************************************************   МЕНЮ   *****************************************************************'''

def menu():
    print(); sleep(0.02)
    print(" \033[91m[\033[0m1\033[91m]\033[93m запустить"); sleep(0.02)
    print(" \033[91m[\033[0m2\033[91m]\033[93m сменить токен"); sleep(0.02)
    print(" \033[91m[\033[0m0\033[91m]\033[93m закрыть"); sleep(0.02)
    print("\033[0m"); sleep(0.02)
    def vibr():
        pok = input("\033[92m выбери вариант: \033[96m"); print("\033[0m")
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
            print('\033[91m ОШИБКА\033[0m скорее всего вы что то неправильно ввели\n')
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
        print('\n\033[0m неизвестная\033[91m ОШИБКА \033[0m\n')
        input("\033[92m введите что-нибудь, чтобы вернуться в меню: \033[96m")
        banner()
        menu()
        return 0

huy()
