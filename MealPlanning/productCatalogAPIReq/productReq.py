import requests
from productClass import Product
import json
from tqdm import tqdm

url = "https://www.traderjoes.com/api/graphql"
totalPages = 1
currentPage = 1
responses = []

headers = {
    "Content-Type": "application/json"
}

pbar = None  # Initialize the progress bar variable
while currentPage != totalPages + 1:
    
    data = {
        "operationName":"SearchProducts",
        "variables":{
            "storeCode":"212",
            "availability":"1",
            "published":"1",
            "categoryId":8,
            "currentPage":currentPage,
            "pageSize":15
        },
        "query":"query SearchProducts($categoryId: String, $currentPage: Int, $pageSize: Int, $storeCode: String = \"212\", $availability: String = \"1\", $published: String = \"1\") {\n  products(\n    filter: {store_code: {eq: $storeCode}, published: {eq: $published}, availability: {match: $availability}, category_id: {eq: $categoryId}}\n    currentPage: $currentPage\n    pageSize: $pageSize\n  ) {\n    items {\n      sku\n      item_title\n      category_hierarchy {\n        id\n        name\n        __typename\n      }\n      primary_image\n      primary_image_meta {\n        url\n        metadata\n        __typename\n      }\n      sales_size\n      sales_uom_description\n      price_range {\n        minimum_price {\n          final_price {\n            currency\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      retail_price\n      fun_tags\n      item_characteristics\n      __typename\n    }\n    total_count\n    pageInfo: page_info {\n      currentPage: current_page\n      totalPages: total_pages\n      __typename\n    }\n    aggregations {\n      attribute_code\n      label\n      count\n      options {\n        label\n        value\n        count\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    responses.append(response.text)
    if pbar is None:  # If the progress bar is not created yet
        tp_data = json.loads(response.text)
        totalPages = tp_data["data"]["products"]["pageInfo"]["totalPages"]
        pbar = tqdm(total=totalPages)  # Create the progress bar with the actual total
    else:
        currentPage += 1
        # Update the progress bar
        pbar.update(1)
pbar.close()

sku_dict = {}
# Now, you can process the responses
for response in responses:
    data = json.loads(response)
    items = data["data"]["products"]["items"]
    for item in items:
        key = item["item_title"].lower().replace(' ', '-')
        value = item["sku"]
        sku_dict[key] = value

product_list = []
for key, value in tqdm(sku_dict.items()):
    
    data2 = {
        "operationName": "SearchProduct",
        "variables": {
            "storeCode": "212",
            "published": "1",
            "sku": value
        },
        "query": "query SearchProduct($sku: String, $storeCode: String = \"212\", $published: String = \"1\") {\n  products(\n    filter: {sku: {eq: $sku}, store_code: {eq: $storeCode}, published: {eq: $published}}\n  ) {\n    items {\n      category_hierarchy {\n        id\n        url_key\n        description\n        name\n        position\n        level\n        created_at\n        updated_at\n        product_count\n        __typename\n      }\n      item_story_marketing\n      product_label\n      fun_tags\n      primary_image\n      primary_image_meta {\n        url\n        metadata\n        __typename\n      }\n      other_images\n      other_images_meta {\n        url\n        metadata\n        __typename\n      }\n      context_image\n      context_image_meta {\n        url\n        metadata\n        __typename\n      }\n      published\n      sku\n      url_key\n      name\n      item_description\n      item_title\n      item_characteristics\n      item_story_qil\n      use_and_demo\n      sales_size\n      sales_uom_code\n      sales_uom_description\n      country_of_origin\n      availability\n      new_product\n      promotion\n      price_range {\n        minimum_price {\n          final_price {\n            currency\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      retail_price\n      nutrition {\n        display_sequence\n        panel_id\n        panel_title\n        serving_size\n        calories_per_serving\n        servings_per_container\n        details {\n          display_seq\n          nutritional_item\n          amount\n          percent_dv\n          __typename\n        }\n        __typename\n      }\n      ingredients {\n        display_sequence\n        ingredient\n        __typename\n      }\n      allergens {\n        display_sequence\n        ingredient\n        __typename\n      }\n      created_at\n      first_published_date\n      last_published_date\n      updated_at\n      related_products {\n        sku\n        item_title\n        primary_image\n        primary_image_meta {\n          url\n          metadata\n          __typename\n        }\n        price_range {\n          minimum_price {\n            final_price {\n              currency\n              value\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        retail_price\n        sales_size\n        sales_uom_description\n        category_hierarchy {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    total_count\n    page_info {\n      current_page\n      page_size\n      total_pages\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    prodResponse = requests.post(url, headers=headers, data=json.dumps(data2))
    raw_data = json.loads(prodResponse.text)
    item_data = raw_data["data"]["products"]["items"][0]
    product = Product(item_data)
    product_list.append(product)

product_list_dict = [product.to_dict() for product in product_list]

with open('products.json', 'w') as f:
    json.dump(product_list_dict, f)




