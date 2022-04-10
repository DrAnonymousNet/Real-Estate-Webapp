from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, Agent, House, Land, Amenity, Images
from .filter import HouseFilter
from .forms import HouseForm, ImageForm, Image_formset, Amenity_formset
from django.forms import modelformset_factory
from account.decorator import is_author


# Create your views here.

def Home(request):
    featured_house = House.objects.filter(featured=True)
    featured_agent = Agent.objects.filter(featured=True)
    latest_property = House.objects.filter(date_listed__isnull=False)[:20]
    if request.method == "POST":
        filtered = HouseFilter(request.GET, queryset=House.objects.all())
        context = {
            "filter": filtered
        }

        return render(request, "search_result.html", context=context)

    context = {
        "featured_house": featured_house,
        "featured_agent": featured_agent,
        "latest_house": latest_property,


    }
    return render(request, "index.html", context)


def property_list(request):
    p_list = House.objects.filter(date_listed__isnull=False)
    context = {"properties": p_list}
    return render(request, "property_list.html", context=context)


def agent_list(request):
    agents = Agent.objects.all()

    context = {
        "agents": agents
    }
    return render(request, "agent_list.html", context)


def property_detail(request, id):
    property = House.objects.get(pk=id)
    ag = property.agent.id
    agent = Agent.objects.get(pk=ag)
    context = {
        "property": property,
        "agent": agent
    }
    return render(request, "property_detail.html", context)


def agent_property_list(request, id):
    agent = Agent.objects.get(id=id)
    properties = House.objects.filter(agent__id=id)

    context = {
        "agent": agent,
        "agent_properties": properties,
        "id":id
    }
    return render(request, "agent_property_list.html", context)


def property_create(request):
    form_1 = HouseForm(request.POST or None)
    form_2 = Amenity_formset(request.POST or None, prefix="amenity", queryset = Amenity.objects.none())
    form_3 = Image_formset(request.POST or None, request.FILES or None, prefix="image", queryset = Images.objects.none())
    if form_1.is_valid() and form_2.is_valid() and form_3.is_valid():
        form_1.instance.agent = request.user.agent
        #empty = [ field for field in form_2.cleaned_data if field == None ]
        form_1.save()
        form_2.save()
        for form in form_2:
            form.save()
            qs = House.objects.get(id=form_1.instance.id)
            qs.amenity.add(form.instance)
            qs.save()
        for form in form_3:
            if form in form_3.deleted_forms or not form["picture"].value():
                continue
            form.save()
            qs = House.objects.get(id=form_1.instance.id)
            qs.image.add(form.instance)
            qs.save()

        return redirect("property_detail", id = form_1.instance.id)
    context = {
        "form": form_1,
        "form_2": form_2,
         "form_3":form_3}

    return render(request, "property_create.html", context=context)

@is_author
def property_edit(request, id):

    property = get_object_or_404(House, id = id)
    form_1= HouseForm(instance=property)
    form_2 = Amenity_formset(prefix="amenity", queryset = property.amenity.all())
    form_3 = Image_formset(prefix="image", queryset=property.image.all())

    if request.method == "POST":
        form_1= HouseForm(request.POST, request.FILES, instance=property)
        form_2 = Amenity_formset(request.POST or None, prefix="amenity")
        form_3 = Image_formset(request.POST , request.FILES, prefix="image")
        if form_1.is_valid() and form_2.is_valid() and form_3.is_valid():
            form_1.save()
            form_2.save()
            for form in form_2:
                if form in form_2.deleted_forms or not form["name"].value():
                    continue
                form.save()
                qs = House.objects.get(id=form_1.instance.id)
                qs.amenity.add(form.instance)
                qs.save()
            for form in form_3:
                if form in form_3.deleted_forms or not form["picture"].value():
                    continue
                form.save()
                qs = House.objects.get(id=form_1.instance.id)
                qs.image.add(form.instance)
                qs.save()
        return redirect("property_detail", id=id)

    context = {
        "form": form_1,
        "form_2": form_2,
         "form_3":form_3
    }

    return render(request, "property_edit.html", context=context)

@is_author
def property_delete(request, id):
    property = get_object_or_404(House, id=id)

    if request.method == "POST":
        property.delete()
        return redirect("agent_property_list", id=request.user.id)
    context = {
        "property":property
    }
    return render(request, "property_confirm_delete.html", context=context)

def search_view(request):
    filtered = HouseFilter(request.GET, queryset=House.objects.all())
    context = {
        "filter":filtered
    }

    return render(request, "search_result.html", context=context)