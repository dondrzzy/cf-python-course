import pickle

recipes_list = []
ingredients_list = []

def calc_difficulty(recipe):
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
    recipe["difficulty"] = calc_difficulty(recipe)
    return recipe

filename = input("Enter the filename where you've stored your recipes: ")
try:
    file = open(filename, 'rb')
    # data is a dict with recipes_list and all_ingredients
    data = pickle.load(file)
except FileNotFoundError:
    print("File doesn't exist - exiting.")
    data = {
        "recipes_list": recipes_list,
        "all_ingredients": ingredients_list
    }
except:
    print("An unexpected error occurred.")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
else:
    file.close()
finally:
    recipes_list = recipes_list
    ingredients_list = ingredients_list

n = int(input("How many recipes would you like to enter: "))

for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

print("recipes_list: ", recipes_list)
print("ingredients_list: ", ingredients_list)

data = {
    "recipes_list": recipes_list,
    "all_ingredients": ingredients_list
}

with open(filename, "wb") as my_file:
    pickle.dump(data, my_file)
