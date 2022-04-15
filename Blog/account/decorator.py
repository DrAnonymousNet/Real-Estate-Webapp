from django.shortcuts import render,redirect


def isunthenticated(func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            return redirect("Home")
        return func(request, *args,**kwargs)
    return wrapper_func


