from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from recipes.models import Category, Ingredients
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse

def viewcategory(request, pIndex = 1):
    category = Category.objects
    filter_list = category.filter(status__lt=9)
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
    page = Paginator(filter_list, 5)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    category_list = page.page(pIndex)
    plist = page.page_range

    context = {"categorylist":category_list, 'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    
    return render(request, "users/category/viewcategory.html",context)

def add(request):
    return render(request, "users/category/add.html")

def doadd(request):
    try:
        ob = Category()
        ob.name = request.POST['name']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Added!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Add!"}
    
    return render(request, "users/category/categoryinfo.html",context)

def delete(request, category_id = 0):
    try:
        ob = Category.objects.get(id=category_id)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()

        # Delete the corresponding ingredients
        ingredients_list = Ingredients.objects.filter(category_id = category_id)
        for ob in ingredients_list:
            ob.status = 9
            ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.save()

        context = {'info':"Successfully Deleted!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Delete!"}
    
    return render(request, "users/category/categoryinfo.html",context)

def edit(request, category_id = 0):
    try:
        ob = Category.objects.get(id=category_id)
        context = {'category':ob}
        return render(request, "users/category/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Information Not Found!"}
        return render(request, "users/category/categoryinfo.html",context)

def doedit(request, category_id = 0):
    try:
        ob = Category.objects.get(id=category_id)
        if request.POST['name']:
            ob.name = request.POST['name']
        # ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Editted!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Edit!"}
    
    return render(request, "users/category/categoryinfo.html",context)

def showingredients(request, pIndex = 1):
    cid = request.GET.get("cid",0)

    print(request.session['cid']) 

    if cid != 0 and request.session['cid'] == '0':
        request.session['cid'] = str(cid)

    elif request.session['cid'] != '0' and cid != 0:
        request.session['cid'] = str(cid)
    
    elif request.session['cid'] != '0' and cid == 0:
        cid = int(request.session['cid'])

    else:
        context = {'info':"Unknown Error!"}
        return render(request, "attendees/info.html",context)

    ingredients = Ingredients.objects
    filter_list = ingredients.filter(status__lt=9, category_id=cid)

    mywhere = []
    keyword = request.GET.get("keyword",None)
    if keyword:
        filter_list = filter_list.filter(Q(name__contains=keyword)).distinct()
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
    ingredients_list = page.page(pIndex)
    plist = page.page_range

    for vo in ingredients_list:
        cob = Category.objects.get(id=vo.category_id)
        vo.categoryname = cob.name

    context = {"ingredientslist":ingredients_list, 'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    
    return render(request, "users/category/showingredients.html",context)

