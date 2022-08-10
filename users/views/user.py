from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from users.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import time, os

def edit(request, user_id = 0):
    try:
        ob = User.objects.get(id=user_id)
        context = {'user':ob}
        return render(request, "users/user/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Information Not Found!"}
        return render(request, "users/info.html",context)

def doedit(request, user_id = 0):
    try:
        ob = User.objects.get(id=user_id)

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
            destination = open("./static/uploads/Users/"+avatar_pic,"wb+")
            for chunk in pic_file.chunks():  
                destination.write(chunk)  
            destination.close()

        ob.avatar_pic = avatar_pic

        ob.save()

        ob = User.objects.get(id=user_id)
        request.session['user'] = ob.toDict()

        context = {'info':"Sucessfully Editted!"}

        if pic_file and oldpicname != 'avatar5.png':
            os.remove("./static/uploads/Users/"+oldpicname)

    except Exception as err:
        print(err)
        context = {'info':"Fail to Edit!"}

        if pic_file and oldpicname != 'avatar5.png':
            os.remove("./static/uploads/Users/"+oldpicname)
    
    return render(request, "users/info.html",context)