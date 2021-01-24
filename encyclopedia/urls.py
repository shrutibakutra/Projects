from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/keyword",views.search,name="search"),
    path("<str:title>",views.content , name="content"),
    path("t/addnew",views.addnew , name = "addnew"),
    path("edit/<str:title>", views.edit , name = "edit"),
    path("page/random/", views.random_page, name="random_page"),    
]
