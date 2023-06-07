import requests
import json
from settings import valid_email, valid_password
class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:
        """ Метод авторизкется на сервере с указанными email и password и
         возвращает auth_key при успешной авторизации"""


        data = {
            'email': email,
            'password': password
            }
        res = requests.get(self.base_url+'/api/key', headers=data)
        status = res.status_code
        result = ''

        try:
            result = res.json()
        except:
            result = res.text

        return status, result
    def get_list_of_pets(self, auth_key:str, filter: str = "") -> json:
        """Метод получает список питомцев с указанным фильтром "my_pets" - возвращает объект json со списком питомцев
         пользователя, при пустом значении ключа "filter" - возвращает список всех питомцев """
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ''

        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_new_pet(self, auth_key:str, name:str, animal_type:str, age:int, pet_photo:str) -> json:
        """Метод добавляет питомца с указанными данными и возвращает json-объект с данными нового питомца"""
        data = {
            'name': name,
            'animal_type': animal_type,
            'age' : age
        }

        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url+'api/pets', headers=headers, data=data, files=file)

        status = res.status_code

        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: str, pet_id: str) -> json:
        """Метод удаляет питомца с указанным id и возвращвет статус запроса  """
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url+'api/pets/'+pet_id, headers=headers)

        status = res.status_code

        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_pet_without_photo(self, auth_key: str, name: str, animal_type: str, age: int):

        """Метод добавляет питомца без фотографии с указанными данными"""

        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age}

        res = requests.post(self.base_url+'/api/create_pet_simple', headers=headers, data=data)

        status = res.status_code

        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def update_pet(self, auth_key: str, pet_id: str, name: str, animal_type: str, age: int):
        """Метод изменяет данные питомца с указанным id"""
        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age}


        res = requests.put(self.base_url+'/api/pets/'+pet_id, headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return  status, result
    def set_photo_of_pet(self, auth_key, pet_id, pet_photo):
        """Метод добавляет фото существующего питомца c  указанным id """
        headers = {'auth_key': auth_key['key']}
        files = {'pet_photo':(pet_photo, open(pet_photo, 'rb'), 'image/jpeg' )}
        res = requests.post(self.base_url+'/api/pets/set_photo/'+pet_id, headers=headers, files=files)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result











