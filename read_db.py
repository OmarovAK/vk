from write_db import read_password, create_engine
from sqlalchemy.orm import sessionmaker
from models import User_vk, Black_list, Favorite_partners, Partners


def read_black_list(user_vk_id):
    '''На вход ID пользователя, возвращает список из ID забаненных
    использовать для фильтрации при выводе новых партнеров'''

    Session = sessionmaker(bind=create_engine(read_password()))
    session = Session()
    result = []
    for c in session.query(Black_list).filter(Black_list.user_vk_id == user_vk_id).all():
        result.append(c.info())
    session.close()
    return result


def read_favorite_partners(user_vk_id):
    '''На вход ID пользователя, возвращает список из ID избранных
    использовать для фильтрации при выводе новых партнеров'''

    Session = sessionmaker(bind=create_engine(read_password()))
    session = Session()
    result = []
    if session.query(Favorite_partners).filter(Favorite_partners.user_vk_id == user_vk_id).all():
        for c in session.query(Favorite_partners).filter(Favorite_partners.user_vk_id == user_vk_id).all():
            result.append(c.partner_vk_id)
    session.close()
    return result


def read_favorite_partners_all(partner_vk_id):
    '''На вход ID партнера, возвращает список избранных в формате:
    dict[id_partner] = [имя, фамилия]'''
    # Возможны изменения, функция декаративная, нужна только для информационного вывода избранных партнеров

    Session = sessionmaker(bind=create_engine(read_password()))
    session = Session()
    result = dict()

    for c in session.query(Partners).join(Favorite_partners.partners).filter(Favorite_partners.partner_vk_id == partner_vk_id).all():
        result[partner_vk_id] = [c.name, c.surname, c.profile_link]

    session.close()
    return result


def user_vk_search(user_vk_id):
    '''На вход ID пользователя, возвращает значение Bool'''

    Session = sessionmaker(bind=create_engine(read_password()))
    session = Session()
    if session.query(User_vk).filter(User_vk.user_vk_id == user_vk_id).all():
        result = True
    else:
        result = False
    session.close()
    return result


def user_vk_partner_search(user_vk_id, partner_vk_id):
    '''На вход ID пользователя и ID Партнера, возвращает значение Bool'''

    Session = sessionmaker(bind=create_engine(read_password()))
    session = Session()
    if session.query(Favorite_partners).filter(Favorite_partners.user_vk_id == user_vk_id,
                                               Favorite_partners.partner_vk_id == partner_vk_id).all():
        result = True
    else:
        result = False
    session.close()
    return result

def partner_vk_search(partner_vk_id):
    '''На вход ID пользователя, возвращает значение Bool'''
    Session = sessionmaker(bind=create_engine(read_password()))
    session = Session()
    if session.query(Partners).filter(Partners.partner_vk_id== partner_vk_id).all():
        result = True
    else:
        result = False
    session.close()
    return result


