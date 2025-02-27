Description of link to Part 1

Our Part 1 proposal was comprised of:

- Recipe Insights: Shows comprehensive details, such as required ingredients, instructions, preparation/cooking time, serving size, calories, and sugar content when user selects a recipe (though anyone can view the recipe without being logged in).
	- For part 3, we made Rate and Review and Ingredient Assistance features contained within Recipe Insights, plus also added a feature to allow users to modify and delete reviews:
	- Rate and Review: Once logged in, users can leave ratings and reviews for each recipe and, if necessary, have the flexibility to modify or delete their feedback later. Also, users can view reviews written by other users or themselves on each recipe page. Note that users can only modify or delete their own reviews, so they will see the button to modify or delete for their own reviews only.
	
	- Ingredient Assistance: When users delve into a recipe's required ingredients and notice they're missing some, they can click on each ingredient and view the Whole Foods products related to that ingredient - the application will provide information such as company name, product name, prices, and link to the purchase page. But, if there is no Whole Foods products information available with that ingredient, the ingredient name does not have a hyperlink to click on.

- Recipe Exploration: users can widely search for recipes based on recipe name (if the user searches for “shrimp pasta,” the application will give back recipes that have “shrimp pasta,” “shrimp,” or “pasta” in name), recipe categories (Dessert, Vegetable, Asian, etc.), specific ingredients (tomatoes, cabbage, chicken breast, etc.), calories (less than or higher than a certain amount), sugar content (analogous to calories, especially beneficial for individuals with diabetes), authors, ratings, or cooking duration.
	- Note that searching by recipe name feature is slightly modified. If the user selects to search by Name and searches for "salmon", they would get back recipes that have "salmon" in their name like "Smoked Salmon Dip" and "Lemon Marinated Salmon." (We don't have a recipe that has "shrimp" in its name, so we changed the example to be "salmon." Similarly, searching by author name is supported. So, if the user selects to search by Author and search for "Marg", they will get all recipes written by users that have "Marg" contained in their username. The search query is case-insensitive, meaning the users will get back the same result whether they search for "Marg" or "mArG" for example.
	- Searching for recipe categories can be actually done in the main index page instead of a search query. The main index page lists all categories we have, and if the user selects on any, they can see all the recipes contained in it.

- Following and Followers: A user can follow other users and have other users follow them.
	- For part 3, to support this feature, we created a new table 'follows' in our database to keep track of the 'follower' and 'followee' relationship - this addition allows us to update the number of followers and following more easily across Users and Authors. 
	- This feature can be seen in the user profile page. When a user is viewing another user's profile, they will see either a 'follow' button if they are not currently following the other user and an 'unfollow' button if they are currently following the other user. Note that a user cannot follow themselves. Also, when a user is viewing their own profile, they will see the 'following' and 'followers' list that shows all users that they are currently following and the other users that are following the user, respectively.
	- More about the user profile page: This is our newly added feature for part 3! If a user clicks on the hyperlink associated with a user's name, they can view their profile, containing information like numbers of reviews written, following, recipes written, and followers. If a user is viewing their own profile, they will see additional (sensitive) information like their first name, last name, email, and date of birth, along with the hyperlinks to their bookmarked recipes, following list, followers list, and recommended recipes. (These features are explained below in detail.)

- Recipe Submission: Users are encouraged to share their recipes by submitting them to the database. Users will see a hyperlink to submit a new recipe in the main index page. There, they can input all information regarding their recipe they wish to submit. After submitting, the recipe will be added to our database and be seen on the website.

- My Recipe Book: Users can bookmark or save their favorite recipes for easy future access.
	- For part 3, we did something similar as in the case of Followers and Following: We created a new table 'bookmarked' which stores the relationship between users and recipes - just as before, this proved to be a more efficient way to connect users with recipes without affecting both entities separately but being able to reflect their interactions in our website.
	- As briefly explained above, users can view their bookmarked recipes in their own profile. From there, they can also remove a recipe from the bookmarked list by simply clicking on the 'Remove' button.

- Recipe Recommendations: based on the user's activity, such as saved recipes, our system will suggest new recipes that align with their interest according to a simple algorithm.
	- The way we went about this for part 3 was based on prioritizing recipes from authors that the user follows, and if there are none to choose from, then some of the top rated recipes that are recently added will be considered. All users can view the recommended recipes in their profile page and will get a total of 5 recommendations.


Here are some more explanations about our new features for Part 3!

- Index: our index or 'home' website has three features:
	- displays all recipe categories, whereby if the user clicks on a given category, they will be directed to a website which contains the recipes within that category
	- displays our top 5 recipes (most popular ones in terms of aggregated ratings)
	- search bar which allows users to search by recipe name and author

- User/Author Profile: Our user/author profile page allows us to keep track of people's information (e.g., their names to be displayed, first names, last names, followers, following, or recipes and reviews submitted).

- A 'login' feature with a twist: Instead of a real login system, we will imitate one by providing the option to select a user from a dropdown menu. Based on who the current user is, features like modifying/deleting a review or submitting recipe are made available.


Two Interesting Examples (and database operations)

- Submit New Reviews: 

In recipe insights, there is a review submission feature which was slightly tricky to implement, as it in turn updated other tables like reviews and recipes (with attributes such as reviewcount and aggregatedrating) - for this we furthermore considered the cases if a user is selected or not: if it’s not, the user will be directed to the error page, but if it is, we will instead direct them to a site to submit the review. Once the user successfully submits a review, the recipe page will reflect the update in aggregatedrating and the reviews section (which now displays the new review). I thought this page was interesting because of its adaptability in updating values in different entities simultaneously, while handling the update in the review section.

- Followers/Following Feature: 

For the followers/following count under the profile website (similarly to what was done for bookmarks in My Recipe Book), we came up with a table that reflects the relationship between people called “follows”, so that we could keep track of the amount of followers and following - I thought it would be useful to include this because it highlights an approach we came up with since part 1 and which we also implemented for a different site (my recipe book). When a user follows another user, their relationship will be added to the follows table, and if a user unfollows another user, their relationship will be removed from the follows table. Implementing this was ultimately useful because it abstracted the values (followers and following) pertaining to the relationship among authors and users, and it also allowed us to isolate and more easily update these values by having users interact with other authors/users. Plus, the following list is also used when recommending new recipes to a user, so we thought this feature is worth explaining. 
