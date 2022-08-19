from django.shortcuts import render

from . import util
import markdown
import random

entries_list = util.list_entries()

def index(request):
    update_entries_list()
    return render(request, "encyclopedia/index.html", {
        'entries':entries_list
    })

def update_entries_list():
    global entries_list
    entries_list = util.list_entries()

def entry(request, title):
    update_entries_list()
    if title not in entries_list:
        return render(request, "encyclopedia/not_found.html")
    else:
        html = md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            'entry':html,
            'entry_title':title,
        })

def md_to_html(title):
    entry_to_convert = util.get_entry(title)
    return markdown.markdown(entry_to_convert)

def search(request):
    update_entries_list()
    results = []
    if request.method == 'GET':
        input_search = request.GET['q']

        for e in entries_list:
            if input_search.upper() == e.upper():
                return entry(request,e)

            elif input_search.upper() in e.upper():
                results.append(e)
                
        if results:
            return render(request, "encyclopedia/search.html", {
                "results":results
            })
        else:
            return render(request, "encyclopedia/not_found.html")

def new_entry(request):
    return render(request, "encyclopedia/new_entry.html")

def save_new_entry(request):
    update_entries_list()
    if request.method == "POST":
        new_entry_title = request.POST['entry_title']
        new_entry_content = request.POST['content']
        for e in entries_list:
            if new_entry_title.upper() == e.upper():
                return render(request, "encyclopedia/already_exists.html")
            else:
                util.save_entry(new_entry_title, new_entry_content)
                update_entries_list()
                return entry(request, new_entry_title)
      
def edit_entry(request):
    title = request.POST.get('entry_title')
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit_entry.html", {
        'entry_title':title,
        'content':content
    })

def save_edit(request):
    if request.method == "POST":
        entry_title = request.POST['entry_title']
        entry_content = request.POST['content']
        util.save_entry(entry_title, entry_content)
        update_entries_list()
        return entry(request, entry_title)

def random_entry(request):
    update_entries_list()
    return entry(request, random.choice(entries_list))