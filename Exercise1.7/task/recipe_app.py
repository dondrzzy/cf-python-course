from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer, String

engine = create_engine("mysql://cf-python:password@localhost/task_database")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + "-" + self.difficulty + ">"

    def __str__(self):
        # return "Name: \t" + str(self.name) + "\n" + self.name + "-" + self.difficulty + ">"
        return (
            f"ID:\t{self.id}\n"
            f"Name:\t{self.name}\n"
            f"Cooking Time:\t{self.cooking_time}\n"
            f"Difficulty:\t{self.difficulty}\n"
            f"Ingredients:\t{self.ingredients}\n"
        )

    def calculate_difficulty(self):
        difficulty = "Unknown"
        ingredients = self.ingredients.split(',')
        if self.cooking_time < 10 and len(ingredients) < 4:
            difficulty = "Easy"
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            difficulty = "Medium"
        elif self.cooking_time >= 10 and len(ingredients) < 4:
            difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(ingredients) >= 4:
            difficulty = "Hard"
        self.difficulty = difficulty

    def return_ingredients_as_list(self):
        if len(self.ingredients) == 0:
            return []

        return [i.strip() for i in self.ingredients.split(',')]

Base.metadata.create_all(engine)

def create_recipe():
    name = input("Enter name: ")
    if (len(name) > 50):
        print('Error: Value should not exceed 50 characters')
        return create_recipe()
    cooking_time = input("Enter cooking_time: ")
    if cooking_time.isalpha() or not cooking_time.isnumeric():
        print('Error: Cooking time must be an integer')
        return create_recipe()
    cooking_time = int(cooking_time)
    
    ingredients = []
    num_ingredients = int(input("How many ingredients do you want to enter: "))
    for i in range(num_ingredients):
        ingredient = input("Enter ingredient: ").strip()
        ingredients.append(ingredient)

    ingredients = ", ".join(ingredients)
    recipe_entry = Recipe(
        name=name,
        cooking_time=cooking_time,
        ingredients=ingredients,
    )
    recipe_entry.calculate_difficulty()
    session.add(recipe_entry)
    session.commit()

def display_recipes(recipes):
    for recipe in recipes:
        print(str(recipe))

def view_all_recipes():
    recipe_list = session.query(Recipe).all()
    print("recipe_list: ", recipe_list)
    if not recipe_list:
        print("No recipe entries")
        return None

    display_recipes(recipe_list)

def search_by_ingredients():
    if not session.query(Recipe).count():
        print("No recipe entries")
        return None

    results = session.query(Recipe.ingredients).all()
    all_ingredients = []
    for row in results:
        ingredients = row[0]
        ingredients = ingredients.split(",")
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    print("Ingredients:")
    for i, v in enumerate(all_ingredients):
        print(str(i) + ": ", v.strip())
    
    ing_nums = input("Enter numbers corresponding to the ingredient separated by spaces: ")
    ing_nums = ing_nums.split(" ")
    if not ing_nums:
        print("Invalid ingredient entry. Exiting...")
        return None

    search_ingredients = []
    invalid_entry = False
    for num in ing_nums:
        try:
            selected_ingredient = all_ingredients[int(num)]
            search_ingredients.append(selected_ingredient)
        except:
            invalid_entry = True
    if invalid_entry:
        print("Invalid ingredient entry. Exiting...")
        return None

    print("search_ingredients: ", search_ingredients)

    conditions = []
    for i in search_ingredients:
        conditions.append(Recipe.ingredients.like(f"%{i}%"))

    recipes = session.query(Recipe).filter(*conditions).all()

    display_recipes(recipes)

def edit_recipe():
    if not session.query(Recipe).count():
        print("No recipe entries")
        return None
    
    results = session.query(Recipe.id, Recipe.name).all()
    print("Recipes:")
    for result in results:
        print(f"{result[0]}: {result[1]}")
    num = input("Enter number corresponding to the recipe to update: ")
    try:
        num = int(num)
        recipe_to_edit = session.query(Recipe).get(num)
        if not recipe_to_edit:
            raise
    except:
        print('Invalid entry. Exiting...')
        return None

    print("Item to edit")
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Cooking Time: {recipe_to_edit.cooking_time}")
    print(f"3. Ingredients: {recipe_to_edit.ingredients}")

    num = input("Enter number corresponding to the attribute you want to edit: ")
    if num not in ['1', '2', '3']:
        print('Invalid entry. Exiting...')
        return None
    
    if num == '1':
        name = input("Enter updated name: ")
        recipe_to_edit.name = name
    elif num == '2':
        cooking_time = input("Enter updated cooking time: ")
        if not cooking_time.isnumeric():
            print('Invalid entry. Exiting...')
            return None
        recipe_to_edit.cooking_time = int(cooking_time)
    elif num == '3':
        ingredients = input("Enter updated list of comma separated ingredients: ")
        if not ingredients:
            print('Invalid entry. Exiting...')
            return None
        recipe_to_edit.ingredients = ingredients
    recipe_to_edit.calculate_difficulty()
    session.commit()


def delete_recipe():
    if not session.query(Recipe).count():
        print("No recipe entries")
        return None

    results = session.query(Recipe.id, Recipe.name).all()
    print("Recipes:")
    for result in results:
        print(f"{result[0]}: {result[1]}")
    num = input("Enter number corresponding to the recipe to delete: ")
    try:
        num = int(num)
        recipe_to_delete = session.query(Recipe).get(num)
        if not recipe_to_delete:
            raise
    except:
        print('Invalid entry. Exiting...')
        return None

    resp = input("Are you sure. Type 'yes' or 'no': ")
    if resp == 'yes':
        session.delete(recipe_to_delete)
        session.commit()
    else:
        return None


def main_menu():
    choice = '1'

    while(choice != "quit"):
        print("Main Menu")
        print("=========================")
        print("Pick a choice:")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for a recipe by ingredient")
        print("4. Update an existing recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to exit the program.")
        choice = input("Your choice: ")

        if choice == "quit":
            session.close()
            engine.dispose()
        elif choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        else:
            continue

main_menu()
