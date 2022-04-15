from .filter import HouseFilter
from .models import House
from django.http import HttpResponseForbidden

def add_search(func):
    def wrapper(request, *args, **kwargs):
        filtered = HouseFilter()
        #context["filtered"] = filtered

        return func(request,*args, **kwargs)
    return wrapper

def is_author(func):
    def wrapper(request, id, *args, **kwargs):
        agent = House.objects.get(pk = id)
        if request.user != agent.agent.user:
            return HttpResponseForbidden()
        else:
            return func(request, id, *args, **kwargs)

    return wrapper
