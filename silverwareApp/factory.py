from datetime import datetime
from silverwareApp.vars import products

def get_products():
    return products.copy()

def get_FE_products(products):
    products = get_products()
    for p_id, product in products.items():
        products[p_id] = get_product(p_id)

    return products


def get_product(product_id):
    products = get_products()
    product = products[product_id]
    price, discount = product['price'], product['discount']
    product['final_price'] = price if discount == None else int(price * (1 - discount))
    product['discount_str'] = '' if discount == None else f'-{int(discount * 100)}%'
    product['days_before'] = (datetime.today() - product['created_date']).days
    return product