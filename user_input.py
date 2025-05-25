import get_source_data_from_store
from get_calories_from_rezept_and_product import get_calories_from_rezept_and_product


def get_user_data():
    print("Приветствуем вас в программе МенюМастер!\nПожалуйста, введите требуемые данные для получения меню:")
    height_cm = float(input("Ваш рост в сантиметрах: "))
    weight_kg = float(input("Ваш вес в килограммах: "))
    sex = input("Ваш пол (ж/м): ")
    age = float(input("Ваш возраст в годах: "))

    return {'height_cm': height_cm, 'weight_kg': weight_kg, 'sex':sex,  'age':age}

def get_user_menu(calories_needed):
    print("Требуемые калории для поддержания веса:", calories_needed)
    print("Если вы хотите получить ваше меню на день, нажмите 'M'")
    print("Если же вы хотите обновить данные о ассортименте магазина, нажмите 'N'")
    print("Для выхода из программы нажмите 'Q'")

    while True:
        command = input('Введите необходимую команду: ').strip().upper()

        if command == "M":
            print("Загружаем данные о продуктах и рецептах...")
            get_calories_from_rezept_and_product()
        elif command == "N":
            print("Обновление данных о ассортименте магазина...")
            get_source_data_from_store.get_source_data_from_store()
        elif command == "Q":
            print("Завершение работы программы...")
            break
        else:
            print("Неверная команда. Пожалуйста, введите 'M', 'N' или 'Q' для действий.")


