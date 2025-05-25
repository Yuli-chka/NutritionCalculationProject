import json
import os

AUTH_FILE = 'authorization.json'

def load_auth_data():
    """Загрузка данных из authorization.json."""
    if not os.path.exists(AUTH_FILE):
        return {}
    with open(AUTH_FILE, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def save_auth_data(data):
    """Сохранение данных в authorization.json."""
    with open(AUTH_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_user_auth(name, params):
    """Добавление или обновление авторизации пользователя."""
    auth_data = load_auth_data()
    auth_data[name] = params
    save_auth_data(auth_data)

def get_user_auth(name):
    """Получение авторизационных данных пользователя по имени."""
    auth_data = load_auth_data()
    return auth_data.get(name)

def delete_user_auth(name):
    """Удаление данных пользователя из authorization.json."""
    auth_data = load_auth_data()
    if name in auth_data:
        del auth_data[name]
        save_auth_data(auth_data)
        return True
    return False

def get_user_auth(name):
    """Получение авторизационных данных пользователя по имени."""
    auth_data = load_auth_data()
    return auth_data.get(name)


