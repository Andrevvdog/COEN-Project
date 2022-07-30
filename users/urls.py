from django.contrib import admin
from django.urls import path, include
from users.views import webindex, user, friends
from recipes.views import category, ingredients, recipebook, recipes

urlpatterns = [
    path('', webindex.webindex, name = "users_webindex"),

    path('login', webindex.login, name = "users_login"),
    path('dologin', webindex.dologin, name = "users_dologin"),
    path('logout', webindex.logout, name = "users_logout"),
    path('verify', webindex.verify, name = "users_verify"),
    path('register', webindex.register, name = "users_register"),
    path('doregister', webindex.doregister, name = "users_doregister"),


    path('user/edit/<int:user_id>', user.edit, name = "users_user_edit"),
    path('user/doedit/<int:user_id>', user.doedit, name = "users_user_doedit"),

    path('category/<int:pIndex>', category.viewcategory, name = "users_category_viewcategory"),
    path('category/add', category.add, name = "users_category_add"),
    path('category/doadd', category.doadd, name = "users_category_doadd"),
    path('category/del/<int:category_id>', category.delete, name = "users_category_delete"),
    path('category/edit/<int:category_id>', category.edit, name = "users_category_edit"),
    path('category/doedit/<int:category_id>', category.doedit, name = "users_category_doedit"),
    path('category/load/', category.loadCategory, name = "users_category_load"),

    path('ingredients/<int:pIndex>', ingredients.viewingredients, name = "users_ingredients_viewingredients"),
    path('ingredients/add', ingredients.add, name = "users_ingredients_add"),
    path('ingredients/doadd', ingredients.doadd, name = "users_ingredients_doadd"),
    path('ingredients/del/<int:ingredients_id>', ingredients.delete, name = "users_ingredients_delete"),
    path('ingredients/edit/<int:ingredients_id>', ingredients.edit, name = "users_ingredients_edit"),
    path('ingredients/doedit/<int:ingredients_id>', ingredients.doedit, name = "users_ingredients_doedit"),

    path('friends/<int:pIndex>', friends.viewfriends, name = "users_friends_viewfriends"),
    path('friends/add', friends.add, name = "users_friends_add"),
    path('friends/del/<int:friends_id>', friends.delete, name = "users_friends_delete"),
    path('friends/doadd', friends.doadd, name = "users_friends_doadd"),
    path('friends/edit/<int:friends_id>', friends.edit, name = "users_friends_edit"),
    path('friends/doedit/<int:friends_id>', friends.doedit, name = "users_friends_doedit"),

    path('recipebook/<int:pIndex>', recipebook.viewrecipebook, name = "users_recipebook_viewrecipebook"),
    path('recipebook/add', recipebook.add, name = "users_recipebook_add"),
    path('recipebook/del/<int:recipebook_id>', recipebook.delete, name = "users_recipebook_delete"),
    path('recipebook/doadd', recipebook.doadd, name = "users_recipebook_doadd"),
    path('recipebook/edit/<int:recipebook_id>', recipebook.edit, name = "users_recipebook_edit"),
    path('recipebook/doedit/<int:recipebook_id>', recipebook.doedit, name = "users_recipebook_doedit"),
    path('recipebook/showrecipes/<int:pIndex>', recipebook.showrecipes, name = "users_recipebook_showrecipes"),

    path('recipes/<int:pIndex>', recipes.viewrecipes, name = "users_recipes_viewrecipes"),
    path('recipes/add', recipes.add, name = "users_recipes_add"),
    path('recipes/del/<int:recipes_id>', recipes.delete, name = "users_recipes_delete"),
    path('recipes/doadd', recipes.doadd, name = "users_recipes_doadd"),
    path('recipes/edit/<int:recipes_id>', recipes.edit, name = "users_recipes_edit"),
    path('recipes/doedit/<int:recipes_id>', recipes.doedit, name = "users_recipes_doedit"),
    path('recipes/recipesdetail/<int:recipes_id>', recipes.recipesdetail, name = "users_recipes_recipesdetail"),

]
