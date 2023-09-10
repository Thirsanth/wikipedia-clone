from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.entries,name="entries"),
    path("search/",views.entry_search,name="entry_search"),
    path("new/",views.new_entry,name="new_entry"),
    path("edit/",views.edit_page,name="edit_page"),
    path("save/",views.save_edit,name="save_edit"),
    path("random/",views.random_page,name="random_page")
]
