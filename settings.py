base_url = "http://magnit.ru/catalog/"

id_categories_from_store = [4887, 4893, 4894, 4885, 4851, 4848, 4839, 4844, 17627, 17637,
                            4854, 4841, 38169, 17979, 4868, 38051, 4862, 4869, 4864, 17607,
                            5003, 38915, 38859, 4566, 16533, 4551, 38833, 4537, 4547]

url = 'https://web-gateway.middle-api.magnit.ru/v3/goods'
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://magnit.ru',
    'Referer': 'https://magnit.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'X-App-Version': '0.1.0',
    'X-Client-Name': 'magnit',
    'X-Device-Id': 'iutehj8gi4',
    'X-Device-Platform': 'Web',
    'X-Device-Tag': 'disabled',
    'X-Platform-Version': 'window.navigator.userAgent',
}


def settings_get_source_from_store(number_page):
    return {
        "categoryIDs": id_categories_from_store,
        "includeForAdults": True,
        "onlyDiscount": False,
        "order": "desc",
        "pagination": {"number": number_page, "size": 500},
        "shopType": "6",
        "sortBy": "price",
        "storeCodes": ["992301"],
        "filters": []
    }


source_path = "source/"

recipes_path = source_path + 'recipes.json'
product_data_path = source_path + "product_details.json"
input_file_path_recipes = source_path + 'recipes.xlsx'
output_file_path_recipes = source_path + 'recipes.json'

meat_keywords = [
    "мясо", "свинина", "говядина", "индейка", "цыпленок", "бройлер",
    "утка", "курица", "шашлык", "фарш", "бедро", "голень", "шейка",
    "грудка", "филе", "ребра", "котлеты", "купаты", "колбаски",
    "биточки", "стейк", "поджарка", "мякоть", "субпродукты"
]

