class Recipe:
    def __init__(self, json_data, pagelink, categories):
        self.recipeName = json_data.get("title")
        self.servesMin = json_data.get(":items", {}).get("root", {}).get(":items", {}).get("body", {}).get(":items", {}).get("top_section", {}).get(":items", {}).get("recipe_details", {}).get("servesMin")
        self.servesMax = json_data.get(":items", {}).get("root", {}).get(":items", {}).get("body", {}).get(":items", {}).get("top_section", {}).get(":items", {}).get("recipe_details", {}).get("servesMax")
        self.hoursToCook = json_data.get(":items", {}).get("root", {}).get(":items", {}).get("body", {}).get(":items", {}).get("top_section", {}).get(":items", {}).get("recipe_details", {}).get("hoursToCook")
        self.minutesToCook = json_data.get(":items", {}).get("root", {}).get(":items", {}).get("body", {}).get(":items", {}).get("top_section", {}).get(":items", {}).get("recipe_details", {}).get("minutesToCook")

        ingredients = json_data.get(":items", {}).get("root", {}).get(":items", {}).get("body", {}).get(":items", {}).get("section", {}).get(":items", {}).get("recipe_info", {}).get(":items", {}).get("recipe_ingredients", {}).get("ingredients")
        self.ingredients = ingredients if ingredients is not None else []

        steps = json_data.get(":items", {}).get("root", {}).get(":items", {}).get("body", {}).get(":items", {}).get("section", {}).get(":items", {}).get("recipe_info", {}).get(":items", {}).get("recipe_directions", {}).get("steps", [{}])
        self.recipeDirections = [step.get("description") for step in steps if step.get("description") is not None]

        self.pageLink = pagelink
        self.categories = categories

    def to_dict(self):
        return {
            "recipeName": self.recipeName,
            "servesMin": self.servesMin,
            "servesMax": self.servesMax,
            "hoursToCook": self.hoursToCook,
            "minutesToCook": self.minutesToCook,
            "ingredients": self.ingredients,
            "recipeDirections": self.recipeDirections,
            "pageLink": self.pageLink,
            "categories": self.categories
        }
