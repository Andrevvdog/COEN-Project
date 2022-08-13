from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from users.models import User
from django.shortcuts import redirect
from django.urls import reverse
import re
from datetime import datetime
import os
import hashlib
from captcha.image import ImageCaptcha
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
import io

def verify(request):
    number = ['0','1','2','3','4','5','6','7','8','9']
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    captcha_text = []
    char_set=number+alphabet
    for i in range(4):
        c = random.choice(char_set)
        captcha_text.append(c)

    image = ImageCaptcha()
 
    captcha_text = ''.join(captcha_text)
    captcha = image.generate(captcha_text)

    captcha_image = Image.open(captcha).resize((150, 35),resample=0)
    buffer = io.BytesIO()
    captcha_image.save(buffer, 'png')
    print(captcha_text)

    request.session['verifycode'] = str(captcha_text)

    return HttpResponse(buffer.getvalue(), 'image/png')

def register(request):
    return render(request, 'users/webindex/register.html')

def doregister(request):
    try:
        if request.POST['code'] != request.session['verifycode']:
            context = {"info":"Wrong Verification Code！"}
            return render(request, "users/webindex/register.html", context)
        user_list = User.objects.filter(username=request.POST['username'])
        if len(user_list) == 0:
            ob = User()
            ob.email = request.POST['email']
            ob.username = request.POST['username']
            ob.nickname = request.POST['nickname']
            ob.avatar_pic = "avatar5.png"
            if (request.POST['password'] == request.POST['repassword']):
                import hashlib, random
                md5 = hashlib.md5()
                n = random.randint(100000, 999999)
                s = request.POST['password'] + str(n)
                md5.update(s.encode('utf-8'))
                ob.password_hash = md5.hexdigest()
                ob.password_salt = n
                ob.status = 1
                ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ob.save()
                context = {'info':"Sucessfully Registered!"}

                return render(request, "users/webindex/login.html", context)
            
            else:
                context = {"info":"Invalid Password！"}
        else:
            context = {"info":"Username Already Exists！"}
    except Exception as err:
        print(err)
        context = {"info":"Unknown Error!"}
    return render(request, "users/webindex/register.html", context)

def webindex(request):
    return render(request, 'users/webindex/webindex.html')

def login(request):
    return render(request, 'users/webindex/login.html')

def dologin(request):
    try:
        if request.POST['code'] != request.session['verifycode']:
            context = {"info":"Wrong Verification Code！"}
            return render(request, "users/webindex/login.html", context)
        user = User.objects.get(username=request.POST['username'])
        if user.status == 1:
            md5 = hashlib.md5()
            s = request.POST['pass'] + user.password_salt
            md5.update(s.encode('utf-8'))
            if user.password_hash == md5.hexdigest():
                request.session['user'] = user.toDict()
                request.session['rbid'] = 0
                request.session['cid'] = 0
                return redirect(reverse("users_webindex"))
            else:
                context = {"info":"Wrong Password！"}

        else:
            context = {"info":"Invalid User！"}
    except Exception as err:
        print(err)
        context = {"info":"Account Not Exists!"}
    return render(request, "users/webindex/login.html", context)

def logout(request):
    del request.session['user']
    del request.session['rbid']
    del request.session['cid']
    return redirect(reverse("users_login"))



