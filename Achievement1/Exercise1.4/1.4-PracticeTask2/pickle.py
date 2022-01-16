import pickle
recipe = {"name": "Tea", "ingredients": ["Tea Leaves", "Water", "Sugar"], "cooking_time": 5, "difficulty": "Easy"}
with open("recipe_binary.bin", "wb") as my_file:
    pickle.dump(recipe, my_file)

print(recipe["name"]+ " Recipe details")
print("Name: " + recipe["name"])
print("Ingredients:")
for i in recipe["ingredients"]:
     print("- ", i)
print("Difficulty: ", recipe["difficulty"])


