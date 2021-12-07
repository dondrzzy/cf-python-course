import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    password='password')
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20))
''')

def calculate_difficulty(cooking_time, ingredients):
    difficulty = "Unknown"
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = "Hard"
    return difficulty

def display_recipes(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()
    print()
    print("Recipies:")
    print("=========================")
    for row in results:
        print("ID: ", row[0])
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking time: ", row[3])
        print("Difficulty: ", row[4])
        print()

def create_recipe(conn, cursor):
    name = input("Enter name: ")
    cooking_time = int(input("Enter cooking_time: "))
    ingredients = input("Enter ingredients: ")
    ingredients = [i.strip() for i in ingredients.split(",")]
    difficulty = calculate_difficulty(cooking_time, ingredients)

    sql = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s);"
    ingredients = ", ".join(ingredients)
    values = (name, ingredients, cooking_time, difficulty)
    cursor.execute(sql, values)
    display_recipes(conn, cursor)
    conn.commit()

def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
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
    
    ing_input = int(input("Enter a number corresponding to the ingredient: "))

    search_ingredient = all_ingredients[ing_input]

    sql = "SELECT * FROM Recipes WHERE ingredients LIKE '%s'" % (f"%{search_ingredient}%")
    print("search sql: ", sql)
    cursor.execute(sql)
    results = cursor.fetchall()

    for row in results:
        print("ID: ", row[0])
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking time: ", row[3])
        print("Difficulty: ", row[4])
        print()

def update_recipe(conn, cursor):
    display_recipes(conn, cursor)
    id_to_update = int(input("Enter ID of recipe to update: "))
    column_to_update = input("Enter column to update. Options include name, cooking_time, ingredients: ")
    new_value = input("Enter new value: ")

    if column_to_update == 'name':
        new_value = f"'{new_value}'"
    if column_to_update == 'cooking_time':
        new_value = int(new_value)
    if column_to_update == 'ingredients':
        new_value = f"'{new_value}'"

    update_sql = f"UPDATE Recipes SET {column_to_update} = {new_value} WHERE ID = {id_to_update}"
    cursor.execute(update_sql)

    if column_to_update in ["cooking_time", "ingredents"]:
        cursor.execute(f"SELECT cooking_time, ingredients FROM Recipes WHERE ID = {id_to_update}")
        results = cursor.fetchall()
        ingredients = results[0][1].split(", ")
        difficulty = calculate_difficulty(results[0][0], ingredients)

        update_sql = f"UPDATE Recipes SET difficulty = '{difficulty}' WHERE ID = {id_to_update}"
        cursor.execute(update_sql)

    display_recipes(conn, cursor)
    conn.commit()


def delete_recipe(conn, cursor):
    display_recipes(conn, cursor)
    id_to_delete = int(input("Enter ID of recipe to delete: "))
    delete_sql = f"DELETE FROM Recipes WHERE ID = {id_to_delete}"
    cursor.execute(delete_sql)

    display_recipes(conn, cursor)
    conn.commit()

def main_menu(conn, cursor):
    choice = '1'

    while(choice != "quit"):
        print("Main Menu")
        print("=========================")
        print("Pick a choice:")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("Type 'quit' to exit the program.")
        choice = input("Your choice: ")

        if choice == "quit":
            conn.commit()
            conn.close
        elif choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)

main_menu(conn, cursor)
