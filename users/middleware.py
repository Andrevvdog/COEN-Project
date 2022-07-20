#执行登录判断
from django.shortcuts import redirect
from django.urls import reverse
import re

class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        print("MiddleWare")

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        path = request.path
        print("url: ", path)

        urllist = ['/users/login', '/users/dologin', '/users/logout', '/users/verify', '/users/register', '/users/doregister']
        if re.match(r'^/users', path) and (path not in urllist):
            if 'adminuser' not in request.session:
                return redirect(reverse("users_login"))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response