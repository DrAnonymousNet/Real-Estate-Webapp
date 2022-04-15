from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, Agent, House, Land, Amenity, Images
from .filter import HouseFilter
from .forms import HouseForm, ImageForm, Image_formset, Amenity_formset
from django import forms
from .decorator import is_author
from django.http import HttpResponse
from django.core.paginator import Paginator


# Create your views here.

def paginate(queryset, num, page_num):
    paginator = Paginator(queryset, num)
    current_page = paginator.page(page_num)
    paginated_queryset = current_page.object_list

    return paginator, paginated_queryset, current_page


def Home(request):
    featured_house = House.objects.filter(featured=True)
    featured_agent = Agent.objects.filter(featured=True)
    latest_property = House.objects.filter(date_listed__isnull=False)[:20]
    filtered = HouseFilter()

    context = {
        "featured_house": featured_house,
        "featured_agent": featured_agent,
        "latest_house": latest_property,
        "filtered": filtered
    }
    return render(request, "index.html", context)


def property_list(request):
    p_list = House.objects.filter(date_listed__isnull=False)
    filtered = HouseFilter()

    page_num = request.GET.get("page")
    if not page_num:
        page_num = 1
    paginator, paginated_qs, current_page = paginate(p_list, 3, page_num)
    context = {
        "filtered": filtered,
        "current_page": current_page,
        "properties": paginated_qs,
        "page_num": page_num,
        "paginator":paginator
    }
    return render(request, "property_list.html", context=context)


def agent_list(request):
    agents = Agent.objects.all()
    filtered = HouseFilter()

    page_num = request.GET.get("page")
    if not page_num:
        page_num = 1
    paginator, paginated_qs, current_page = paginate(agents, 3, page_num)
    context = {
        "filtered": filtered,
        "current_page": current_page,
        "agents": paginated_qs,
        "page_num": page_num,
        "paginator": paginator,
    }
    return render(request, "agent_list.html", context)


def property_detail(request, id):
    property = House.objects.get(pk=id)
    ag = property.agent.id
    agent = Agent.objects.get(pk=ag)
    filtered = HouseFilter()
    context = {
        "property": property,
        "agent": agent,
        "filtered": filtered
    }
    return render(request, "property_detail.html", context)


def agent_property_list(request, id):
    agent = Agent.objects.get(id=id)
    properties = House.objects.filter(agent__id=id)
    filtered = HouseFilter()

    page_num = request.GET.get("page")
    if not page_num:
        page_num = 1
    paginator, paginated_qs, current_page = paginate(properties, 2, page_num)
    context = {
        "filtered": filtered,
        "current_page": current_page,
        "agents": paginated_qs,
        "page_num": page_num,
        "paginator": paginator,
        "agent":agent,
        "id":id,
        "agent_properties": paginated_qs

    }


    return render(request, "agent_property_list.html", context)


def property_create(request):
    form_1 = HouseForm(request.POST or None)
    form_2 = Amenity_formset(request.POST or None, prefix="amenity", queryset=Amenity.objects.none())
    form_3 = Image_formset(request.POST or None, request.FILES or None, prefix="image", queryset=Images.objects.none())
    filtered = HouseFilter()
    if form_1.is_valid() and form_2.is_valid() and form_3.is_valid():
        form_1.instance.agent = request.user.agent
        # empty = [ field for field in form_2.cleaned_data if field == None ]
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

            qs = House.objects.get(id=form_1.instance.id)
            form.instance.house = qs
            form.save()

        return redirect("property_detail", id=form_1.instance.id)
    context = {
        "form": form_1,
        "form_2": form_2,
        "form_3": form_3,
        "filtered": filtered
    }

    return render(request, "property_create.html", context=context)


@is_author
def property_edit(request, id):
    property = get_object_or_404(House, id=id)
    form_1 = HouseForm(instance=property)
    form_2 = Amenity_formset(prefix="amenity", queryset=property.amenity.all())
    form_3 = Image_formset(prefix="image", queryset=property.images_set.all(), instance=property)
    filtered = HouseFilter()

    if request.method == "POST":
        form_1 = HouseForm(request.POST, request.FILES, instance=property)
        form_2 = Amenity_formset(request.POST, prefix="amenity")
        form_3 = Image_formset(request.POST, request.FILES, prefix="image", instance=property)
        if form_1.is_valid() and form_2.is_valid() and form_3.is_valid():
            form_1.save()
            form_2.save()
            qs = House.objects.get(id=form_1.instance.id)
            for form in form_2:
                if form in form_2.deleted_forms or not form["name"].value():
                    continue
                form.save()

                qs.amenity.add(form.instance)
                qs.save()

            for form in form_3:

                if form in form_3.deleted_forms or not form["picture"].value():
                    print(form.instance)

                    if form["picture"].value() and form.instance in Images.objects.all():
                        Images.objects.get(picture=form.instance).delete()
                    continue
                form.save()
                qs.images_set.add(form.instance)

        return redirect("property_detail", id=id)

    context = {
        "form": form_1,
        "form_2": form_2,
        "form_3": form_3,
        "filtered": filtered
    }

    return render(request, "property_edit.html", context=context)


@is_author
def property_delete(request, id):
    property = get_object_or_404(House, id=id)
    filtered = HouseFilter()

    if request.method == "POST":
        property.delete()
        return redirect("agent_property_list", id=request.user.id)
    context = {
        "property": property,
        "filtered": filtered
    }
    return render(request, "property_confirm_delete.html", context=context)


def search_view(request):
    filtered = HouseFilter(request.GET, queryset=House.objects.all())

    context = {
        "filtered": filtered
    }

    return render(request, "search_result.html", context=context)
