import json

from auth_handler import add_user_auth, get_user_auth, load_auth_data
from flask import Flask, request, jsonify, send_from_directory, render_template

app = Flask(__name__)


name_pers = {}
dish_name = {}
user_data = {}



USER_DATA_FILE = "user_data.json"


def save_user_data_to_file(data):

    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_user_data_from_file():
    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


@app.route('/set_user_data', methods=['POST'])
def set_user_data():

    data = request.get_json()
    required_fields = ["height", "weight", "gender", "age", "name", "activity", "diet"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    user_data = load_user_data_from_file()

    user_data.update({
        "name": data["name"],
        "height": data["height"],
        "weight": data["weight"],
        "gender": data["gender"],
        "age": data["age"],
        "activity": data["activity"],
        "diet": data["diet"]
    })

    user_data["calories"] = calculate_calories_api(user_data)

    save_user_data_to_file(user_data)

    add_user_auth(data["name"], user_data)

    from get_menu_from_calories import (
        get_all_breakfast,
        get_all_lunch,
        get_all_dinner,
        get_total_price_for_all_meals,
        get_combined_grocery_basket
    )

    user_data["meals"] = {
        "breakfast": get_all_breakfast(),
        "lunch": get_all_lunch(),
        "dinner": get_all_dinner(),
    }

    user_data["total_price"] = get_total_price_for_all_meals(
        user_data["meals"]["breakfast"],
        user_data["meals"]["lunch"],
        user_data["meals"]["dinner"]
    )
    user_data["grocery_basket"] = get_combined_grocery_basket(
        user_data["meals"]["breakfast"],
        user_data["meals"]["lunch"],
        user_data["meals"]["dinner"]
    )

    save_user_data_to_file(user_data)

    add_user_auth(data["name"], user_data)

    return jsonify({"message": "User data and meals saved successfully"})


@app.route('/user_data_update', methods=['GET'])
def user_data_update():
    user_data = load_user_data_from_file()
    from get_menu_from_calories import (
        get_all_breakfast,
        get_all_lunch,
        get_all_dinner,
        get_total_price_for_all_meals,
        get_combined_grocery_basket
    )
    # Пересчет данных
    user_data["meals"] = {
        "breakfast": get_all_breakfast(),
        "lunch": get_all_lunch(),
        "dinner": get_all_dinner(),
    }
    user_data["total_price"] = get_total_price_for_all_meals(
        user_data["meals"]["breakfast"],
        user_data["meals"]["lunch"],
        user_data["meals"]["dinner"]
    )
    user_data["grocery_basket"] = get_combined_grocery_basket(
        user_data["meals"]["breakfast"],
        user_data["meals"]["lunch"],
        user_data["meals"]["dinner"]
    )

    save_user_data_to_file(user_data)

    return jsonify({"message": "User data and meals updated successfully"})


@app.route('/get_user_auth', methods=['POST'])
def get_user_auth_route():
    data = request.get_json()

    name = data.get('name')

    if not name:
        return jsonify({"error": "Missing required field: name"}), 400

    from auth_handler import get_user_auth
    return get_user_auth(name)


@app.route('/get_image', methods=['POST'])
def get_image():
    data = request.get_json()

    user_name = data.get('name')
    meal = data.get('meal')

    if not user_name or not meal:
        return jsonify({"error": "Missing required fields: name or meal"}), 400

    auth_data = get_user_auth(user_name)
    if not auth_data:
        return jsonify({"error": "User not found"}), 404

    meals = auth_data.get('meals', {})
    if meal not in meals:
        return jsonify({"error": f"Invalid meal category: {meal}"}), 400

    meal_data = meals[meal]
    image_name = meal_data.get('name_png')
    if not image_name:
        return jsonify({"error": "Image not found for the specified meal"}), 404

    image_folder = 'illustrations'

    try:
        return send_from_directory(image_folder, f"{image_name}.png")
    except FileNotFoundError:
        return jsonify({"error": "Image file not found on the server"}), 404


@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    data = request.get_json()

    name = data.get('name')
    if not name:
        return jsonify({"error": "Missing required field: 'name'"}), 400

    auth_data = get_user_auth(name)
    if not auth_data:
        return jsonify({"error": "User not found"}), 404

    user_info = {
        "name": auth_data.get("name"),
        "height": auth_data.get("height"),
        "weight": auth_data.get("weight"),
        "gender": auth_data.get("gender"),
        "age": auth_data.get("age"),
        "activity": auth_data.get("activity"),
        "diet": auth_data.get("diet"),
        "calories": auth_data.get("calories"),
    }

    return jsonify(user_info), 200

@app.route('/get_user_calories', methods=['POST'])
def get_user_calories():
    data = request.get_json()

    name = data.get('name')

    if not name:
        return jsonify({"error": "Missing required field: name"}), 400

    auth_data = get_user_auth(name)

    if not auth_data:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"calories": auth_data.get('calories')})

@app.route('/get_user_price', methods=['POST'])
def get_user_price():
    data = request.get_json()

    name = data.get('name')

    if not name:
        return jsonify({"error": "Missing required field: name"}), 400

    auth_data = get_user_auth(name)

    if not auth_data:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"total_price": auth_data.get('total_price')})

@app.route('/get_user_breakfast', methods=['POST'])
def get_user_breakfast():
    data = request.get_json()

    name = data.get('name')
    if not name:
        return jsonify({"error": "Missing required field: name"}), 400

    auth_data = get_user_auth(name)
    if not auth_data:
        return jsonify({"error": "User not found"}), 404

    meals = auth_data.get('meals')
    if not meals or 'breakfast' not in meals:
        return jsonify({"error": "Breakfast not found for user"}), 404

    breakfast = meals['breakfast']

    return jsonify({"breakfast": breakfast}), 200

@app.route('/get_user_lunch', methods=['POST'])
def get_user_lunch():
    data = request.get_json()

    name = data.get('name')
    if not name:
        return jsonify({"error": "Missing required field: name"}), 400

    auth_data = get_user_auth(name)
    if not auth_data:
        return jsonify({"error": "User not found"}), 404

    meals = auth_data.get('meals')
    if not meals or 'lunch' not in meals:
        return jsonify({"error": "Breakfast not found for user"}), 404

    lunch = meals['lunch']

    return jsonify({"lunch": lunch}), 200

@app.route('/get_user_dinner', methods=['POST'])
def get_user_dinner():
    data = request.get_json()

    name = data.get('name')
    if not name:
        return jsonify({"error": "Missing required field: name"}), 400

    auth_data = get_user_auth(name)
    if not auth_data:
        return jsonify({"error": "User not found"}), 404

    meals = auth_data.get('meals')
    if not meals or 'lunch' not in meals:
        return jsonify({"error": "Breakfast not found for user"}), 404

    dinner = meals['dinner']

    return jsonify({"dinner": dinner}), 200

@app.route('/get_user_grocery_basket', methods=['POST'])
def get_user_grocery_basket():
    data = request.get_json()

    name = data.get('name')

    if not name:
        return jsonify({"error": "Missing required field: name"}), 400

    auth_data = get_user_auth(name)

    if not auth_data:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"grocery_basket": auth_data.get('grocery_basket')})


@app.route('/get_user_life', methods=['POST'])
def get_user_life():
    data = request.get_json()

    name = data.get('name')
    if not name:
        return jsonify({"error": "Missing required field: 'name'"}), 400

    auth_data = get_user_auth(name)
    if not auth_data:
        return jsonify({"error": "User not found"}), 404

@app.route('/get_first_page', methods=['POST'])
def get_first_page():
    data = request.get_json()
    required_fields = ["name"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    return jsonify

@app.route('/get_user_name', methods=['POST'])
def get_user_name():
    data = request.get_json()

    if "name" not in data:
        return jsonify({"error": "Name field is required"}), 400
    return jsonify({"name": data["name"]})

def load_user_data():
    with open('authorization.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['users']


@app.route('/get_calories', methods=['GET'])
def get_calories():
    if "calories" not in user_data:
        return jsonify({"error": "User data not found"}), 404


    return jsonify({"calories": user_data["calories"]})


@app.route('/set_calories', methods=['POST'])
def set_calories():
    data = request.get_json()
    if "calories" not in data:
        return jsonify({"error": "Calories field is required"}), 400

    user_data["calories"] = data["calories"]
    user_data["diet"] = data.get("diet", "No diet specified")

    return jsonify({"message": "Calories updated successfully"})

@app.route('/check_user_auth', methods=['POST'])
def check_user_auth():
    data = request.get_json()

    name = data.get('name')
    if not name:
        return jsonify({"error": "Missing required field: name"}), 400

    auth_data = get_user_auth(name)

    if not auth_data:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User exists in the system"}), 200



def calculate_calories_api(user_data):
    if user_data["gender"].lower() == 'ж':
        bmr = 88.36 + (13.4 * user_data["weight"]) + (4.8 * user_data["height"]) - (5.7 * user_data["age"])
    else:
        bmr = 447.6 + (9.2 * user_data["weight"]) + (3.1 * user_data["height"]) - (4.3 * user_data["age"])
    if user_data["activity"] == 1:
        tdee = bmr * 1.2
    elif user_data["activity"] == 2:
        tdee = bmr * 1.375
    elif user_data["activity"] == 3:
        tdee = bmr * 1.55
    elif user_data["activity"] == 4:
        tdee = bmr * 1.725
    else:
        tdee = bmr * 1.9
    return round(tdee)

def get_user_data():
    return user_data

if __name__ == '__main__':
    app.run(debug=True)

def get_user_auth(name):
    auth_data = load_auth_data()
    return auth_data.get(name)


