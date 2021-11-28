recipes_list = []
ingredients_list = []

n = int(input("How many recipes would you like to enter: "))

def take_recipe():
    name = input("Enter name: ")
    cooking_time = int(input("Enter cooking_time: "))
    ingredients = input("Enter comma separated ingredients: ")
    ingredients = [i.strip() for i in ingredients.split(",")]
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
    }
    return recipe

for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)


def get_difficulty(recipe):
    difficulty = "Unknown"
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        difficulty = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        difficulty = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        difficulty = "Intermediate"
    elif recipe["cooking_time"] > 10 and len(recipe["ingredients"] > 4):
        difficulty = "Intermediate"
    return difficulty

for recipe in recipes_list:
    difficulty = get_difficulty(recipe)
    print("Recipe: ", recipe["name"])
    print("Cooking time: ", recipe["cooking_time"])
    print("Ingredients:")
    for i in recipe["ingredients"]:
        print(i)
    print("Difficulty level: ", difficulty)

    
