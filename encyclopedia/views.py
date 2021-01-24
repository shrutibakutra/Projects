from django.shortcuts import render, HttpResponseRedirect,get_object_or_404
from . import util
from django import forms
import random
from django.urls import reverse
import re
from markdown2 import Markdown

markdowner = Markdown()


class addencyclopedia(forms.Form):
    title = forms.CharField(label="new title",widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}) ,label="new content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def content(request, title):
    title = title
    files = util.list_entries()
    content = util.get_entry(title)
    page_converted = markdowner.convert(content)
    if title in files:
        return render(request, "encyclopedia/content.html", {
            "content": page_converted,
            "title": title
        })
    else:
        return render(request , "encyclopedia/error.html" , {
            "error":"Sorry! page not found!"
        })


def addnew(request):
    if request.method == 'POST':
        form = addencyclopedia(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if title not in util.list_entries():
                util.save_entry(title, content)                 
                return render(request,"encyclopedia/content.html", {
                    "title":(title),
                    "content":markdowner.convert(content)           
                    })
            else:
                return render(request,"encyclopedia/error.html",
                { "error":"Page with this title already exists! Please try with another Title :)"}
                )
        else:
            return render(request, "encyclopedia/addnew.html", {
                "form": form,
            })
    return render(request, "encyclopedia/addnew.html", {
        "form": addencyclopedia(),
    })


def edit(request,title):
    entry = util.get_entry(title)
    if(request.method == 'POST'):     
        form = addencyclopedia(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title,content)
            return render(request,"encyclopedia/content.html",{
                "content":markdowner.convert(content),
                "title":title
            }) 
    else:
        form = addencyclopedia(initial={"content":entry, "title":title})
        return render(request,"encyclopedia/edit.html",{
            "form":form
            })


def random_page(request):
    entries = util.list_entries()
    selected_page = random.choice(entries)
    return render(request, "encyclopedia/content.html", {
        "content": markdowner.convert(util.get_entry(selected_page.capitalize())),
        "title": selected_page
        })

def search(request):
    search_term = ""
    files = util.list_entries()    
    if 'search' in request.GET:
        search_term = request.GET['search']
        if search_term.capitalize() in files:
            return render(request, "encyclopedia/content.html", {
                    "content": markdowner.convert(util.get_entry(search_term.capitalize())),
                    "title":(search_term)
            })
        else:
    
            return render(request , "encyclopedia/index.html",
            {'entries': files})    