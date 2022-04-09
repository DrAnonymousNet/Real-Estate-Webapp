from django.shortcuts import render,redirect
from realEstate.models import House
from django.http import HttpResponseForbidden

def isunthenticated(func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            return redirect("Home")
        return func(request, *args,**kwargs)
    return wrapper_func

def is_author(func):
    def wrapper(request, id, *args, **kwargs):
        agent = House.objects.get(pk = id)
        if request.user != agent.agent.user:
            return HttpResponseForbidden()
        else:
            return func(request, id, *args, **kwargs)

    return wrapper