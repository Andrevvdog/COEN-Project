from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from recipes.models import Orders, Recipes
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import time, os

def vieworders(request, pIndex = 1):
    orders = Orders.objects
    filter_list = orders.filter(status__lt=9, user_id=request.session['user']['id'])
    mywhere = []
    keyword = request.GET.get("keyword",None)
    if keyword:
        filter_list = filter_list.filter(Q(create_at__contains=keyword))
        mywhere.append('keyword='+keyword)
    
    status = request.GET.get("status",'')
    if status != '':
        filter_list = filter_list.filter(status=status)
        mywhere.append('status='+status)

    pIndex = int(pIndex)
    page = Paginator(filter_list, 6)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    orders_list = page.page(pIndex)
    plist = page.page_range

    for vo in orders_list:
        ro = Recipes.objects.get(id=vo.recipes)
        vo.recipesname = ro.name
        vo.cookingtime = ro.cooking_time * vo.num

        total_calories = 0
        ingredients = []
        for io in ro.ingredients.all():
            ingredients.append(io)
            total_calories += io.calories

        vo.ingredientslist = ingredients
        vo.calories = total_calories * vo.num

    context = {"orderslist":orders_list, 'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    
    return render(request, "users/orders/vieworders.html",context)


def add(request, recipes_id = 0):
    try:
        recipe = Recipes.objects.get(id=recipes_id)
        recipes = Recipes.objects.filter(status__lt=9, user_id=request.session['user']['id']).values("id","name")
        context = {"recipe":recipe, "recipeslist":recipes}
        return render(request, "users/orders/add.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Information Not Found!"}
        return render(request, "users/info.html",context)


def doadd(request, recipes_id = 0):
    try:
        ob = Orders.objects.filter(recipes=recipes_id, user=request.session['user']['id'],status__lt=9)

        if len(ob) != 0:
            ob = ob[0]
            ob.num = request.POST['num']
            if int(request.POST['num']) <= 0:
                context = {'info':"Invalid Number!"}
                return render(request, "users/info.html",context)
            ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.save()

        else:
            ob = Orders()
            ob.user_id = request.session['user']['id']
            ob.recipes = recipes_id
            ob.num = request.POST['num']
            ob.status = 1
            ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.save()

        context = {'info':"Successfully Added!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Add!"}
    
    return render(request, "users/info.html",context)

def delete(request, orders_id = 0):
    try:
        ob = Orders.objects.get(id=orders_id)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Deleted!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Delete!"}
    
    return render(request, "users/info.html",context)


def edit(request, orders_id = 0):
    try:
        orders = Orders.objects.get(id=orders_id)
        recipes = Recipes.objects.filter(status__lt=9, user_id=request.session['user']['id']).values("id","name")
        context = {"orders":orders, "recipeslist":recipes}
        return render(request, "users/orders/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Information Not Found!"}
        return render(request, "users/info.html",context)

def doedit(request, orders_id = 0):
    try:
        ob = Orders.objects.get(id=orders_id)
        if len(Orders.objects.filter(user_id=request.session['user']['id'],recipes__lt=ob.recipes,status__lt=9, recipes=request.POST['recipes_id'])) != 0:
            context = {'info':"Order Already Exists!"}
            return render(request, "users/info.html",context)

        ob.recipes = request.POST['recipes_id']
        if int(request.POST['num']) <= 0:
            context = {'info':"Invalid Number!"}
            return render(request, "users/info.html",context)
        ob.num = request.POST['num']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ob.save()
        context = {'info':"Updated Successfully!"}

    except Exception as err:
        print(err)
        context = {'info':"Fail to Update!"}
    
    return render(request, "users/info.html",context)


