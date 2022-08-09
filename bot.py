import random
import vk_api
import requests
from connect_to_base import db
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload


class VK:
    def __init__(self, group_id, token, ind_token):
        self.group_id = group_id
        self.token = token
        self.ind_token = ind_token
        self.API_VERSION = '5.81'

    def vk_bot(self):
        global res_partner, image_url, n, result_id, last_name_fav, name_favourite, id_fav
        session = requests.Session()
        vk_session = vk_api.VkApi(token=self.token, api_version=self.API_VERSION)
        upload = VkUpload(vk_session)
        longpoll = VkLongPoll(vk_session, group_id=self.group_id)

        def send_message(user_id, message, keyboard=None, attachment=None):
            post = {
                'user_id': user_id,
                'message': message,
                'random_id': random.randint(1, 5000)
            }
            if attachment is None:
                pass
            else:
                post['attachment'] = attachment
            if keyboard is not None:
                pass
                post['keyboard'] = keyboard.get_keyboard()
            else:
                pass

            vk_session.method('messages.send', post)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                message = event.text.lower()
                user_id = event.user_id
                url = 'https://api.vk.com/method/users.get'
                params = {
                    'user_ids': user_id,
                    'access_token': self.ind_token,
                    'v': '5.131',
                    'fields': 'sex, city'
                }
                res = requests.get(url=url, params=params)

                city = res.json()['response'][0]['city']['id']
                sex = res.json()['response'][0]['sex']
                id_user = res.json()['response'][0]['id']
                name = res.json()['response'][0]['first_name']
                surname = res.json()['response'][0]['last_name']
                db.connect().execute(
                    f"INSERT INTO user_vk (user_vk_id, name, surname) VALUES ('{id_user}','{name}', '{surname}')"
                    f"ON CONFLICT DO NOTHING; ")
                tuple_ = db.connect().execute(
                    f"SELECT * FROM user_vk_partners WHERE user_vk_id = '{id_user}'").fetchall()
                keyboard = VkKeyboard()
                keyboard.add_button(label='Поиск', color=VkKeyboardColor.NEGATIVE)
                keyboard.add_button(label='Посмотреть свой список', color=VkKeyboardColor.NEGATIVE)
                if message == 'посмотреть свой список':
                    if len(tuple_) > 0:
                        tuple_ = db.connect().execute(f"SELECT name, surname FROM partners left join "
                                                      f"user_vk_partners ON partners.partner_vk_id = user_vk_partners.partner_vk_id "
                                                      f"WHERE user_vk_partners.user_vk_id = '{user_id}' ").fetchall()
                        count = 1
                        for i in tuple_:
                            send_message(user_id,
                                         f'{count}. {i[0]} {i[1]}', keyboard=keyboard)
                            count = count + 1
                    else:
                        send_message(user_id,
                                     f'У Вас еще нет своего списка. Пожалуйста нажмите поиск и добавьте кого - нибудь', keyboard=keyboard)

                elif message == 'поиск':
                    keyboard.add_button('Добавить в избранное', color=VkKeyboardColor.PRIMARY)
                    if sex == 2:
                        sex = 1
                    elif sex == 1:
                        sex = 2
                    count = 0
                    while count == 0:
                        url = 'https://api.vk.com/method/users.search'
                        params = {
                            'access_token': self.ind_token,
                            'v': '5.131',
                            'city': city,
                            'sex': sex,
                            'status': 1,
                            'count': 1,
                            'offset': random.randint(1, 100),
                            'fields': 'city, sex, photo_max, photo_max_orig',

                        }
                        res_partner = requests.get(url=url, params=params)
                        tuple_ = db.connect().execute(f"SELECT * FROM user_vk_partners WHERE user_vk_id='{user_id}' "
                                                      f"AND partner_vk_id = '{res_partner.json()['response']['items'][0]['id']}' ").fetchone()
                        print('Мой список', tuple_)

                        if not res_partner.json()['response']['items'][0]['is_closed'] and tuple_ is None:
                            count = 1
                            result_id = res_partner.json()['response']['items'][0]['id']

                    name_favourite = res_partner.json()['response']['items'][0]['first_name']
                    last_name_fav = res_partner.json()['response']['items'][0]['last_name']
                    id_fav = res_partner.json()['response']['items'][0]['id']

                    url = 'https://api.vk.com/method/photos.get'
                    params = {
                        'owner_id': result_id,
                        'access_token': self.ind_token,
                        'v': '5.131',
                        'album_id': 'profile',
                        'extended': 1
                    }
                    res_photo = requests.get(url=url, params=params)
                    dict_photos = res_photo.json()['response']['items']
                    list_count_likes = []
                    for i in dict_photos:
                        list_count_likes.append(i['likes']['count'])

                    list_count_likes.sort()
                    print(list_count_likes[-3:])
                    list_urls = []
                    for i in list_count_likes[-3:]:
                        for k in dict_photos:
                            if i == k['likes']['count']:
                                list_urls.append(k['sizes'][-1]['url'])
                    my_dict = dict(zip(list_count_likes[-3:], list_urls))

                    count = 1
                    for k, i in sorted(my_dict.items(), reverse=True):
                        name_favourite = res_partner.json()['response']['items'][0]['first_name']
                        last_name_fav = res_partner.json()['response']['items'][0]['last_name']
                        image_url = i
                        image = session.get(image_url, stream=True)
                        photo = upload.photo_messages(photos=image.raw)[0]
                        attachments = 'photo{}_{}'.format(photo['owner_id'], photo['id'])
                        send_message(user_id,
                                     f'Фотография  пользователя {name_favourite} {last_name_fav} # {count}, с количеством лайков {k}',
                                     attachment=attachments, keyboard=keyboard)
                        count = count + 1
                elif message == 'добавить в избранное':
                    tuple_ = db.connect().execute(f"SELECT * FROM user_vk_partners WHERE "
                                                  f"user_vk_id = '{id_user}' AND partner_vk_id = '{id_fav}'").fetchall()
                    print(tuple_)
                    if len(tuple_) == 0:
                        db.connect().execute(
                            f"INSERT INTO partners (partner_vk_id, name, surname) VALUES ('{id_fav}', '{name_favourite}', '{last_name_fav}')"
                            f"ON CONFLICT DO NOTHING")
                        db.connect().execute(
                            f"INSERT INTO user_vk_partners (user_vk_id, partner_vk_id) VALUES ('{id_user}', '{id_fav}')"
                            f"ON CONFLICT DO NOTHING")
                        send_message(user_id,
                                     f'{name_favourite} {last_name_fav} c идентификатором {id_fav} добавлен в Базу данных',
                                     keyboard=keyboard)
                    else:
                        send_message(user_id,
                                     f'{name_favourite} {last_name_fav} c идентификатором {id_fav} уже есть в базе данных',
                                     keyboard=keyboard)
                else:
                    send_message(user_id, 'Я вас не понимаю! :(')
