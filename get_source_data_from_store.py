import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from settings import url, headers, base_url, settings_get_source_from_store, product_data_path


def get_products_from_store():
    all_products = []
    page_number = 1
    while True:
        response = requests.post(url, headers=headers, json=settings_get_source_from_store(page_number))
        if response.ok:
            data = response.json()
            products = data.get('goods', [])
            if not products:
                break
            all_products.extend(products)
            page_number += 1
        else:
            print(f'End on page {page_number}: {response.text}')
            break


    return all_products


def formating_products(products):
    products_by_category = {}
    total_products = 0

    for product in products:

        for category in product['categories']:
            if category not in products_by_category:
                products_by_category[category] = []

            products_by_category[category].append(product['id'])
            total_products += 1

    print(f"Total products: {total_products}")

    return products_by_category


def get_detail_product_info(products_by_category, base_url, headers):
    all_product_details = []  #

    total_products = sum(len(ids) for ids in products_by_category.values())

    with tqdm(total=total_products, desc="Обрабатываем продукты") as pbar:
        for category, product_ids in products_by_category.items():
            for product_id in product_ids:
                product_url = f"{base_url}{product_id}/"
                response = requests.get(product_url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    product_title_div = soup.find('div', class_='product-details__title')
                    product_title = product_title_div.text.strip() if product_title_div else 'Название не найдено'

                    calories_div = soup.find('div', class_='kbju__item')
                    calories_count = calories_div.find('div',
                                                       class_='kbju__item-count').text.strip() if calories_div else '0'
                    calories_text = calories_div.find('div',
                                                      class_='kbju__item-text').text.strip() if calories_div else 'ккал'
                    calories = f"{calories_count} {calories_text}"

                    price_span = soup.find('div', class_='product-details__price')
                    price = price_span.text.strip() if price_span else 'Цена не указана'

                    product_data = {
                        'ID': product_id,
                        'Название продукта': product_title,
                        'Цена': price,
                        'Калорийность': calories
                    }

                    all_product_details.append(product_data)
                else:
                    print(f"Ошибка загрузки страницы {product_url}: статус {response.status_code}")

                pbar.update(1)

    with open(product_data_path, 'w', encoding='utf-8') as f:
        json.dump(all_product_details, f, ensure_ascii=False, indent=4)

    return all_product_details


def get_source_data_from_store():
    products = get_products_from_store()
    clean_data_products = formating_products(products)
    get_detail_product_info(clean_data_products, base_url, headers)
