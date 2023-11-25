"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, abort, session, url_for
from datetime import datetime

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

app.secret_key = 'J6v6QwEB6fpG' # Random password; required to set secret key to use session

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@34.75.94.195/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@34.75.94.195/proj1part2"
#     New server: 34.74.171.121
#
DATABASEURI = "postgresql://jl6509:6509@34.74.171.121/proj1part2"

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
conn = engine.connect()

# The string needs to be wrapped around text()

conn.execute(text("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);"""))
conn.execute(text("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');"""))

# To make the queries run, we need to add this commit line

conn.commit() 

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


# Get all users with their id and displayname for displaying a dropdown menu for user selection
def all_users():
  with engine.connect() as connection:
    cursor = connection.execute(text("""SELECT UserID, DisplayName FROM People"""))
    results = cursor.mappings().all()
    users = {}
    for result in results:
      userid = result["userid"]
      users[userid] = result["displayname"]
    cursor.close()

  return users

# A global variable that stores the dictionary of all users
users = all_users()

# Pass the users dictionary to all templates
@app.context_processor
def inject_user():
  return {"users": users}

# Set user for current session based on the user_id selected from the dropdown menu
@app.route('/set_user', methods=['POST'])
def set_user():
  user_id = request.form.get('user_id')
  if user_id:
    session['user_id'] = int(user_id)
  else:
    session.pop('user_id', None)  # Remove the user_id from the session if no user is selected
  # After setting the user, redirect to the previous page if it exists or else, the main page
  return redirect(request.referrer or '/')

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: https://flask.palletsprojects.com/en/2.0.x/quickstart/?highlight=routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/2.0.x/api/?highlight=incoming%20request%20data

  """

  """
  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  #
  # example of a database query 
  #
  cursor = g.conn.execute(text("SELECT name FROM test"))
  g.conn.commit()

  # 2 ways to get results

  # Indexing result by column number
  names = []
  for result in cursor:
    names.append(result[0])  

  # Indexing result by column name
  names = []
  results = cursor.mappings().all()
  for result in results:
    names.append(result["name"])
  cursor.close()
  """

  # Query to get all categories
  cursor = g.conn.execute(text("""SELECT CategoryID, CategoryName FROM Categories"""))
  g.conn.commit()
  all_categories = [] # a list of tuples
  results = cursor.mappings().all()
  for result in results:
    all_categories.append((result["categoryid"], result["categoryname"]))
  cursor.close()

  # Query to get top 5 recipes with the highest aggregated rating
  # (if there is a tie, then choose based on lower RecipeID)
  cursor = g.conn.execute(text("""SELECT R.RecipeName, P.DisplayName, R.AggregatedRating, R.RecipeID
                               FROM Recipes_written_by R, Authors A, People P
                               WHERE R.UserID = A.UserID AND A.UserID = P.UserID
                               ORDER BY R.AggregatedRating DESC, R.RecipeID ASC
                               LIMIT 5"""))
  g.conn.commit()
  top_5_recipes = [] # a list of tuples
  results = cursor.mappings().all()
  for result in results:
    top_5_recipes.append((result["recipename"], result["displayname"], result["aggregatedrating"], result["recipeid"]))
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #
  #     # creates a <div> tag for each element in data
  #     # will print:
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  # context = dict(data = names)

  context = dict(categories=all_categories, recipes=top_5_recipes)

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#

# Helper function to convert time into ~ hr ~ min format
def convert_time(time):
  hours = int(time // 60)
  mins = int(time % 60)
  if hours > 0:
    formatted_time = f"{hours} hr {mins} min"
  else:
    formatted_time = f"{mins} min"

  return formatted_time


# A page for each category showing a list of all recipes in the category
@app.route('/category/<int:category_id>')
def category(category_id):
  params_dict = {"categoryid": category_id}
  # Get all the recipes that belong to the given category_id
  cursor = g.conn.execute(text("""
                               SELECT R.RecipeName, P.DisplayName, R.TotalTime, R.AggregatedRating, R.Calories, R.Sugar, R.RecipeID
                               FROM Recipes_written_by R, Categories C, belongs_to B, Authors A, People P
                               WHERE R.RecipeID = B.RecipeID AND B.CategoryID = C.CategoryID
                               AND R.UserID = A.UserID AND A.UserID = P.UserID
                               AND C.CategoryID = :categoryid
                               """), params_dict)
  g.conn.commit()
  recipes_in_category = [] # a list of tuples 
  results = cursor.mappings().all()
  for result in results:
    formatted_time = convert_time(result["totaltime"])
    recipes_in_category.append((result["recipename"], result["displayname"], formatted_time, result["aggregatedrating"], result["calories"], result["sugar"], result["recipeid"]))
  cursor.close()

  # Get the name of the category with the given category_id
  # Need to run this query separately because some categories do not have any recipes in it, thus not showing up in belongs_to
  cursor = g.conn.execute(text("""SELECT C.CategoryName FROM Categories C WHERE C.CategoryID = :categoryid"""), params_dict)
  g.conn.commit()
  category_name = ""
  for result in cursor:
    category_name = result[0]
  cursor.close()

  context = dict(id=category_id, name=category_name, recipes=recipes_in_category)
  return render_template("category_recipes.html", **context)


# A page that shows a list of all recipes
@app.route('/recipes')
def recipes():
  # Get all recipes from the database
  # If a recipe belongs to more than one category, the resulting table will contain more than one row for that recipe
  cursor = g.conn.execute(text("""
                               SELECT R.RecipeID, R.RecipeName, P.DisplayName, C.CategoryName, R.TotalTime, R.AggregatedRating, R.Calories, R.Sugar, C.CategoryID
                               FROM Recipes_written_by R, Categories C, belongs_to B, Authors A, People P
                               WHERE R.RecipeID = B.RecipeID AND B.CategoryID = C.CategoryID
                               AND R.UserID = A.UserID AND A.UserID = P.UserID
                               """))
  g.conn.commit()
  results = cursor.mappings().all()

  # Process the result so that we (intuitionally) have only one row for one recipe (handle multiple categories)
  all_recipes = {} # This is going to be a nested dictionary
  for result in results:
    recipe_id = result["recipeid"]
    if recipe_id not in all_recipes: # If it is the first row for a recipe
      # First, convert total time into ~ hr ~ min
      formatted_time = convert_time(result["totaltime"])

      all_recipes[recipe_id] = {
        "recipename": result["recipename"],
        "displayname": result["displayname"],
        "categories": [(result["categoryname"], result["categoryid"])],
        "totaltime": formatted_time, 
        "aggregatedrating": result["aggregatedrating"], 
        "calories": result["calories"], 
        "sugar": result["sugar"]
        }
    else: # if recipe_id is already in all_recipes (i.e., if recipe belongs to more than one category)
      all_recipes[recipe_id]["categories"].append((result["categoryname"], result["categoryid"]))
  
  cursor.close()
  
  context = {"recipes": all_recipes}
  return render_template("all_recipes.html", **context)


# Recipe Insights (View all details of a recipe, reviews, and required ingredients)
@app.route('/recipe/<int:recipe_id>')
def recipe_insights(recipe_id):
  params_dict = {"recipeid": recipe_id}
  # Get all details of the recipe, categories that it belongs to, and the author's name
  # If a recipe belongs to more than one category, the resulting table will contain more than one row for that recipe
  cursor = g.conn.execute(text("""
                               SELECT R.*, P.DisplayName, C.CategoryName, C.CategoryID
                               FROM Recipes_written_by R, Categories C, belongs_to B, Authors A, People P
                               WHERE R.RecipeID = B.RecipeID AND B.CategoryID = C.CategoryID
                               AND R.UserID = A.UserID AND A.UserID = P.UserID
                               AND R.RecipeID = :recipeid
                               """), params_dict)
  g.conn.commit()
  results = cursor.mappings().all()

  recipe_details = {}
  for result in results:
    if not recipe_details: # If this is the first row for this recipe
      # First, convert all time into ~ hr ~ min
      formatted_cooktime = convert_time(result["cooktime"])
      formatted_preptime = convert_time(result["preptime"])
      formatted_totaltime = convert_time(result["totaltime"])

      recipe_details = {
        "recipeid": result["recipeid"],
        "recipename": result["recipename"],
        "cooktime": formatted_cooktime,
        "preptime": formatted_preptime,
        "totaltime": formatted_totaltime, 
        "description": result["description"],
        "instructions": result["instructions"],
        "aggregatedrating": result["aggregatedrating"], 
        "reviewcount": result["reviewcount"],
        "servings": result["servings"],
        "calories": result["calories"], 
        "sugar": result["sugar"],
        "datepublished": result["datepublished"],
        "author": result["displayname"],
        "categories": [(result["categoryname"], result["categoryid"])]
        }
    else: # if not the first row (i.e., if recipe belongs to more than one category)
      recipe_details["categories"].append((result["categoryname"], result["categoryid"]))
  
  cursor.close()

  # Get all reviews of the recipe with all details of each review and the user's name
  cursor = g.conn.execute(text("""
                               SELECT V.*, P.DisplayName
                               FROM Recipes_written_by R, Reviews_created_by_evaluates V, Users U, People P
                               WHERE R.RecipeID = V.RecipeID
                               AND V.UserID = U.UserID AND U.UserID = P.UserID
                               AND R.RecipeID = :recipeid
                               ORDER BY V.DateSubmitted ASC
                               """), params_dict)
  g.conn.commit()
  results = cursor.mappings().all()

  all_reviews = {}
  for result in results: # each row/result corresponds to one review for the recipe
    reviewnumber = result["reviewnumber"]
    if reviewnumber not in all_reviews:
      all_reviews[reviewnumber] = {
        "rating": result["rating"],
        "content": result["content"],
        "datesubmitted": result["datesubmitted"],
        "datemodified": result["datemodified"],
        "author": result["displayname"],
        "userid": result["userid"]
      }

  cursor.close()

  # Get all required ingredients for the recipe
  cursor = g.conn.execute(text("""
                               SELECT I.IngredientID, I.IngredientName, U.ItemAmount
                               FROM Recipes_written_by R, uses U, Ingredients I
                               WHERE R.RecipeID = U.RecipeID
                               AND U.IngredientID = I.IngredientID
                               AND R.RecipeID = :recipeid
                               """), params_dict)
  g.conn.commit()
  results = cursor.mappings().all()

  all_ingredients = {}
  for result in results: # each row/result corresponds to one ingredient for the recipe
    ingredientid = result["ingredientid"]
    if ingredientid not in all_ingredients:
      # Nested query to check if there are Whole Foods products associated with this ingredient
      # If so, link the ingredient page to the ingredient name; If not, do not link
      params_dict2 = {"ingredientid": ingredientid}
      cursor2 = g.conn.execute(text("""
                                   SELECT COUNT(*)
                                   FROM WholeFoodsProducts_linked_to W
                                   WHERE W.IngredientID = :ingredientid
                                   """), params_dict2)
      g.conn.commit()
      has_whole_foods = False # True if there are associated Whole Foods products
      for result2 in cursor2:
        if result2[0] > 0: has_whole_foods = True
      cursor2.close()

      all_ingredients[ingredientid] = {
        "ingredientname": result["ingredientname"],
        "itemamount": result["itemamount"],
        "wholefoods": has_whole_foods
      }

  cursor.close()

  context = {"recipe": recipe_details, "reviews": all_reviews, "ingredients": all_ingredients}
  return render_template("recipe_insights.html", **context)


# If ingredient available at Whole Foods, show products info
@app.route('/ingredient/<int:ingredient_id>')
def ingredient(ingredient_id):
  params_dict = {"ingredientid": ingredient_id}

  cursor = g.conn.execute(text("""
                                SELECT *
                                FROM WholeFoodsProducts_linked_to W, Ingredients I
                                WHERE W.IngredientID = I.IngredientID
                                AND W.IngredientID = :ingredientid
                                """), params_dict)
  g.conn.commit()
  results = cursor.mappings().all()

  all_products = {}
  ingredient_name = ""
  for result in results: # each row/result corresponds to one WholeFoods product for the ingredient
    ingredient_name = result["ingredientname"]
    productid = result["productid"]
    all_products[productid] = {
      "companyname": result["companyname"],
      "productname": result["productname"],
      "regularprice": result["regularprice"],
      "saleprice": result["saleprice"],
      "primeprice": result["primeprice"],
      "link": result["link"]
    }

  cursor.close()

  context = {"ingredientname": ingredient_name, "products": all_products}
  return render_template("ingredient.html", **context)


# Allow users to search by recipe name or author's name
@app.route('/search_results')
def search_results():
    search_type = request.args.get('search_type')
    query = request.args.get('query')

    if not query:
        return "Please enter a search term.", 400

    if search_type == 'name':
        # Search for recipe name, doesn't have to type in exact name and case-insensitive
        # e.g. if search for "carrot", result will contain recipes that have "carrot" in their name
        search_term = f"%{query}%"
        sql_query = text("""
                         SELECT *
                         FROM Recipes_written_by R, Categories C, belongs_to B, Authors A, People P
                         WHERE R.RecipeName ILIKE :searchterm
                         AND R.RecipeID = B.RecipeID AND B.CategoryID = C.CategoryID
                         AND R.UserID = A.UserID AND A.UserID = P.UserID
                         """)
    elif search_type == 'author':
        # Search for author's name, doesn't have to type in exact name and case-insensitive
        search_term = f"%{query}%"
        sql_query = text("""
                         SELECT *
                         FROM Recipes_written_by R, Categories C, belongs_to B, Authors A, People P
                         WHERE P.DisplayName ILIKE :searchterm
                         AND P.UserID = A.UserID AND A.UserID = R.UserID
                         AND R.RecipeID = B.RecipeID AND B.CategoryID = C.CategoryID
                         """)

    cursor = g.conn.execute(sql_query, {"searchterm": search_term})
    results = cursor.mappings().all()

    query_results = {}
    for result in results:
      recipe_id = result["recipeid"]
      if recipe_id not in query_results: # If it is the first row for a recipe
        # First, convert total time into ~ hr ~ min
        formatted_time = convert_time(result["totaltime"])

        query_results[recipe_id] = {
          "recipename": result["recipename"],
          "displayname": result["displayname"],
          "categories": [(result["categoryname"], result["categoryid"])],
          "totaltime": formatted_time, 
          "aggregatedrating": result["aggregatedrating"], 
          "calories": result["calories"], 
          "sugar": result["sugar"]
          }
      else: # if recipe_id is already in query_results (i.e., if recipe belongs to more than one category)
        query_results[recipe_id]["categories"].append((result["categoryname"], result["categoryid"]))
    
    cursor.close()

    context = {"recipes": query_results}
    return render_template("search_results.html", **context)


"""
# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add(): 
  name = request.form['name']
  params_dict = {"name":name}
  g.conn.execute(text('INSERT INTO test(name) VALUES (:name)'), params_dict)
  g.conn.commit()
  return redirect('/')
"""

# Submit a new review (can only be done by signed in users)
@app.route('/recipe/<int:recipe_id>/submit_review', methods=['GET', 'POST'])
def submit_review(recipe_id):
  user_id = session.get('user_id') # Get the current user's ID
  if not user_id: # If no user selected
    message = "You must select a user to submit a review."
    return render_template("error.html", message=message)
  
  if request.method == 'POST':
    rating = int(request.form.get('rating'))
    content = request.form.get('content')
    datesubmitted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Need to generate ReviewNumber, which will be the current ReviewCount + 1
    # Also get current AggregatedRating b/c it needs to be updated
    cursor = g.conn.execute(text("""SELECT R.ReviewCount, R.AggregatedRating
                                 FROM Recipes_written_by R
                                 WHERE R.RecipeID = :recipeid"""), {"recipeid": recipe_id})
    g.conn.commit()
    reviewcount = None
    aggregatedrating = None
    for result in cursor:
      reviewcount = result[0]
      aggregatedrating = result[1]
    cursor.close()
    reviewnumber = reviewcount + 1 # This will be ReviewNumber of this review as well as updated ReviewCount

    # Insert review into reviews table
    params_dict = {"ReviewNumber": reviewnumber, "Rating": rating, "Content": content, 
                   "DateSubmitted": datesubmitted, "RecipeID": recipe_id, "UserID": user_id}
    g.conn.execute(text("""INSERT INTO Reviews_created_by_evaluates(ReviewNumber, Rating, Content, DateSubmitted, RecipeID, UserID)
                        VALUES (:ReviewNumber, :Rating, :Content, :DateSubmitted, :RecipeID, :UserID)"""), params_dict)
    g.conn.commit()

    # Also update ReviewCount and AggregatedRating in recipes table
    new_aggregatedrating = (aggregatedrating * reviewcount + rating) / reviewnumber
    g.conn.execute(text("""UPDATE Recipes_written_by
                        SET ReviewCount = :reviewnumber, AggregatedRating = :new_aggregatedrating
                        WHERE RecipeID = :recipeid"""), {"reviewnumber": reviewnumber, "recipeid": recipe_id, "new_aggregatedrating": new_aggregatedrating})
    g.conn.commit()

    # Also update ReviewsWritten in Users table
    # First, get current ReviewsWritten
    cursor = g.conn.execute(text("""SELECT U.ReviewsWritten
                                 FROM Users U
                                 WHERE U.UserID = :userid"""), {"userid": user_id})
    g.conn.commit()
    reviewswritten = None
    for result in cursor:
      reviewswritten = result[0]
    cursor.close()

    reviewswritten += 1 # Increment ReviewsWritten by 1

    g.conn.execute(text("""UPDATE Users
                        SET ReviewsWritten = :reviewswritten
                        WHERE UserID = :userid"""), {"reviewswritten": reviewswritten, "userid": user_id})
    g.conn.commit()

    return redirect(url_for('recipe_insights', recipe_id=recipe_id))

  # If GET request, direct to review submission page
  cursor = g.conn.execute(text("""SELECT R.RecipeName 
                               FROM Recipes_written_by R 
                               WHERE R.RecipeID = :recipeid"""), {"recipeid": recipe_id})
  g.conn.commit()
  recipename = ""
  for result in cursor:
    recipename = result[0]
  cursor.close()
  
  return render_template('submit_review.html', recipe_id=recipe_id, recipename=recipename)


# Edit an existing review (can only be done by the review's author)
@app.route('/recipe/<int:recipe_id>/edit_review/<int:review_number>', methods=['GET', 'POST'])
def edit_review(recipe_id, review_number):
  user_id = session.get('user_id') # Get the current user's ID
  if not user_id: # If no user selected
    message = "You must select a user to edit a review."
    return render_template("error.html", message=message)
  
  # Get the review to be edited to prefill the form and calculate new AggregatedRating
  cursor = g.conn.execute(text("""
                               SELECT Rating, Content, UserID
                               FROM Reviews_created_by_evaluates
                               WHERE RecipeID = :recipeid AND ReviewNumber = :reviewnumber
                               """), {"recipeid": recipe_id, "reviewnumber": review_number})
  g.conn.commit()
  results = cursor.mappings().all()
  cursor.close()

  if not results:
    message = "The review does not exist."
    return render_template("error.html", message=message)
  
  review = {}
  for result in results:
    if user_id != int(result["userid"]): # Verify that the current user is the author of review
      message = "You can only edit your own reviews." 
      return render_template("error.html", message=message)
    review["rating"] = result["rating"] # Current rating
    review["content"] = result["content"]
    review["userid"] = result["userid"]
  
  if request.method == 'POST': # Update review based on user input
    new_rating = int(request.form.get('rating'))
    new_content = request.form.get('content')
    datemodified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    params_dict = {"new_rating": new_rating, "new_content": new_content, "datemodified": datemodified,
                   "recipeid": recipe_id, "reviewnumber": review_number}
    g.conn.execute(text("""
                        UPDATE Reviews_created_by_evaluates
                        SET Rating = :new_rating, Content = :new_content, DateModified = :datemodified
                        WHERE RecipeID = :recipeid AND ReviewNumber = :reviewnumber
                        """), params_dict)
    g.conn.commit()

    # Update AggregatedRating in recipes table
    # First, need to get the current AggregatedRating and ReviewCount
    cursor = g.conn.execute(text("""SELECT R.ReviewCount, R.AggregatedRating
                                 FROM Recipes_written_by R
                                 WHERE R.RecipeID = :recipeid"""), {"recipeid": recipe_id})
    g.conn.commit()
    reviewcount = None
    aggregatedrating = None
    for result in cursor:
      reviewcount = result[0]
      aggregatedrating = result[1]
    cursor.close()

    new_aggregatedrating = (aggregatedrating * reviewcount - review["rating"] + new_rating) / reviewcount
    g.conn.execute(text("""UPDATE Recipes_written_by
                        SET AggregatedRating = :new_aggregatedrating
                        WHERE RecipeID = :recipeid"""), {"recipeid": recipe_id, "new_aggregatedrating": new_aggregatedrating})
    g.conn.commit()

    return redirect(url_for('recipe_insights', recipe_id=recipe_id))
  
  return render_template('edit_review.html', review=review, recipe_id=recipe_id, review_number=review_number)
  

# Delete an existing review (can only be done by the review's author)
@app.route('/recipe/<int:recipe_id>/delete_review/<int:review_number>', methods=['GET', 'POST'])
def delete_review(recipe_id, review_number):
  user_id = session.get('user_id') # Get the current user's ID
  if not user_id: # If no user selected
    message = "You must select a user to delete a review."
    return render_template("error.html", message=message)
  
  # Get the review to be edited to prefill the form and calculate new AggregatedRating
  cursor = g.conn.execute(text("""
                               SELECT Rating, Content, UserID
                               FROM Reviews_created_by_evaluates
                               WHERE RecipeID = :recipeid AND ReviewNumber = :reviewnumber
                               """), {"recipeid": recipe_id, "reviewnumber": review_number})
  g.conn.commit()
  results = cursor.mappings().all()
  cursor.close()

  if not results:
    message = "The review does not exist."
    return render_template("error.html", message=message)
  
  review = {}
  for result in results:
    if user_id != int(result["userid"]): # Verify that the current user is the author of review
      message = "You can only delete your own reviews." 
      return render_template("error.html", message=message)
    review["rating"] = result["rating"] # Current rating
    review["content"] = result["content"]
    review["userid"] = result["userid"]

  if request.method == 'POST': # Delete review if user confirms it
    
    g.conn.execute(text("""
                        DELETE FROM Reviews_created_by_evaluates
                        WHERE RecipeID = :recipeid AND ReviewNumber = :reviewnumber
                        """), {"recipeid": recipe_id, "reviewnumber": review_number})
    g.conn.commit()

    # Update AggregatedRating and ReviewCount in recipes table
    # First, need to get the current AggregatedRating and ReviewCount
    cursor = g.conn.execute(text("""SELECT R.ReviewCount, R.AggregatedRating
                                 FROM Recipes_written_by R
                                 WHERE R.RecipeID = :recipeid"""), {"recipeid": recipe_id})
    g.conn.commit()
    reviewcount = None
    aggregatedrating = None
    for result in cursor:
      reviewcount = result[0]
      aggregatedrating = result[1]
    cursor.close()
    
    new_reviewcount = reviewcount - 1
    if new_reviewcount > 0:
      new_aggregatedrating = (aggregatedrating * reviewcount - review["rating"]) / new_reviewcount
    else: # If no review left
      new_aggregatedrating = 0
    g.conn.execute(text("""UPDATE Recipes_written_by
                        SET AggregatedRating = :new_aggregatedrating, ReviewCount = :new_reviewcount
                        WHERE RecipeID = :recipeid"""), 
                        {"recipeid": recipe_id, "new_aggregatedrating": new_aggregatedrating, "new_reviewcount": new_reviewcount})
    g.conn.commit()

    # Also update ReviewsWritten in Users table
    # First, get current ReviewsWritten
    cursor = g.conn.execute(text("""SELECT U.ReviewsWritten
                                 FROM Users U
                                 WHERE U.UserID = :userid"""), {"userid": user_id})
    g.conn.commit()
    reviewswritten = None
    for result in cursor:
      reviewswritten = result[0]
    cursor.close()

    reviewswritten -= 1 # Decrement ReviewsWritten by 1

    g.conn.execute(text("""UPDATE Users
                        SET ReviewsWritten = :reviewswritten
                        WHERE UserID = :userid"""), {"reviewswritten": reviewswritten, "userid": user_id})
    g.conn.commit()

    return redirect(url_for('recipe_insights', recipe_id=recipe_id))
  
  return render_template('delete_review.html', review=review, recipe_id=recipe_id, review_number=review_number)


# Submit a new recipe (can only be done by signed in users)
@app.route('/recipe/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
  user_id = session.get('user_id') # Get the current user's ID
  if not user_id: # If no user selected
    message = "You must select a user to submit a recipe."
    return render_template("error.html", message=message)
  
  if request.method == 'POST':
    recipename = request.form.get('recipename')
    preptime = float(request.form.get('preptime'))
    cooktime = float(request.form.get('cooktime'))
    totaltime = preptime + cooktime
    description = request.form.get('description')
    instructions = request.form.get('instructions')
    servings = request.form.get('servings')
    servings = int(servings) if servings else None # Can be left blank -> null
    calories = request.form.get('calories')
    calories = float(calories) if calories else None # Can be left blank -> null
    sugar = request.form.get('sugar')
    sugar = float(sugar) if sugar else None # Can be left blank -> null
    datepublished = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Need to generate RecipeID, which will be the current max RecipeID + 1
    cursor = g.conn.execute(text("""SELECT MAX(R.RecipeID) FROM Recipes_written_by R"""))
    g.conn.commit()
    recipeid = None
    for result in cursor:
      recipeid = result[0]
    cursor.close()
    recipeid += 1 # This will be the RecipeID for this new recipe

    # Insert review into reviews table
    params_dict = {"RecipeID": recipeid, "RecipeName": recipename, "CookTime": cooktime, "PrepTime": preptime, 
                   "TotalTime": totaltime, "Description": description, "Instructions": instructions, 
                   "AggregatedRating": 0, "ReviewCount": 0, "Servings": servings, "Calories": calories, 
                   "Sugar": sugar, "UserID": user_id, "DatePublished": datepublished}
    g.conn.execute(text("""INSERT INTO Recipes_written_by(RecipeID, RecipeName, CookTime, PrepTime, TotalTime, Description, Instructions, AggregatedRating, ReviewCount, Servings, Calories, Sugar, UserID, DatePublished)
                        VALUES (:RecipeID, :RecipeName, :CookTime, :PrepTime, :TotalTime, :Description, :Instructions, :AggregatedRating, :ReviewCount, :Servings, :Calories, :Sugar, :UserID, :DatePublished)"""), 
                        params_dict)
    g.conn.commit()

    # Update RecipesWritten in Authors table if current user exists in this table
    # If not, insert current user into Authors table
    cursor = g.conn.execute(text("""SELECT A.RecipesWritten
                                 FROM Authors A
                                 WHERE A.UserID = :userid"""), {"userid": user_id})
    g.conn.commit()
    recipeswritten = 0
    for result in cursor:
      recipeswritten = result[0]
    cursor.close()

    if recipeswritten > 0: # User exists in Authors table 
      recipeswritten += 1 # Update RecipesWritten
      g.conn.execute(text("""UPDATE Authors
                        SET RecipesWritten = :recipeswritten
                        WHERE UserID = :userid"""), {"recipeswritten": recipeswritten, "userid": user_id})
      g.conn.commit()
    else: # User does not exist in Authors table
      g.conn.execute(text("""INSERT INTO Authors(UserID, RecipesWritten, Followers)
                          VALUES (:UserID, :RecipesWritten, :Followers)"""), 
                          {"UserID": user_id, "RecipesWritten": 1, "Followers": 0})
      g.conn.commit()

    return render_template('thank_you.html')
  
  return render_template('submit_recipe.html')

# Edit an existing recipe (can only be done by the recipe's author)


# Delete an existing recipe (can only be done by the recipe's author)


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
