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



