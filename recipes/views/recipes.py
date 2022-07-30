from pickle import NONE
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from recipes.models import Ingredients, RecipeBook, Recipes
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import time, os

def viewrecipes(request, pIndex=1):
    recipes = Recipes.objects
    filter_list = recipes.filter(status__lt=9, user_id=request.session['user']['id'])
    mywhere = []
    keyword = request.GET.get("keyword",None)
    if keyword:
        filter_list = filter_list.filter(Q(name__contains=keyword) | Q(ingredients__name__contains=keyword))
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
    recipes_list = page.page(pIndex)
    plist = page.page_range

    for vo in recipes_list:
        total_calories = 0
        for io in vo.ingredients.all():
            total_calories += io.calories
        vo.calories = total_calories

    context = {"recipeslist":recipes_list, 'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    
    return render(request, "users/recipes/viewrecipes.html",context)


def add(request):
    recipebook = RecipeBook.objects.filter(status__lt=9, user_id=request.session['user']['id']).values("id","name")
    ingredients = Ingredients.objects.filter(status__lt=9).values("id","name")
    context = {"recipebooklist":recipebook, "ingredientslist":ingredients}
    return render(request, "users/recipes/add.html",context)


def doadd(request):
    try:
        pic_file = request.FILES.get("cover_pic",None)
        if not pic_file:
            return HttpResponse("No Cover Picture Information!")
        cover_pic = str(time.time())+"."+pic_file.name.split('.').pop()
        destination = open("./static/uploads/Recipes/"+cover_pic,"wb+")
        for chunk in pic_file.chunks():   
            destination.write(chunk)  
        destination.close()

        ob = Recipes()
        ob.user_id = request.session['user']['id']
        ob.recipebook_id = request.POST['recipebook_id']
        ob.name = request.POST['name']
        ob.cover_pic = cover_pic
        ob.rate = request.POST['rate']
        ob.methods = request.POST['methods']
        ob.cooking_time = request.POST['cooking_time']
        ob.keywords = request.POST['keywords']

        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()

        ingredients = request.POST.getlist('ingredients')

        for vo in ingredients:
            ob.ingredients.add(vo)

        context = {'info':"Successfully Added!"}

    except Exception as err:
        print(err)
        context = {'info':"Fail to Add!"}
    
    return render(request, "users/info.html",context)


def delete(request, recipes_id = 0):
    try:
        ob = Recipes.objects.get(id=recipes_id)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Deleted!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Delete!"}
    
    return render(request, "users/info.html",context)


def edit(request, recipes_id = 0):
    try:
        ob = Recipes.objects.get(id=recipes_id)
        rblist = RecipeBook.objects.filter(status__lt=9).values("id","name")
        
        iblist = Ingredients.objects.filter(status__lt=9)
        ib = [int(vo.id) for vo in ob.ingredients.all()]

        context = {'recipes':ob,'recipebooklist':rblist,'ingredientslist':iblist,'ingerdientid':ib}
        return render(request, "users/recipes/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Information Not Found!"}
        return render(request, "users/info.html",context)


def doedit(request, recipes_id = 0):
    try:
        ob = Recipes.objects.get(id=recipes_id)
        ob.recipebook_id = request.POST['recipebook_id']
        ob.name = request.POST['name']
        ob.rate = request.POST['rate']
        ob.methods = request.POST['methods']
        ob.cooking_time = request.POST['cooking_time']
        ob.keywords = request.POST['keywords']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        oldpicname = request.POST['oldpicname']
        pic_file = request.FILES.get("cover_pic",None)
        if not pic_file:
            cover_pic = oldpicname
        else:    
            cover_pic = str(time.time())+"."+pic_file.name.split('.').pop()
            destination = open("./static/uploads/Recipes/"+cover_pic,"wb+")
            for chunk in pic_file.chunks():  
                destination.write(chunk)  
            destination.close()
            
        ob.cover_pic = cover_pic
        ob.save()
        
        ob.ingredients.clear()
        ingredients = request.POST.getlist('ingredients')

        for vo in ingredients:
            ob.ingredients.add(vo)


        context = {'info':"Updated Successfully!"}

        if pic_file:
            os.remove("./static/uploads/Recipes/"+oldpicname)

    except Exception as err:
        print(err)
        context = {'info':"Fail to Update!"}

        if pic_file:
            os.remove("./static/uploads/Recipes/"+cover_pic)
    
    return render(request, "users/info.html",context)


def recipesdetail(request, recipes_id = 0):
    
    recipes = Recipes.objects.get(id=recipes_id)
    recipebook = RecipeBook.objects.get(id=recipes.recipebook_id)

    recipes.recipebookname = recipebook.name
    recipes.methodslist = recipes.methods.split('@')

    ingredients = []
    total_calories = 0
    for io in recipes.ingredients.all():
        ingredients.append(io)
        total_calories += io.calories
    recipes.ingredientslist = ingredients
    recipes.calories = total_calories

    context = {'recipelist':recipes}
    
    return render(request, "users/recipes/recipesdetail.html",context)