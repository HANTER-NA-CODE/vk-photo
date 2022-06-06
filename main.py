from requests import get, post
from os import system
from time import sleep


def vk(METHOD, PARAMS = ''):
    try:
        return get(f"https://api.vk.com/method/{METHOD}?{PARAMS}&access_token={TOKEN}&v={version}").json()['response']
    except:
        print(get(f"https://api.vk.com/method/{METHOD}?{PARAMS}&access_token={TOKEN}&v={version}").json())

TOKEN = input('токен: ')##
version = '5.131'

'''********************************************************************************************************************************'''

albom = vk('photos.createAlbum', 'title=' + input('название для нового альбома: '))

pyt = input('путь к фотке: ')

for i in range(int(input('сколько фоток: '))):
    server = vk('photos.getUploadServer', 'album_id=' + str(albom['id'])) 
    url = server['upload_url']                              #ссылка для загрузки файла
    response = post(url, files={'file': open(pyt, 'rb')})   #загрузка файла
    file = response.json()                                  #ответ сервера
    vk('photos.save',
       'album_id=' + str(albom['id']) + '&' +
       'server=' + str(file['server']) + '&' +
       'photos_list=' + str(file['photos_list']) + '&' +
       'hash=' + str(file['hash'])
      )
    #sleep(1)
