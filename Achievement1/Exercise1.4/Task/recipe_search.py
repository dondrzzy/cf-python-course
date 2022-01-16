import pickle

def display_recipe(recipe):
    print(recipe["name"]+ " Recipe details")
    print("Name: " + recipe["name"])
    print("Ingredients:")
    for i in recipe["ingredients"]:
        print("- ", i)
    print("Difficulty: ", recipe["difficulty"])


def search_ingredient(data):
    print("Available ingredients:")
    for i, ingredient in enumerate(data["all_ingredients"]):
        print(str(i) + ": " + ingredient)
    
    try:
        a = int(input("Enter a number corresponding to an ingredient: "))
        ingredient_searched = data["all_ingredients"][a]
    except IndexError:
        print("Invalid input selected.")
        return None
    except:
        print("Invalid input selected.")
        return None
    else:
        recipes_list = data["recipes_list"]
        for recipe in recipes_list:
            if ingredient_searched in recipe["ingredients"]:
                print("Recipe: ", recipe["name"])
    finally:
        print("Function complete!")

filename = input("Enter the filename where you've stored your recipes: ")
try:
    my_file = open(filename, 'rb')
    data = pickle.load(my_file)
except FileNotFoundError:
    print("File doesn't exist - exiting.")
except:
    print("An unexpected error occurred.")
else:
    search_ingredient(data)
finally:
    print("Goodbye!")

