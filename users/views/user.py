from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from users.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import time, os

def edit(request, uid = 0):
    try:
        ob = User.objects.get(id=uid)
        context = {'user':ob}
        return render(request, "users/user/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Information Not Found!"}
        return render(request, "users/info.html",context)

def update(request, uid = 0):
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST['nickname']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.email = request.POST['email']

        oldpicname = request.POST['oldpicname']
        myfile = request.FILES.get("avatar_pic",None)
        if not myfile:
            avatar_pic = oldpicname
        else:    
            avatar_pic = str(time.time())+"."+myfile.name.split('.').pop()
            destination = open("./static/uploads/Users/"+avatar_pic,"wb+")
            for chunk in myfile.chunks():  
                destination.write(chunk)  
            destination.close()

        ob.avatar_pic = avatar_pic

        ob.save()

        ob = User.objects.get(id=uid)
        request.session['adminuser'] = ob.toDict()

        context = {'info':"Sucessfully Editted!"}

        if myfile and oldpicname != 'avatar5.png':
            os.remove("./static/uploads/Users/"+oldpicname)

    except Exception as err:
        print(err)
        context = {'info':"Fail to Edit!"}

        if myfile and oldpicname != 'avatar5.png':
            os.remove("./static/uploads/Users/"+oldpicname)
    
    return render(request, "users/info.html",context)