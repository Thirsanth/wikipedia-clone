from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.http import HttpResponse
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def markdown_to_html(title):
    content=util.get_entry(title)
    markdowner=Markdown()
    if content==None:
        return None
    else:
        return markdowner.convert(content)

def entries(request,title):
    entry_request=markdown_to_html(title)
    if entry_request==None:
        return render(request,"encyclopedia/error.html",{
            "message":"The requested page "+title+" does not exist"
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content":entry_request
        })

def entry_search(request):
    if request.method=="POST":
        search_request=request.POST['q']
        html_content=markdown_to_html(search_request)
        if html_content is not None:  
            return render(request,"encyclopedia/entry.html",{
            "title":search_request,
            "content":html_content
        })
        else:
            all_entries=util.list_entries()
            substring_recomendation=[]
            search_lower=search_request.lower()
            for s in all_entries:
                s_list=s.lower()
                if search_lower in s_list:
                    substring_recomendation.append(s_list)
            return render(request,"encyclopedia/search.html",{
                "recomendation":substring_recomendation
            })
           
def new_entry(request):
    if request.method=="GET":
        return render(request,"encyclopedia/new.html")
    else:
        title=request.POST['title']
        content=request.POST['content']
        get_title=util.get_entry(title)
        if get_title is not None:
            return render(request,"encyclopedia/error.html",{
                "message":title+" page already exist"
            })
        else:
            util.save_entry(title,content)
            html_content=markdown_to_html(title)
            return render(request,"encyclopedia/entry.html",{
                "title":title,
                "content":html_content
            })
def edit_page(request):
    if request.method=="POST":
        get_title=request.POST['title']
        html_content=util.get_entry(get_title)
        return render(request,"encyclopedia/edit.html",{
            "title":get_title,
            "content":html_content
        })
    else:
        return render(request,"encyclopedia/error.html",{
            "message":"An error occured while editing the page."
        })

def save_edit(request):
    if request.method=="POST":
        title=request.POST['title']
        content=request.POST['content']
        util.save_entry(title,content)
        html_content=markdown_to_html(title)
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content":html_content
        })
    else:
        return render(request,"encyclopedia/error.html",{
            "message":"An error occured while saving the edited page."
        })
def random_page(request):
    get_entries=util.list_entries()
    if get_entries is not None:
        random_entry=random.choice(get_entries)
        html_content=markdown_to_html(random_entry)
        return render(request,"encyclopedia/entry.html",{
            "title":random_entry,
            "content":html_content
        })
    else:
        return render(request,"encyclopedia/error.html",{
            "message":"An error occured while displaying an random page"
        })

