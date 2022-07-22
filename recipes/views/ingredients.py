from pickle import NONE
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from recipes.models import Category, Ingredients
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import time, os

def viewingredients(request, pIndex=1):
    ingredients = Ingredients.objects
    filter_list = ingredients.filter(status__lt=9)
    mywhere = []
    keyword = request.GET.get("keyword",None)
    if keyword:
        filter_list = filter_list.filter(name__contains=keyword)
        mywhere.append('keyword='+keyword)

    category_id = request.GET.get("category_id",None)
    if category_id:
        filter_list = filter_list.filter(category_id=category_id)
        mywhere.append('category_id='+category_id)
    
    status = request.GET.get("status",'')
    if status != '':
        filter_list = filter_list.filter(status=status)
        mywhere.append('status='+status)

    pIndex = int(pIndex)
    page = Paginator(filter_list, 5)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    ingredients_list = page.page(pIndex)
    plist = page.page_range

    for vo in ingredients_list:
        cob = Category.objects.get(id=vo.category_id)
        vo.categoryname = cob.name

    context = {"ingredientslist":ingredients_list, 'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    
    return render(request, "users/Ingredients/viewingredients.html",context)

def add(request):
    clist = Category.objects.filter(status__lt=9).values("id","name")
    context = {"categorylist":clist}
    return render(request, "users/Ingredients/add.html", context)

def doadd(request):
    try:
        pic_file = request.FILES.get("cover_pic",None)
        if not pic_file:
            return HttpResponse("No Cover Picture Information!")
        cover_pic = str(time.time())+"."+pic_file.name.split('.').pop()
        destination = open("./static/uploads/Ingredients/"+cover_pic,"wb+")
        for chunk in pic_file.chunks():   
            destination.write(chunk)  
        destination.close()

        ob = Ingredients()
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.calories = request.POST['calories']
        ob.cover_pic = cover_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Added!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Add!"}
    
    return render(request, "users/info.html",context)

def delete(request, ingredients_id = 0):
    try:
        ob = Ingredients.objects.get(id=ingredients_id)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Deleted!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Delete!"}
    
    return render(request, "users/info.html",context)

def edit(request, ingredients_id = 0):
    try:
        ob = Ingredients.objects.get(id=ingredients_id)
        clist = Category.objects.filter(status__lt=9).values("id","name")
        context = {'Ingredients':ob,"categorylist":clist}
        return render(request, "users/Ingredients/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Information Not Found!"}
        return render(request, "users/info.html",context)

def doedit(request, ingredients_id = 0):
    try:
        ob = Ingredients.objects.get(id=ingredients_id)
        # ob.Recipe_id_id = request.POST['Recipe_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.calories = request.POST['calories']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        oldpicname = request.POST['oldpicname']
        pic_file = request.FILES.get("cover_pic",None)
        if not pic_file:
            cover_pic = oldpicname
        else:    
            cover_pic = str(time.time())+"."+pic_file.name.split('.').pop()
            destination = open("./static/uploads/Ingredients/"+cover_pic,"wb+")
            for chunk in pic_file.chunks():  
                destination.write(chunk)  
            destination.close()
            
        ob.cover_pic = cover_pic
        ob.save()
        context = {'info':"Updated Successfully!"}

        if pic_file:
            os.remove("./static/uploads/Ingredients/"+oldpicname)

    except Exception as err:
        print(err)
        context = {'info':"Fail to Update!"}

        if pic_file:
            os.remove("./static/uploads/Ingredients/"+cover_pic)
    
    return render(request, "users/info.html",context)