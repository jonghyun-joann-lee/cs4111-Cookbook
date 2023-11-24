Usage of AI Tools for Project 1 Part 3

We used ChatGPT for the following tasks where the usage of it is allowed.

1. Asked how to construct a table in HTML when writing category_recipes.html
a. Prompt: 
In HTML, how do you create a table with columns that are named Recipe Name, Author, TotalTime, AggregatedRating, Calories, and Sugar (grams)? 

b. Response: 
Creating a table in HTML with specific column names involves using the <table>, <tr>, <th>, and <td> tags. Here's how you would structure a table with the columns "Recipe Name", "Author", "Category", "Total Time", "Aggregated Rating", "Calories", and "Sugar (grams)":
<table>
  <!-- Table Header -->
  <tr>
    <th>Recipe Name</th>
    <th>Author</th>
    <th>Total Time</th>
    <th>Aggregated Rating</th>
    <th>Calories</th>
    <th>Sugar (grams)</th>
  </tr>

  <!-- Table Row Example -->
  <tr>
    <td>Example Recipe</td>
    <td>Example Author</td>
    <td>Example Time</td>
    <td>Example Rating</td>
    <td>Example Calories</td>
    <td>Example Sugar</td>
  </tr>

  <!-- Add more rows as needed -->
</table>

In this structure:

<table> is the container for your table.
<tr> stands for "table row" and is used for each row of the table.
<th> stands for "table header" and is used for header cells, which typically contain the titles for each column.
<td> stands for "table data" and is used for the actual data cells of the table.
You can add as many <tr> sections as you need for the number of rows you want in your table, and each <tr> should contain <td> elements corresponding to the data for each column.

c. Usage: 
Copied the code given by ChatGPT and tweaked it to use a loop for inserting row examples into the table by putting {% for recipe in recipes %}.


2. Asked how to insert link for a variable to direct users to the associated page for that variable in HTML when writing index.html
a. Prompt: 
I have a variable named category_name in HTML. I want users to be able to click on that and be directed to a page that is associated with it. I have a python code that routes to it like this.
@app.route('/category/<category_name>')
def category(category_name):
  (actual code ommitted)
  return render_template("category_recipes.html", **context)

b. Response: 
To create a clickable link in HTML that directs users to the page associated with category_name, you can use an anchor (<a>) tag. The href attribute of the anchor tag will be dynamically set to the URL route you've defined in your Python code.

Here's how you can do it:

HTML Template:
In your HTML template, you would typically loop through a list of categories or directly use category_name if it's a single item. The anchor tag's href attribute should point to the URL defined by your Flask route.

html
Copy code
<!-- If you have a list of categories -->
{% for category in categories %}
<a href="{{ url_for('category', category_name=category.name) }}">{{ category.name }}</a>
{% endfor %}

<!-- If it's a single category -->
<a href="{{ url_for('category', category_name=category_name) }}">{{ category_name }}</a>
In this snippet, url_for is a Flask function that generates a URL to the given endpoint with the method provided. category is the name of the function in your Python route, and category_name is the variable part of the URL.

Python Route:
Your Python Flask route looks correct. When a user clicks on the link, they will be directed to a URL like /category/<category_name>, and your category function will handle the request.

python
Copy code
@app.route('/category/<category_name>')
def category(category_name):
    # Your code to handle the request
    return render_template("category_recipes.html", **context)
This setup will create a clickable link in your HTML template that directs users to the specific category page as defined in your Flask route. Make sure that category_name in the url_for function matches the variable name in the route decorator in your Flask app.

c. Usage:
Copied the code provided by ChatGPT that uses href and the url_for function into index.html
(Update) Use the idea but made all necessary changes to use category_id instead of the name after encounting issues with the url when category name contains '/' (e.g. Soy/Tofu)


3. Asked if there is a way to check whether a variable is empty or not in HTML
a. Prompt:
Is there a way to check if a variable passed onto HTML is empty or not when that variable is a list?

b. Response:
Yes, you can check if a variable passed into HTML is empty or not, even when that variable is a list. This can be achieved through various methods, depending on the server-side language you are using to generate the HTML. Here are some common approaches:
...(Approahces using JavaScript, PHP, etc.)
Using Python (with a web framework like Flask or Django)
In the HTML template:
{% if my_list %}
    <!-- List is not empty -->
    <p>The list is not empty</p>
{% else %}
    <!-- List is empty -->
    <p>The list is empty</p>
{% endif %}
...(Other approaches)

c. Usage:
Incorporated the given code into category_recipes.html but changed the variable my_list to recipes 


4. Asked how to check if it is the end of a list in HTML
a. Prompt: 
In HTML, I have a variable named recipe.categories, which is a list of tuples. How do I check if it is the end of a list?  It not, I would like to add a comma right after the list item. If it is, I do not want to add a comma. Here are the lines of the HTML code that I wish to modify.

<td>
  {% for category_name, category_id in recipe.categories %} <!-- recipe.categories = [(CategoryName, CategoryID)] -->
  <a href="{{ url_for('category', category_id=category_id) }}">{{ category_name }}</a>
  {% endfor %}
</td> 
  
b. Response:
To modify your HTML code to include a comma after each list item except the last one in the recipe.categories list, you can utilize Jinja2's loop control variables. Jinja2, which is often used in Flask applications, provides a loop.last variable that can be used to check if the current iteration is the last in the loop. You can conditionally add a comma based on this.

Here's how you can modify your code snippet:
<td>
  {% for category_name, category_id in recipe.categories %} <!-- recipe.categories = [(CategoryName, CategoryID)] -->
  <a href="{{ url_for('category', category_id=category_id) }}">{{ category_name }}</a>{% if not loop.last %}, {% endif %}
  {% endfor %}
</td>

In this code:

{% if not loop.last %}, {% endif %}: This line checks if the current loop iteration is not the last one. If it's not the last, a comma (,) is added right after the link. The space after the comma ensures that there is a space between the comma and the next item in the list. If it is the last item, no comma is added.
Remember that this solution assumes you are using Jinja2 templating with Flask or a similar Python web framework. If you're using a different templating engine, the approach might be slightly different.

c. Usage:
Incorporated the given code by ChatGPT into all_recipes.html


5. Asked how to add search function in HTML with a dropdown box, text input box, and a search button
a. Prompt: 
I want to add a search functionality in my existing html page. For the design, I want something like "Search for a recipe: " and then a dropdown box that allows users to choose either name or author to search for and then a text input box and then a search button. I am using Flask application and Jinja2 template.

b. Response: 
To add a search functionality with the specified design to your existing HTML page in a Flask application using Jinja2 templates, you'll need to modify both your HTML (with Jinja2 syntax) and your Flask backend. Here's a step-by-step guide to achieve this:

1. HTML Template with Jinja2
You'll need to create a form in your HTML template that includes a dropdown box, a text input box, and a search button. Here's an example of how you could structure it:

<form action="{{ url_for('search_results') }}" method="get">
  <label for="search-for">Search for a recipe:</label>
  <select name="search_type" id="search-type">
    <option value="name">Name</option>
    <option value="author">Author</option>
  </select>
  <input type="text" name="query" required>
  <button type="submit">Search</button>
</form>

2. Flask Backend
In your Flask application, you'll need to handle the search. This function will take the query parameters, perform the search, and return the results.

@app.route('/search_results')
def search_results():
    search_type = request.args.get('search_type')
    query = request.args.get('query')

    # Implement your search logic here
    # For example, query your database based on search_type and query

    results = perform_search(search_type, search_query) # This is a placeholder function

    return render_template('search_results.html', results=results)

def perform_search(search_type, query):
    # Implement your search logic here
    # This function should return the search results based on the type and query
    pass

3. Search Results Template
Create a new Jinja2 template (e.g., search_results.html) to display the search results. 

<!-- search_results.html -->
{% extends 'base.html' %} <!-- or your base template -->

{% block content %}
    <h2>Search Results</h2>
    {% for result in results %}
        <!-- Display each result, e.g., result.name, result.author -->
    {% endfor %}
{% endblock %}

4. Styling and JavaScript (Optional)
You can add CSS to style your form and use JavaScript to enhance the user experience, such as adding real-time search suggestions.

5. Database Integration
The perform_search function in your Flask app should contain the logic to query your database based on the search_type and search_query. This implementation depends on your database structure and the ORM (if any) you're using.

6. Testing
Once everything is set up, test the functionality thoroughly to ensure that the search works as expected and the results are displayed correctly.

This setup gives you a basic search functionality. Depending on your application's requirements, you might need to add more complex features like pagination, advanced search filters, or full-text search capabilities.

c. Usage: 
For creating the dropbox, search box, and search button, copied the provided code by ChatGPT into index.html
For creating route function in python, referred to ChatGPT on how to access the user's input (e.g. request.args.get('search_type')), but implemented the search logic and processing of the results by myself.
For search_results.html, did not refer to ChatGPT's response. I used the same table style in all_recipes.html that I previously wrote.

6. Aksed how to create a dropdown menu that lists all users and allow to choose one in HTML
a. Prompt: 
Please write in HTML for displaying a dropdown menu that allows to choose a user based on displayname (with a loop that goes around for all users) and store the user_id for the session. I'm using Flask and Jinja2 template. 

b. Response:
1. User Dropdown on Each Page:
You could add a dropdown menu to your website's layout that lists all users. When a selection is made, the chosen user ID is stored in the session. This allows you to "simulate" different users interacting with the application without a login system.

<!-- Place this in a base template that other templates extend -->
<form action="{{ url_for('set_user') }}" method="post">
    <select name="user_id" onchange="this.form.submit()">
        {% for user in users %}
            <option value="{{ user.UserID }}">{{ user.DisplayName }}</option>
        {% endfor %}
    </select>
</form>

2. Route to Set the Current User:

@app.route('/set_user', methods=['POST'])
def set_user():
    session['user_id'] = request.form['user_id']
    return redirect(request.referrer or url_for('index'))
This route sets the selected user ID into the session and then redirects back to the page the user was on, or to the index if the referrer is not available.

3. Using the Current User ID:
When you need to perform actions like submitting reviews or recipes, you would use session['user_id'] to get the currently selected user's ID.

For displaying the dropdown, make sure to fetch the list of users from the database and pass it to your base template. If you're using template inheritance, you can make this dropdown part of your base layout so it's available on every page.

c. Usage: 
Integrated the provided HTML code by ChatGPT into all HTML templates to allow selecting who the current user is. This was to mimic the user login system and show different functionalities based on who the current user is. Any user can write new reviews or recipes, but the current user can modify or delete only its review or recipe.
Made a minor tweak to reflect the variables that I pass onto the tempaltes.
Also, referred to the response by ChatGPT on how to create a route function in python that uses the input submitted by the user (the selected user displayname).
Also, made a minor tweak here to redirect users to the index page.
Plus, searched on Google how to use the Flask's session object and pass on context to every template using @app.context_processor.


7. Debugging error related to Flask
a. Prompt:
What is this error? What should I do?

Traceback (most recent call last):
  File "server.py", line 101, in <module>
    users = all_users()
  File "server.py", line 86, in all_users
    cursor = g.conn.execute(text("""SELECT UserID, DisplayName FROM People"""))
  File "/home/jl6509/.virtualenvs/dbproj/lib/python3.8/site-packages/werkzeug/local.py", line 311, in __get__
    obj = instance._get_current_object()
  File "/home/jl6509/.virtualenvs/dbproj/lib/python3.8/site-packages/werkzeug/local.py", line 508, in _get_current_object
    raise RuntimeError(unbound_message) from None
RuntimeError: Working outside of application context.

This typically means that you attempted to use functionality that needed
the current application. To solve this, set up an application context
with app.app_context(). See the documentation for more information.

b. Response:

The error you're encountering is because you're trying to use Flask's g object outside of an application context. Flask's g object, which is used for storing and sharing data during the lifetime of an app context (typically a web request), cannot be accessed when your application is starting up or outside of a view function.

Since you're trying to fetch users at the module level (i.e., when your Python script is being executed, which is outside of an application context), you're seeing this error.

Here's how you can modify your all_users() function to run within an application context:

def all_users():
    with app.app_context():
        cursor = g.conn.execute(text("""SELECT UserID, DisplayName FROM People"""))
        results = cursor.mappings().all()
        users = {result['UserID']: result['DisplayName'] for result in results}
        cursor.close()
    return users
By wrapping the database access code with app.app_context(), you manually create an application context, which allows you to use g.

Alternatively, since you're fetching users at the start of your application, you might want to establish a connection to the database directly rather than using g.conn. Here's an example of how you might do it:

from sqlalchemy import create_engine, text

# Assuming you have a DATABASE_URI variable set up in your config
database_uri = "your_database_uri_here"  # Replace with your database URI
engine = create_engine(database_uri)

def all_users():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT UserID, DisplayName FROM People"))
        users = {row['UserID']: row['DisplayName'] for row in result}
        return users

# Now you can call all_users() to initialize the global users variable
users = all_users()

In this case, you're not using Flask's g object at all but rather creating a new database connection using SQLAlchemy's create_engine method, which is independent of the Flask app context.

Remember that if you use the second approach, you need to ensure that your database URI is correctly set up in app.config['DATABASE_URI'].

Choose the method that best fits your application's design and structure.

c. Usage:
Implemented the first way of wrapping my code with app.app_context() as suggested by ChatGPT but received an error.
So implemented the second way of using engine.connect() as conn.

