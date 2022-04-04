from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item


def home_page(request):

    if request.method == "POST":
        new_item_text = request.POST["item_text"]
        Item.objects.create(text=new_item_text)
        return redirect("/")
    items = Item.objects.all()

    return render(request, "home.html", {"items": items})
