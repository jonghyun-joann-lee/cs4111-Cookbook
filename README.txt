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

