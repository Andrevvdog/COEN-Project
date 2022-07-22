from django.contrib import admin
from django.urls import path, include
from users.views import index, user
from recipes.views import category, ingredients

urlpatterns = [
    path('', index.index, name = "users_index"),

    path('login', index.login, name = "users_login"),
    path('dologin', index.dologin, name = "users_dologin"),
    path('logout', index.logout, name = "users_logout"),
    path('verify', index.verify, name = "users_verify"),
    path('register', index.register, name = "users_register"),
    path('doregister', index.doregister, name = "users_doregister"),


    path('user/edit/<int:user_id>', user.edit, name = "users_user_edit"),
    path('user/update/<int:user_id>', user.update, name = "users_user_update"),

    path('category/<int:pIndex>', category.index, name = "users_category_index"),
    path('category/add', category.add, name = "users_category_add"),
    path('category/insert', category.insert, name = "users_category_insert"),
    path('category/del/<int:category_id>', category.delete, name = "users_category_delete"),
    path('category/edit/<int:category_id>', category.edit, name = "users_category_edit"),
    path('category/update/<int:category_id>', category.update, name = "users_category_update"),
    path('category/load/', category.loadCategory, name = "users_category_load"),

    path('ingredients/<int:pIndex>', ingredients.index, name = "users_ingredients_index"),
    path('ingredients/add', ingredients.add, name = "users_ingredients_add"),
    path('ingredients/insert', ingredients.insert, name = "users_ingredients_insert"),
    path('ingredients/del/<int:ingredients_id>', ingredients.delete, name = "users_ingredients_delete"),
    path('ingredients/edit/<int:ingredients_id>', ingredients.edit, name = "users_ingredients_edit"),
    path('ingredients/update/<int:ingredients_id>', ingredients.update, name = "users_ingredients_update"),

]
