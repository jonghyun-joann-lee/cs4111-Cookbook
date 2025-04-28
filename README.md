# Project Overview

This project builds upon our Part 1 proposal, adding new features and improvements based on user interaction and database optimization.

---

# Key Features

## 🥘 Recipe Insights
- Displays comprehensive recipe details: ingredients, instructions, preparation/cooking time, serving size, calories, and sugar content.
- **Rate and Review** (New in Part 3):
  - Logged-in users can leave, modify, or delete reviews for recipes.
  - Users can view all reviews, but only modify or delete their own.
- **Ingredient Assistance** (New in Part 3):
  - Clickable ingredients show related Whole Foods products (company name, product name, price, and purchase link).
  - Ingredients without product matches remain plain text without links.

---

## 🔎 Recipe Exploration
- Users can search recipes by:
  - Recipe name (e.g., "salmon" returns "Smoked Salmon Dip," "Lemon Marinated Salmon")
  - Recipe categories (Dessert, Vegetable, Asian, etc.)
  - Specific ingredients (e.g., tomatoes, chicken breast)
  - Calories (less than or greater than a certain value)
  - Sugar content (helpful for users with diabetes)
  - Author name
  - Ratings
  - Cooking duration
- **Notes**:
  - Recipe name and author searches are case-insensitive.
  - Recipe categories are accessible directly from the index (home) page.

---

## 👥 Following and Followers
- Users can follow/unfollow other users.
- Profile page shows:
  - 'Follow' or 'Unfollow' button (depending on relationship).
  - List of users they follow and who follow them.
- **Database Update**:
  - Added a new `follows` table to efficiently manage follower-followee relationships.
- Users cannot follow themselves.
- Viewing your own profile reveals personal info (first name, last name, email, DOB).

---

## 📝 Recipe Submission
- Users can submit new recipes from the main index page.
- Recipes are added to the database and displayed on the site after submission.

---

## 📚 My Recipe Book
- Users can bookmark/save favorite recipes for easy future access.
- **Database Update**:
  - Added a new `bookmarked` table linking users to recipes.
- Users can view and remove bookmarked recipes via their profile page.

---

## 🎯 Recipe Recommendations
- Based on user's activity (e.g., saved recipes).
- Recommendation priorities:
  - Recipes from authors the user follows.
  - Recently added top-rated recipes if no followed authors.
- Users can view 5 recommended recipes on their profile page.

---

# Additional Part 3 Features

## 🏠 Index (Home) Page
- Displays all recipe categories for browsing.
- Highlights top 5 recipes based on aggregated ratings.
- Includes a search bar (search by recipe name or author).

## 👤 User/Author Profile
- Displays:
  - Names
  - Followers
  - Following
  - Submitted recipes and reviews
- If viewing your own profile, additional sensitive info is shown:
  - First name, last name, email, date of birth
  - Links to bookmarks, followers, following, and recommended recipes

## 🔐 Login Simulation
- Instead of real authentication, users select themselves from a dropdown menu.
- Logged-in users can submit recipes, write/edit/delete reviews, etc.

---

# Interesting Implementations

## ✍️ Submitting New Reviews
- Review submission updates multiple tables:
  - `reviews` (new review)
  - `recipes` (updated `reviewcount` and `aggregatedrating`)
- Error handling:
  - No user selected → error page.
  - User selected → review submission page.
- Successful submissions immediately update the recipe's reviews and ratings.

## 🔗 Followers and Following Relationship
- `follows` table efficiently tracks follower-followee relationships.
- Allows easy update/removal of relationships when users follow or unfollow.
- **Bonus**: Follower lists are leveraged in generating personalized recipe recommendations.

---

# Final Notes
- The project has evolved significantly from Part 1 with many database optimizations and user interaction improvements.
- New features like Rating/Review, Ingredient Assistance, Bookmarking, and Profile Pages greatly enhance the user experience.
