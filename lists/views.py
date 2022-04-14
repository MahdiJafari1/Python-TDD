from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse

from lists.models import Item, List


def home_page(request):
    return render(request, "home.html")


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST["item_text"], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        return render(request, "home.html", {"error": "You cannot have an empty list item"})
    return redirect(reverse("view_list", args=[list_.id]))


def add_item(request, id):
    list_ = List.objects.get(id=id)
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(reverse("view_list", args=[list_.id]))


def view_list(request, id):
    list_ = List.objects.get(id=id)
    if request.method == 'POST':
        item = Item(text=request.POST["item_text"], list=list_)
        return redirect(reverse("view_list"))
    return render(request, "list.html", {"list": list_})

    try: 
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        return render(request, "home.html", {"error": "You cannot have an empty list item"}) 
