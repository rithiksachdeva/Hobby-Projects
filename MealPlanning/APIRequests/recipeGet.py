import requests
from recipeClass import Recipe
import json
from tqdm import tqdm

url = "https://www.traderjoes.com/home/recipes.model.json"

response = requests.get(url)

data = response.json()

recipes = data[":items"]["root"][":items"]["body"][":items"]["section"][":items"]["recipes-grid"]["recipes"]["recipes"]

recipe_list = []

for recipe in recipes:
    title = recipe['title']
    page_link = recipe['pageLink']
    categories = recipe['categories']

    recipe_list.append({
        "title": title,
        "pageLink": page_link,
        "categories": categories
    })

base_url = "https://www.traderjoes.com"

recipe_objects = []

for recipe in tqdm(recipe_list, desc="Fetching recipes"):
    page_link = recipe['pageLink']

    recipe_url = f"{base_url}{page_link}.model.json"

    recipe_response = requests.get(recipe_url)

    if recipe_response.status_code == 200:
        recipe_data = recipe_response.json()

        recipe_object = Recipe(recipe_data, page_link, recipe['categories'])

        recipe_objects.append(recipe_object)
    else:
        print(f"Failed to get the details for the recipe: {recipe['title']}")

recipe_list_dict = [recipe.to_dict() for recipe in recipe_objects]

with open('recipes.json', 'w') as f:
    json.dump(recipe_list_dict, f)
