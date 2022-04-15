from django.forms import ValidationError
from django.shortcuts import redirect, render

from lists.models import Item, List


def home_page(request):
    return render(request, "home.html")


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST["item_text"], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        return render(
            request, "home.html", {"error": "You cannot have an empty list item"}
        )
    return redirect(list_)


def view_list(request, id):
    list_ = List.objects.get(id=id)
    if request.method == "POST":
        try:
            item = Item(text=request.POST["item_text"], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You cannot have an empty list item"
            return render(request, "list.html", {"list": list_, "error": error})

    return render(request, "list.html", {"list": list_})
