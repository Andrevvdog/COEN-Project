from pickle import NONE
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from users.models import Category, Ingredients
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import time, os

def index(request, pIndex=1):
    umod = Ingredients.objects
    ulist = umod.filter(status__lt=9)
    mywhere = []
    kw = request.GET.get("keyword",None)
    if kw:
        ulist = ulist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)

    cid = request.GET.get("category_id",None)
    if cid:
        ulist = ulist.filter(category_id=cid)
        mywhere.append('category_id='+cid)
    
    status = request.GET.get("status",'')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append('status='+status)

    pIndex = int(pIndex)
    page = Paginator(ulist, 5)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    plist = page.page_range

    for vo in list2:
        cob = Category.objects.get(id=vo.category_id)
        vo.categoryname = cob.name

    context = {"ingredientslist":list2, 'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    
    return render(request, "users/Ingredients/index.html",context)

def add(request):
    clist = Category.objects.values("id","name")
    context = {"categorylist":clist}
    return render(request, "users/Ingredients/add.html", context)

def insert(request):
    try:
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            return HttpResponse("No Cover Picture Information!")
        cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/uploads/Ingredients/"+cover_pic,"wb+")
        for chunk in myfile.chunks():   
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

def delete(request, pid = 0):
    try:
        ob = Ingredients.objects.get(id=pid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Deleted!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Delete!"}
    
    return render(request, "users/info.html",context)

def edit(request, pid = 0):
    try:
        ob = Ingredients.objects.get(id=pid)
        clist = Category.objects.values("id","name")
        context = {'Ingredients':ob,"categorylist":clist}
        return render(request, "users/Ingredients/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Information Not Found!"}
        return render(request, "users/info.html",context)

def update(request, pid = 0):
    try:
        ob = Ingredients.objects.get(id=pid)
        # ob.Recipe_id_id = request.POST['Recipe_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.calories = request.POST['calories']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        oldpicname = request.POST['oldpicname']
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            cover_pic = oldpicname
        else:    
            cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
            destination = open("./static/uploads/Ingredients/"+cover_pic,"wb+")
            for chunk in myfile.chunks():  
                destination.write(chunk)  
            destination.close()

        ob.cover_pic = cover_pic
        ob.save()
        context = {'info':"Updated Successfully!"}

        if myfile:
            os.remove("./static/uploads/Ingredients/"+oldpicname)

    except Exception as err:
        print(err)
        context = {'info':"Fail to Update!"}

        if myfile:
            os.remove("./static/uploads/Ingredients/"+cover_pic)
    
    return render(request, "users/info.html",context)