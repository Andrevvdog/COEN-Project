from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from recipes.models import RecipeBook, Recipes
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import time, os

def viewrecipebook(request, pIndex=1):
    recipebook = RecipeBook.objects
    filter_list = recipebook.filter(status__lt=9, user_id=request.session['user']['id'])
    mywhere = []
    keyword = request.GET.get("keyword",None)
    if keyword:
        filter_list = filter_list.filter(name__contains=keyword)
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
    recipebook_list = page.page(pIndex)
    plist = page.page_range

    context = {"recipebooklist":recipebook_list, 'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    
    return render(request, "users/recipebook/viewrecipebook.html",context)


def add(request):
    return render(request, "users/recipebook/add.html")


def doadd(request):
    try:
        pic_file = request.FILES.get("cover_pic",None)
        if not pic_file:
            return HttpResponse("No Cover Picture Information!")
        cover_pic = str(time.time())+"."+pic_file.name.split('.').pop()
        destination = open("./static/uploads/Recipebook/"+cover_pic,"wb+")
        for chunk in pic_file.chunks():   
            destination.write(chunk)  
        destination.close()

        ob = RecipeBook()
        ob.user_id = request.session['user']['id']
        ob.name = request.POST['name']
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

def delete(request, recipebook_id = 0):
    try:
        ob = RecipeBook.objects.get(id=recipebook_id)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Deleted!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Delete!"}
    
    return render(request, "users/info.html",context)


def edit(request, recipebook_id = 0):
    try:
        ob = RecipeBook.objects.get(id=recipebook_id)
        context = {'recipebook':ob}
        return render(request, "users/recipebook/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Information Not Found!"}
        return render(request, "users/info.html",context)

def doedit(request, recipebook_id = 0):
    try:
        ob = RecipeBook.objects.get(id=recipebook_id)
        ob.name = request.POST['name']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        oldpicname = request.POST['oldpicname']
        pic_file = request.FILES.get("cover_pic",None)
        if not pic_file:
            cover_pic = oldpicname
        else:    
            cover_pic = str(time.time())+"."+pic_file.name.split('.').pop()
            destination = open("./static/uploads/Recipebook/"+cover_pic,"wb+")
            for chunk in pic_file.chunks():  
                destination.write(chunk)  
            destination.close()
            
        ob.cover_pic = cover_pic
        ob.save()
        context = {'info':"Updated Successfully!"}

        if pic_file:
            os.remove("./static/uploads/Recipebook/"+oldpicname)

    except Exception as err:
        print(err)
        context = {'info':"Fail to Update!"}

        if pic_file:
            os.remove("./static/uploads/Recipebook/"+cover_pic)
    
    return render(request, "users/info.html",context)

def showrecipes(request, pIndex=1):
    rbid = request.GET.get("rbid",0)

    print(request.session['rbid']) 

    if rbid != 0 and request.session['rbid'] == '0':
        request.session['rbid'] = str(rbid)

    elif request.session['rbid'] != '0' and rbid != 0:
        request.session['rbid'] = str(rbid)
    
    elif request.session['rbid'] != '0' and rbid == 0:
        rbid = int(request.session['rbid'])

    else:
        context = {'info':"Unknown Error!"}
        return render(request, "attendees/info.html",context)

    recipes = Recipes.objects
    filter_list = recipes.filter(status__lt=9, user_id=request.session['user']['id'], recipebook_id=rbid)

    mywhere = []
    keyword = request.GET.get("keyword",None)
    if keyword:
        filter_list = filter_list.filter(Q(name__contains=keyword) | Q(ingredients__name__contains=keyword)).distinct()
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
    
    return render(request, "users/recipebook/showrecipes.html",context)


