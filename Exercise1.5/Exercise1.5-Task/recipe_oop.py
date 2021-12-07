class Recipe(object):
    all_ingredients = []
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = None
        self.difficulty = None

    def calculate_difficulty(self):
        difficulty = "Unknown"
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            difficulty = "Intermediate"
        elif self.cooking_time > 10 and len(self.ingredients) > 4:
            difficulty = "Intermediate"
        return difficulty

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_cooking_time(self):
        return self.name

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    def get_ingredients(self):
        return self.ingredients

    def get_difficulty(self):
        if not self.difficulty:
            self.difficulty = self.calculate_difficulty()
        return self.difficulty

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    def add_ingredients(self, *args):
        for i in args:
            self.ingredients.append(i)
        self.update_all_ingredients()

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)

    def print_recipe(self):
        print("\nRecipe: ", self.get_name())
        print("Ingredients:")
        for i in self.get_ingredients():
            print("- " + i)
        print("Difficulty: ", self.get_difficulty())


    def __str__(self):
        output = str(self.get_name()) + ", " + str(self.get_ingredients()) \
            + ", " + str(self.get_cooking_time()) + ", " + str(self.get_difficulty())
        return output


    @staticmethod
    def recipe_search(data, search_term):
        for recipe in data:
            if (recipe.search_ingredient(search_term)):
                recipe.print_recipe()

tea = Recipe("Tea")
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)
print(tea)

coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)
print(coffee)

cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)
print(cake)

smoothie = Recipe("Banana Smoothie")
smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
smoothie.set_cooking_time(5)
print(smoothie)

recipes_list = [tea, coffee, cake, smoothie]

search_params = ["Water", "sugar", "Bananas"]

for param in search_params:
    Recipe.recipe_search(recipes_list, param)
