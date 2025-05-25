import pandas as pd
import re
from fuzzywuzzy import process

from settings import recipes_path, product_data_path


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def find_most_similar_product(recipe_name, product_list):
    recipe_name_processed = preprocess_text(recipe_name)
    product_names = product_list['name'].apply(preprocess_text).tolist()
    best_match, score = process.extractOne(recipe_name_processed, product_names)
    if score > 80:
        best_match_index = product_names.index(best_match)
        return product_list.iloc[best_match_index]
    else:
        return None


def calculate_recipe_calories_and_products(recipe_details, product_list, coefficient=1):
    ingredient_str = recipe_details['ingredients']
    ingredient_list = ingredient_str.split(', ')
    total_calories = 0
    product_basket = set()
    not_found = []

    for ingredient in ingredient_list:
        match = re.search(r'\d+', ingredient)
        if match:
            amount = int(match.group()) * coefficient
        else:
            print(f"Не найдено числовое значение в ингредиенте '{ingredient}'")
            continue  # Пропускаем этот ингредиент, если количество не найдено

        ingredient_name = ' '.join(re.findall(r'\D+', ingredient)).strip()
        similar_product = find_most_similar_product(ingredient_name, product_list)
        if similar_product is not None:
            caloric_value = int(similar_product['calories']) if not isinstance(similar_product['calories'], int) else similar_product['calories']
            calories = (amount / 100) * caloric_value
            total_calories += round(calories, 2)
            product_basket.add(similar_product['name'])
        else:
            not_found.append(ingredient_name)

    if not_found:
        print("Не найдены ингредиенты: " + ", ".join(not_found))
    return total_calories, product_basket


def get_calories_from_rezept_and_product():
    df = pd.read_json(recipes_path)
    product_data = pd.read_json(product_data_path)

    # Обработка данных о калориях

    product_data['calories'] = pd.to_numeric(product_data['calories'].str.replace(' ккал', ''), errors='coerce').fillna(
        0).astype(int)

    # Выборка и расчет калорийности для трех блюд
    df_first_course = df[df['course'] == 'Первые блюда'].sample(n=1)
    first_course_details = df_first_course.to_dict('records')[0]
    df_second_course = df[df['course'] == 'Вторые блюда'].sample(n=1)
    second_course_details = df_second_course.to_dict('records')[0]
    df_third_course = df[df['course'] == 'Третьи блюда'].sample(n=1)
    third_course_details = df_third_course.to_dict('records')[0]

    # Расчет калорийности
    calories_first, basket_first = calculate_recipe_calories_and_products(first_course_details, product_data, 1)
    calories_second, basket_second = calculate_recipe_calories_and_products(second_course_details, product_data, 1)
    calories_third, basket_third = calculate_recipe_calories_and_products(third_course_details, product_data, 1)

    print("Калорийность первого блюда:", round(calories_first, 2))
    print("Продукты для первого блюда:", ", ".join(sorted(basket_first)))
    print("Калорийность второго блюда:", round(calories_second, 2))
    print("Продукты для второго блюда:", ", ".join(sorted(basket_second)))
    print("Калорийность третьего блюда:", round(calories_third, 2))
    print("Продукты для третьего блюда:", ", ".join(sorted(basket_third)))

    result = (
        f"Первое блюдо:"
        f"Калорийность первого блюда: {round(calories_first, 2)}\n"
        f"Продукты для первого блюда: {', '.join(sorted(basket_first))}\n"
        f"Калорийность второго блюда: {round(calories_second, 2)}\n"
        f"Продукты для второго блюда: {', '.join(sorted(basket_second))}\n"
        f"Калорийность третьего блюда: {round(calories_third, 2)}\n"
        f"Продукты для третьего блюда: {', '.join(sorted(basket_third))}"
    )
    product_case = (
        f"Продуктовая корзина: {', '.join(sorted(basket_first))}\n, {', '.join(sorted(basket_second))}\n, {', '.join(sorted(basket_third))}\n"
    )
    return result, product_case