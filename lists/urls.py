from django.urls import path

from lists import views

urlpatterns = [
    path("new", views.new_list, name="new_list"),
    path("<int:id>", views.view_list, name="view_list"),
    path("<int:id>/add_item", views.add_item, name="add_item"),
]
