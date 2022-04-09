from django.shortcuts import render, redirect, get_object_or_404
from .form import UserRegisterForm, UserLoginForm
from .decorator import isunthenticated
from realEstate.forms import AgentForm
from realEstate.models import Agent, Images

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)


# Create your views here.
@isunthenticated
def login_view(request):

    next_ = request.GET.get("next")
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)

        if next_:
            return redirect(next_)
        return redirect(to='Home')

    context = {
        "form": form
    }
    return render(request, "login.html", context=context)

@isunthenticated
def register_view(request):
    next_ = request.GET.get("next")
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.username = email
        user.save()
        new_agent = Agent.objects.create(user = user)
        new_agent.save()
        #new_user = authenticate(username= username, password=password)
        login(request, user)
        if next_:
            return redirect(next_)
        return redirect("profile")
    context = {
        "form":form

    }
    return render(request, "register.html", context=context)


def logout_view(request):
    logout(request)
    return redirect("login")

def profile_create(request):
    user = get_object_or_404(Agent, id= request.user.agent.id)
    if request.method == "POST":
        form = AgentForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("Home")
    form = AgentForm(instance=user)

    context = {
        "form":form
    }
    return render(request, "profile.html", context=context)

