from  api import PetFriends
from  settings import valid_email, valid_password
import requests
import time


pf = PetFriends()


# В некоторых проверках я не использовал переменную "result", запрашивая списки питомцев
# отдельным вызовом функции "get_list_of_pets", так как в некоторых случаях сервер возвращает ответ в формате HTML

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    """Positive:   Проверка аторизации с валидными данными"""

    status, result = pf.get_api_key(email, password)
    assert  status == 200, "Ожидаемый статус: 200, полученный статус: {}".format(status)
    assert 'key' in result,"Авторизация не удалась"

def test_get_all_pets_valid_key(filter=''):
    """Positive:   Проверка получения списка карточек питомцев"""


    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200, "Ожидаемый статус: 200, полученный статус: {}".format(status)
    assert len(result['pets']) > 0, "В ответе сервера отсутствуют карточки питомцев"


def test_add_pet_with_photo(name="Милёнок", animal_type="Бог собак", age=99,
                            pet_photo='images/milay.jpeg'):
    """Positive:   Проверка создания карточки питомца с валидными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert result['name'] == name, "Питомец не создан"
    assert status == 200, "Ожидаемый статус: 200, полученный статус: {}".format(status)


def test_delete_pet():
    """Positive:   Проверка удаления  карточки питомца с валидными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(MyPets['pets']) == 0:
        pf.add_new_pet(auth_key, name="кукиш", animal_type="страхолюдство", age="1", pet_photo="images/reser.jpeg")
        _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = MyPets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert  status == 200, "Ожидаемый статус: 200, полученный статус: {}".format(status)

    # Проверка того, что  питомец был удалён:
    delete = 1
    for pet in MyPets['pets']:
        if pet_id == pet['id']:
            delete = 0
    assert delete == 1, "Удаление  питомца не удалось"




def test_add_pet_without_photo(name='Весельчак', animal_type='Забавыш', age=21):
    """Positive:   Проверка создания карточки питомца без фотографии с валидными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)

    assert result['name'] == name, "Питомец не создан"
    assert status == 200, "Ожидаемый статус: 200, полученный статус: {}".format(status)

def test_update_pet(name='Тот же Вeсельчак', animal_type='По-прежнему забавыш',
                          age=21):
    """Positive:   Проверка изменения данных в карточке питомца с валидными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(MyPets['pets']) == 0:
        pf.add_pet_without_photo(auth_key,'имечко', "дворняга", 1)
        _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = MyPets['pets'][0]['id']
    status, result = pf.update_pet(auth_key, pet_id,  name, animal_type, age)
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200, "Ожидаемый статус: 200, полученный статус: {}".format(status)
    assert MyPets['pets'][0]['name'] == name, "Имя питомца не соответствует обновленным данным"


def test_set_photo():
    """Positive:   Проверка добавления фотографии в существующую карточку питомца  с валидными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаётся питомец с идентичной фотографией для последующего получения этого изображения в формате base64
    # и сравнения с ответом сервера на добавление фото к карточке существующего питомца:
    pf.add_new_pet(auth_key, name='Тимошенька', animal_type="Прелесть райская", age=8, pet_photo='images/reser.jpeg')
    # Получение id питомца для его удаления:
    _, My_Pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = My_Pets['pets'][0]['id']
    # Получение фото питомца в формате base64:
    base64_ = My_Pets["pets"][0]["pet_photo"]
    # Удаляется  питомец , добавленный для получения base64:
    pf.delete_pet(auth_key, pet_id)

    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(MyPets['pets'][0]['pet_photo']) > 20 :
        pf.add_pet_without_photo(auth_key, name='hover', animal_type='huver', age=3)
        _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = MyPets['pets'][0]['id']
    status, result = pf.set_photo_of_pet(auth_key, pet_id, pet_photo='images/reser.jpeg')
    _, MyPets = pf.get_list_of_pets(auth_key, 'my_pets')
    base64_1 = My_Pets["pets"][0]["pet_photo"]
    assert status == 200, "Ожидаемый статус: 200, полученный статус: {}".format(status)
    assert base64_ == base64_1, "Фото не добавлено"



def test_add_new_pet_without_name(name= None, animal_type="интеллектуал", age=7, pet_photo='images/images.jpeg'):
    """Negative:   Проверка на невозможность добавления питомца без имени"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Исходим из того, что сервер должен корректно обрабатывать подобные запросы,
    # возвращая ошибку со стороны клиента
    assert  400 <= status < 500, "Ожидаемый статус: 4xx, полученный статус: {}".format(status)


def test_delete_without_access():
    """Negative:   Проверка возможности удаления карточки питомца ,заведённой другим пользователем"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, Pets = pf.get_list_of_pets(auth_key, '')
    _, My_Pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверка, что первый в списке питомец не входит в список питомцев пользователя с введенными
    # аутентификационными данными:
    number_of_pet = 0
    while Pets['pets'][number_of_pet]['id'] == My_Pets['pets'][0]['id']:
        number_of_pet +=1
    pet_id = Pets['pets'][number_of_pet]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Исходим из того, что сервер должен корректно обрабатывать подобные запросы,
    # возвращая ошибку доступа со стороны клиента:
    assert  status == 403, "Ожидаемый статус: 403, полученный статус: {}".format(status)
    _, Pets = pf.get_list_of_pets(auth_key, '')
    # Проверка того, что чужой питомец не был удалён:
    not_delete = 0

    for pet in Pets['pets']:
        if pet_id == pet['id']:
            not_delete = 1
    assert not_delete == 1, "Удаление чужого питомца удалось"

def test_update_pet_without_access(name='Васиссуалий', animal_type='Лоханкин',
                          age=21):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, Pets = pf.get_list_of_pets(auth_key, '')
    _, My_Pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверка, что первый в списке питомец не входит в список питомцев пользователя с введенными
    # аутентификационными данными:
    number_of_pet = 0
    while Pets['pets'][number_of_pet]['id'] == My_Pets['pets'][0]['id']:
        number_of_pet += 1
    pet_id = Pets['pets'][number_of_pet]['id']
    status, result = pf.update_pet(auth_key, pet_id,  name, animal_type, age)


    assert  status != 200
    assert  result['name'] != name


def test_get_api_key_whitout_password(email = valid_email, password = ''):
    """Positive:   Проверка аторизации с неаполненым полем "PASSWORD"""

    status, result = pf.get_api_key(email, password)
    assert  status != 200, "Ожидаемый статус: 4xx, полученный статус: {}".format(status)
    assert 'key' not in result,"Авторизация удалась"



