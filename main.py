from get_calories_from_rezept_and_product import calculate_calories
from user_input import get_user_data, get_user_menu

if __name__ == "__main__":
    user_data_dict = get_user_data()
    calories_needed = calculate_calories(user_data_dict['height_cm'], user_data_dict['weight_kg'], user_data_dict['sex'], user_data_dict['age'])
    get_user_menu(calories_needed)

