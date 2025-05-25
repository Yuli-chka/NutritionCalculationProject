import json
import random
import requests
import api
from settings import meat_keywords

USER_DATA_FILE = "user_data.json"

def load_user_data_from_file():
    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_user_data_api():
    load_user_data_from_file()
    return load_user_data_from_file()

user_data_api = get_user_data_api()
### Если возврат 0, нет диет, если возврат 1 вегетарианцы

def type_diet():
    user_data = get_user_data_api()
    return user_data.get("diet", "0")  # Возвращает "0" по умолчанию


def get_dich_name(cours_wan):
    with open('recipes.json', encoding='utf-8') as recipes_object:
        data = json.load(recipes_object)
    filtered_recipes = [recipe for recipe in data if recipe['course'] == cours_wan]

    current_diet = type_diet()
    if current_diet == "1":  # Для вегетарианцев
        while True:
            random_recipe = random.choice(filtered_recipes)
            if not any(keyword in random_recipe["ingredients"].lower() for keyword in meat_keywords):
                return random_recipe['dish']
    else:
        random_recipe = random.choice(filtered_recipes)
        return random_recipe['dish']


breakfast = get_dich_name("Первые блюда")
lunch = get_dich_name("Вторые блюда")
dinner = get_dich_name("Третьи блюда")

def get_recipet(cours: object) -> object:
    with open('recipes.json', encoding='utf-8') as recipes_object:
        data = json.loads(recipes_object.read())
    filtered_recipes = [recipe for recipe in data if recipe['dish'] == cours]
    recipe = filtered_recipes[0]
    ingredients_list = [ingredient.strip() for ingredient in recipe['ingredients'].split(',')]
    return ingredients_list


def get_name(cours):
    with open('recipes.json', encoding='utf-8') as recipes_object:
        data = json.loads(recipes_object.read())
    filtered_recipes = [recipe for recipe in data if recipe['dish'] == cours]
    recipe = filtered_recipes[0]
    return recipe['dish']


#Нужно сделать нахождение для каждого продукта


def comparison_product_and_recipe(cours):
    with open('product_details.json', encoding='utf-8') as product_object:
        products = json.load(product_object)

    ingredients = get_recipet(cours)
    result = []
    for variable in ingredients:
        recipe_words = variable.split()
        ingredient = recipe_words[0].lower()
        matching_products = [
            product for product in products
            if ingredient in product.get("name", "").lower()
        ]

        chosen_product = random.choice(matching_products) if matching_products else None
        result.append({
            "recipe_item": variable,
            "matched_product": chosen_product
        })
    return result



structure_breakfast = comparison_product_and_recipe(breakfast)
structure_dinner = comparison_product_and_recipe(dinner)
structure_lunch = comparison_product_and_recipe(lunch)


### Вставляем structure_***
def counting_calories(order):
    results = []
    for item in order:
        recipe_item = item['recipe_item']
        matched_product = item['matched_product']

        if matched_product:

            calories = float(matched_product['calories'].split()[0])

            if recipe_item[-1].isdigit():
                quantity = int(recipe_item.split()[-1])
                result_calories = (quantity / 100) * calories
            elif recipe_item.endswith("шт"):
                quantity = int(recipe_item.split()[-2])
                result_calories = (calories / 2) * quantity
            else:
                result_calories = 0
        else:
            result_calories = 0

        results.append({
            "recipe_item": recipe_item,
            "matched_product": matched_product,
            "calculated_calories": result_calories
        })

    return results


def calculate_total_calories(dish):
    if not isinstance(dish, list):
        raise ValueError("Dish should be a list of dictionaries.")


    if not all(isinstance(item, dict) for item in dish):
        raise ValueError("Each item in the dish list should be a dictionary.")

    total_calories = sum(
        item.get('calculated_calories', 0)
        for item in dish
        if 'calculated_calories' in item
    )
    return round(total_calories)

#Просчитанные продукты с калориями
calories_breakfast = counting_calories(structure_breakfast)
calories_lunch = counting_calories(structure_lunch)
calories_dinner = counting_calories(structure_dinner)

#калории блюд
breakfast_calories = calculate_total_calories(calories_breakfast)
lunch_calories = calculate_total_calories(calories_lunch)
dinner_calories = calculate_total_calories(calories_dinner)



def calculate_uniform_calorie_coefficient(target_calories, total_current_calories):
    if total_current_calories == 0:
        return 1
    return target_calories / total_current_calories


target_calories = get_user_data_api().get('calories', 0)
total_current_calories = breakfast_calories + lunch_calories + dinner_calories
uniform_coefficient = calculate_uniform_calorie_coefficient(target_calories, total_current_calories)



def adjust_calories_with_coefficient(order, coefficient):
    adjusted_results = []

    for item in order:
        recipe_item = item['recipe_item']
        matched_product = item['matched_product']
        calculated_calories = item['calculated_calories']

        if matched_product:
            adjusted_calories = round(calculated_calories * coefficient)

            recipe_words = recipe_item.split()
            if len(recipe_words) > 1 and recipe_words[-1].isdigit():
                quantity = int(recipe_words[-1])
                new_quantity = round(quantity * coefficient)
                adjusted_recipe_item = ' '.join(recipe_words[:-1]) + f" {new_quantity}"
            else:
                adjusted_recipe_item = recipe_item

            adjusted_results.append({
                "recipe_item": adjusted_recipe_item
            })

    return adjusted_results



adjusted_breakfast = adjust_calories_with_coefficient(calories_breakfast, uniform_coefficient)
adjusted_lunch = adjust_calories_with_coefficient(calories_lunch, uniform_coefficient)
adjusted_dinner = adjust_calories_with_coefficient(calories_dinner, uniform_coefficient)

def parse_price(price_str):
    price_str = price_str.replace('₽', '').replace(',', '.').strip()
    try:
        return float(price_str)
    except ValueError:

        return 0

def get_full_recipe(cours: str) -> str:
    with open('recipes.json', encoding='utf-8') as recipes_object:
        data = json.loads(recipes_object.read())
    filtered_recipes = [recipe for recipe in data if recipe['dish'] == cours]
    recipe = filtered_recipes[0]
    return recipe['recipe']

def get_short_recipe_description(cours: str) -> str:
    with open('recipes.json', encoding='utf-8') as recipes_object:
        data = json.loads(recipes_object.read())
    filtered_recipes = [recipe for recipe in data if recipe['dish'] == cours]
    recipe = filtered_recipes[0]
    return recipe['description']

recipe_breakfast = get_full_recipe(breakfast)
recipe_lunch = get_full_recipe(lunch)
recipe_dinner = get_full_recipe(dinner)

short_recipe_breakfast = get_short_recipe_description(breakfast)
short_recipe_lunch = get_short_recipe_description(lunch)
short_recipe_dinner = get_short_recipe_description(dinner)

def png_illustration(cours):
    with open('recipes.json', encoding='utf-8') as recipes_object:
        data = json.loads(recipes_object.read())
    filtered_recipes = [recipe for recipe in data if recipe['dish'] == cours]
    recipe = filtered_recipes[0]
    return recipe['png']

png_breakfast = png_illustration(breakfast)
png_lunch = png_illustration(lunch)
png_dinner = png_illustration(dinner)

print(uniform_coefficient)

def get_all(cours):
    # Загружаем данные пользователя
    user_data = get_user_data_api()
    target_calories = user_data.get("calories", 0)

    # Генерируем данные для блюда
    dich_name = get_dich_name(cours)
    structure = comparison_product_and_recipe(dich_name)
    calories_data = counting_calories(structure)
    total_calories = calculate_total_calories(calories_data)

    # Рассчитываем коэффициент калорийности на основе общих калорий всех блюд
    total_current_calories = breakfast_calories + lunch_calories + dinner_calories
    coefficient = calculate_uniform_calorie_coefficient(target_calories, total_current_calories)

    # Корректируем данные с учетом коэффициента
    adjusted_data = adjust_calories_with_coefficient(calories_data, coefficient)

    # Собираем результат
    recipe = get_full_recipe(dich_name)
    short_description = get_short_recipe_description(dich_name)
    image_name = png_illustration(dich_name)
    total_price = sum(parse_price(item["matched_product"].get("price", "0")) for item in structure if item["matched_product"])

    return {
        "name": [dich_name],
        "grocery_basket": [item['recipe_item'] for item in adjusted_data],
        "structure": [item["matched_product"]["name"] for item in structure if item["matched_product"]],
        "calories": round(total_calories * coefficient),  # Умножаем на локально рассчитанный коэффициент
        "total_price": round(total_price, 2),
        "recipe": recipe,
        "short": short_description,
        "name_png": image_name,
    }



def get_all_breakfast():
    return get_all("Первые блюда")

def get_all_lunch():
    return get_all("Вторые блюда")

def get_all_dinner():
    return get_all("Третьи блюда")

def get_total_price_for_all_meals(breakfast_data, lunch_data, dinner_data):
    return round(breakfast_data["total_price"] + lunch_data["total_price"] + dinner_data["total_price"], 2)

def combine_grocery_basket(grocery_basket):
    combined_basket = {}

    for item in grocery_basket:
        parts = item.split()
        if len(parts) > 1 and parts[-1].isdigit():
            product_name = " ".join(parts[:-1]).strip()
            quantity = int(parts[-1])
        elif len(parts) > 1 and parts[-1] in ["г", "шт"]:
            product_name = " ".join(parts[:-2]).strip()
            quantity = int(parts[-2])
        else:
            product_name = item.strip()
            quantity = 1

        if product_name in combined_basket:
            combined_basket[product_name] += quantity
        else:
            combined_basket[product_name] = quantity

    result = [f"{product_name}" for product_name, quantity in combined_basket.items()]
    return result


def get_combined_grocery_basket(breakfast_data, lunch_data, dinner_data):
    raw_basket = breakfast_data["structure"] + lunch_data["structure"] + dinner_data["structure"]
    return combine_grocery_basket(raw_basket)

total_price_all_meals = get_total_price_for_all_meals(
    get_all_breakfast(),
    get_all_lunch(),
    get_all_dinner()
)

combined_grocery_basket = get_combined_grocery_basket(
    get_all_breakfast(),
    get_all_lunch(),
    get_all_dinner()
)


print(get_all_breakfast())
print(get_all_lunch())
print(get_all_dinner())
