import requests
from app import conf

ID_KEY = conf.getSetting('VK', 'id_key')
SECURE_KEY = conf.getSetting('VK', 'secure_key')
SERVICE_KEY = conf.getSetting('VK', 'service_key')
VERSION = conf.getSetting('VK', 'version')


def refactDict(func):
    # Декоратор для измения списка словарей друзей
    def wrapper(accesToken):
        friends = func(accesToken)
        for friend in friends:
            if 'sex' in friend:
                if friend['sex'] == 0:
                    friend['sex'] = 'не указан'
                elif friend['sex'] == 1:
                    friend['sex'] = 'женский'
                elif friend['sex'] == 2:
                    friend['sex'] = 'мужской'
            if 'online' in friend:
                if friend['online'] == 0:
                    friend['online'] = 'оффлайн'
                elif friend['online'] == 1:
                    friend['online'] = 'онлайн'
            if 'country' not in friend:
                friend['country'] = {'title': 'не указана'}
            if 'city' not in friend:
                friend['city'] = {'title': 'не указан'}
        return friends

    return wrapper


@refactDict
def getFriendsByToken(access_token):
    # Получение друзей пользователя с использованием токена
    friends = []
    fields = ['country', 'city', 'sex', 'photo_200_orig', ]
    responce = requests.get('https://api.vk.com/method/friends.get',
                            params={'access_token': access_token, 'order': 'random', "v": VERSION,
                                    'fields': ', '.join(fields), 'count': 5})
    if 'error' not in responce:
        friends = responce.json()['response']['items']
    return friends


@refactDict
def getFriendsById(idUser):
    # Получение списка друзей по его vk ID
    friends = []
    fields = ['country', 'city', 'sex', 'photo_200_orig', ]
    responce = requests.get('https://api.vk.com/method/friends.get',
                            params={'access_token': SERVICE_KEY, 'user_id': idUser, 'order': 'random', "v": VERSION,
                                    'count': 5})
    responce = responce.json()
    if 'error' not in responce:
        idFriends = responce['response']['items']
        friends = list(map(getUserDataById, idFriends))
    print(friends)
    return friends


def getUserDataByToken(access_token):
    # Получение имени и фамилии пользователя по токену
    responce = requests.get('https://api.vk.com/method/users.get',
                            params={'access_token': access_token, "v": VERSION, 'name_case': 'gen'})
    responce = responce.json()
    userName = responce['response'][0]
    return userName


def getUserDataById(idUser):
    # Получение имени и фамилии пользователя по vk id
    fields = ['country', 'city', 'sex', 'photo_200_orig', 'online']
    responce = requests.get('https://api.vk.com/method/users.get',
                            params={'user_id': idUser, 'access_token': SERVICE_KEY, "v": VERSION, 'name_case': 'gen',
                                    'fields': ', '.join(fields)})
    responce = responce.json()
    userName = responce['response'][0]
    return userName


def getAccessKey(code):
    responce = requests.get('https://oauth.vk.com/access_token',
                            params={'client_id': ID_KEY, 'client_secret': SECURE_KEY,
                                    'redirect_uri': 'https://flaskvkapitest.herokuapp.com', 'code': code})
    if responce.status_code == 200:
        data = responce.json()
        try:
            access_token = data['access_token']
        except KeyError:
            access_token = None
    return access_token
