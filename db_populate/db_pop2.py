import mysql.connector
import re


def parse_file(file_path):
    data = []
    numRecipeProcessed = 0
    with open(file_path, 'r') as file:
        # Skip the first line
        line = file.readline().strip()

        while line:
            if line == '=======================================':
                numRecipeProcessed = numRecipeProcessed+1
                # print("got here")
                print(numRecipeProcessed)
                # Removing the hyphens from the recipe names
                recipe_name = file.readline().strip().replace('-', ' ')
                # Skip the next line
                file.readline()

                ingredients = []
                line = file.readline().strip()
                while not line.startswith('['):
                    line = file.readline().strip()

                # Getting the first ingredient
                line = line[line.find('[') + 1:]
                ingredients.append(line.split()[-1].strip(',.'))

                line = file.readline().strip()
                while not line.endswith(']'):
                    # go through ingredients only taking valid words
                    while True:
                        # Get the last word in the line
                        last_word = line.split()[-1].strip()

                        if last_word.lower() in ['chopped', 'thawed', 'and', 'drained', 'optional', '(optional)',
                                                 'melted', 'sliced', 'chilled', 'cubed', 'softened', 'peeled', 'beaten', 'lightly', 'zest', 'peel']:
                            # Remove the last word and continue looping
                            line = ' '.join(line.split()[:-1])
                        else:
                            ingredient = last_word
                            break

                    if ingredient:
                        ingredients.append(ingredient)

                    line = file.readline().strip()

                # Getting the last ingredient
                last_ingredient = line.strip('[]').split()[-1].strip(',.')
                if last_ingredient:
                    ingredients.append(last_ingredient)

                data.append((recipe_name, ingredients))

            line = file.readline().strip()

    return data


def insert_data(data):
    # Connect to the MySQL database
    cnx = mysql.connector.connect(
        host='sqlclassdb-instance-1.cqjxl5z5vyvr.us-east-2.rds.amazonaws.com',
        user='anygup26',
        password='JsczDvZdWAzh',
        database='webapp_9MF_anygup26'
    )

    cursor = cnx.cursor()
    numRecipeInserted = 0
    # Insert each recipe and its ingredients into the database
    for recipe in data:
        numRecipeInserted = numRecipeInserted+1
        print(numRecipeInserted)
        recipe_name, ingredients = recipe

        # Check if the recipe already exists
        query = "SELECT recipe_id FROM recipe WHERE recipe_name = %s"
        cursor.execute(query, (recipe_name,))
        result = cursor.fetchone()

        if result:
            recipe_id = result[0]
        else:
            # Insert new recipe into the database
            query = "INSERT INTO recipe (recipe_name) VALUES (%s)"
            cursor.execute(query, (recipe_name,))
            cnx.commit()  # Commit the transaction to generate the auto-incremented recipe_id
            recipe_id = cursor.lastrowid

        # Insert ingredients into the database and create recipe-ingredient records
        for ingredient_name in ingredients:
            # Check if the ingredient already exists
            query = "SELECT ingredient_id FROM ingredient WHERE ingredient_name = %s"
            cursor.execute(query, (ingredient_name,))
            result = cursor.fetchone()

            if result:
                ingredient_id = result[0]
            else:
                # Insert new ingredient into the database
                query = "INSERT INTO ingredient (ingredient_name) VALUES (%s)"
                cursor.execute(query, (ingredient_name,))
                cnx.commit()  # Commit the transaction to generate the auto-incremented ingredient_id
                ingredient_id = cursor.lastrowid

            # Create recipe-ingredient record in the recipe_ingredient_xref table
            query = "INSERT INTO recipe_ingredient_xref (recipe_id, ingredient_id) VALUES (%s, %s)"
            cursor.execute(query, (recipe_id, ingredient_id))

    # Commit the changes and close the connection
    cnx.commit()
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    file_path = 'db_populate/sample_data_actual_file.txt'
    data = parse_file(file_path)
    insert_data(data)
