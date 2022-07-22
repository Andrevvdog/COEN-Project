from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from users.models import User, Friends
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import time, os

def viewfriends(request, pIndex=1):
    friends = Friends.objects
    filter_list = friends.filter(status__lt=9, user__lt=(User.objects.get(name=(request.session['user']['id'])).id))
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
    page = Paginator(filter_list, 10)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    friends_list = page.page(pIndex)
    plist = page.page_range

    context = {"friendslist":friends_list, 'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    
    return render(request, "users/friends/viewfriends.html",context)