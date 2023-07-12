class Product:
    def __init__(self, json_data):
        self.itemName = json_data.get("item_title", "")
        self.sku = json_data.get("sku", "")
        self.itemPrice = (json_data.get("price_range", {}) or {}).get("minimum_price", {}).get("final_price", {}).get("value", "")
        self.salesSize = json_data.get("sales_size", "")

        nutrition_data = (json_data.get("nutrition") or [{}])[0]
        self.servingSize = nutrition_data.get("serving_size", "")
        self.calPerServing = nutrition_data.get("calories_per_serving", "")
        self.servingsPerContainer = nutrition_data.get("servings_per_container", "")
        self.includes = ""  # Initialize with empty string

        nutrition_details = (nutrition_data.get("details") or [{}])
        nutrition_dict = {item.get('nutritional_item', ''): item for item in nutrition_details}
        self.totalFat = nutrition_dict.get('Total Fat', {}).get('amount', '')
        self.saturatedFat = nutrition_dict.get('Saturated Fat', {}).get('amount', '')
        self.transFat = nutrition_dict.get('Trans Fat', {}).get('amount', '')
        self.cholesterol = nutrition_dict.get('Cholesterol', {}).get('amount', '')
        self.sodium = nutrition_dict.get('Sodium', {}).get('amount', '')
        self.totalCarb = nutrition_dict.get('Total Carbohydrate', {}).get('amount', '')
        self.dietFiber = nutrition_dict.get('Dietary Fiber', {}).get('amount', '')
        self.totalSugars = nutrition_dict.get('Total Sugars', {}).get('amount', '')
        self.protein = nutrition_dict.get('Protein', {}).get('amount', '')
        self.vitaminD = nutrition_dict.get('Vitamin D', {}).get('amount', '')
        self.calcium = nutrition_dict.get('Calcium', {}).get('amount', '')
        self.iron = nutrition_dict.get('Iron', {}).get('amount', '')
        self.potassium = nutrition_dict.get('Potassium', {}).get('amount', '')
        
        # Handling the "Includes"/"Added Sugars" attribute
        self.includes = nutrition_dict.get('Includes', {}).get('amount', '')
        if self.includes == '':  # If "Includes" is not found, try "Added Sugars"
            self.includes = nutrition_dict.get('Added Sugars', {}).get('amount', '')

        self.ingredients = [(ing.get("ingredient", "") or "") for ing in (json_data.get("ingredients") or [])]
        self.allergens = [(allergen.get("ingredient", "") or "") for allergen in (json_data.get("allergens") or [])]

    def to_dict(self):
        return {
            "itemName": self.itemName,
            "sku": self.sku,
            "itemPrice": self.itemPrice,
            "salesSize": self.salesSize,
            "servingSize": self.servingSize,
            "calPerServing": self.calPerServing,
            "servingsPerContainer": self.servingsPerContainer,
            "includes": self.includes,
            "totalFat": self.totalFat,
            "saturatedFat": self.saturatedFat,
            "transFat": self.transFat,
            "cholesterol": self.cholesterol,
            "sodium": self.sodium,
            "totalCarb": self.totalCarb,
            "dietFiber": self.dietFiber,
            "totalSugars": self.totalSugars,
            "protein": self.protein,
            "vitaminD": self.vitaminD,
            "calcium": self.calcium,
            "iron": self.iron,
            "potassium": self.potassium,
            "ingredients": self.ingredients,
            "allergens": self.allergens
        }