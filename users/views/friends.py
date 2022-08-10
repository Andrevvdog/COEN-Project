from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from users.models import User, Friends
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import time, os

def viewfriends(request, pIndex = 1):
    friends = Friends.objects
    filter_list = friends.filter(status__lt=9, user_id=request.session['user']['id'])
    mywhere = []
    keyword = request.GET.get("keyword",None)
    if keyword:
        filter_list = filter_list.filter(Q(nickname__contains=keyword) | Q(email__contains=keyword))
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
    friends_list = page.page(pIndex)
    plist = page.page_range

    context = {"friendslist":friends_list, 'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    
    return render(request, "users/friends/viewfriends.html",context)


def add(request):
    return render(request, "users/friends/add.html")


def doadd(request):
    try:
        pic_file = request.FILES.get("avatar_pic",None)
        if not pic_file:
            context = {'info':"No Cover Picture Information!"}
            return render(request, "users/info.html",context)
        avatar_pic = str(time.time())+"."+pic_file.name.split('.').pop()
        destination = open("./static/uploads/Friends/"+avatar_pic,"wb+")
        for chunk in pic_file.chunks():   
            destination.write(chunk)  
        destination.close()

        ob = Friends()
        ob.user_id = request.session['user']['id']
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        ob.email = request.POST['email']
        ob.avatar_pic = avatar_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Added!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Add!"}
    
    return render(request, "users/info.html",context)


def delete(request, friends_id = 0):
    try:
        ob = Friends.objects.get(id=friends_id)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Deleted!"}
    except Exception as err:
        print(err)
        context = {'info':"Fail to Delete!"}
    
    return render(request, "users/info.html",context)

def edit(request, friends_id = 0):
    try:
        ob = Friends.objects.get(id=friends_id)
        context = {'friend':ob}
        return render(request, "users/friends/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Information Not Found!"}
        return render(request, "users/info.html",context)

def doedit(request, friends_id = 0):
    try:
        ob = Friends.objects.get(id=friends_id)
        if request.POST['nickname']:
            ob.nickname = request.POST['nickname']
        if request.POST['email']:
            ob.email = request.POST['email']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        oldpicname = request.POST['oldpicname']
        pic_file = request.FILES.get("avatar_pic",None)
        if not pic_file:
            avatar_pic = oldpicname
        else:    
            avatar_pic = str(time.time())+"."+pic_file.name.split('.').pop()
            destination = open("./static/uploads/Friends/"+avatar_pic,"wb+")
            for chunk in pic_file.chunks():  
                destination.write(chunk)  
            destination.close()
            
        ob.avatar_pic = avatar_pic
        ob.save()
        context = {'info':"Updated Successfully!"}

        if pic_file:
            os.remove("./static/uploads/Friends/"+oldpicname)

    except Exception as err:
        print(err)
        context = {'info':"Fail to Update!"}

        if pic_file:
            os.remove("./static/uploads/Friends/"+avatar_pic)
    
    return render(request, "users/info.html",context)
