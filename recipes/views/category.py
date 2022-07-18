from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from recipes.models import Category
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse

def index(request, pIndex=1):
    umod = Category.objects
    ulist = umod.filter(status__lt=9)
    mywhere = []
    kw = request.GET.get("keyword",None)
    if kw:
        ulist = ulist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
    
    status = request.GET.get("status",'')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append('status='+status)

    pIndex = int(pIndex)
    page = Paginator(ulist, 10)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    plist = page.page_range

    context = {"categorylist":list2, 'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    
    return render(request, "users/category/index.html",context)

def add(request):
    return render(request, "users/category/add.html")

def insert(request):
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
    
    return render(request, "users/info.html",context)

def delete(request, cid = 0):
    try:
        ob = Category.objects.get(id=cid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Deleted!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Delete!"}
    
    return render(request, "users/info.html",context)

def edit(request, cid = 0):
    try:
        ob = Category.objects.get(id=cid)
        # slist = Recipe.objects.values("id","name")
        # context = {'category':ob,"Recipelist":slist}
        context = {'category':ob}
        return render(request, "users/category/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Information Not Found!"}
        return render(request, "users/info.html",context)

def update(request, cid = 0):
    try:
        ob = Category.objects.get(id=cid)
        ob.name = request.POST['name']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Editted!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Edit!"}
    
    return render(request, "users/info.html",context)


def loadCategory(request):
    clist = Category.objects.filter(status__lt=9).values("id","name")
    return JsonResponse({'data':list(clist)})