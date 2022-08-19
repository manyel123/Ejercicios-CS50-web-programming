from django.shortcuts import render

from . import util
import markdown
import random

entries_list = util.list_entries()
upper_entries_list = []

# this function will return a list of all entries
def index(request):
    # updating this list will always display an updated list of entries at home page
    update_entries_list()
    # return the request, the html to render, and the context for the html
    # the context will pass the entries_list as "entries" to index.html 
    return render(request, "encyclopedia/index.html", {
        # context for index.html
        'entries':entries_list
    })

# when called, this function will update the entries list
def update_entries_list():
    global entries_list
    entries_list = util.list_entries()

# when called, this function will update all upper entries
def update_upper_entries_list():
    update_entries_list()
    global upper_entries_list
    for e in entries_list:
        upper_entries_list.append(e.upper())

# this function will return a particular entry
def entry(request, title):
    update_upper_entries_list()
    # if the entry title given doesn't exists a "not found" page will be displayed,
    # title and entries list are compared in uppercase for displaying an entry
    # no matter the input format in the link
    if title.upper() not in upper_entries_list:
        return render(request, "encyclopedia/not_found.html")
    # if the given entry exist it will be displayed
    else:
        # before displaying an entry it needs to be converted from markdown to html
        # using the function md_to_html
        html = md_to_html(title)
        # return the entry.html with the "title" and html(entry converted to html) as context
        return render(request, "encyclopedia/entry.html", {
            # html is the body to be displayed at entry.html
            'entry':html,
            # title is the entry_title to be displayed at entry.html
            'entry_title':title,
        })

# function to convert markdown into html
def md_to_html(title):
    entry_to_convert = util.get_entry(title)
    return markdown.markdown(entry_to_convert)

# function for searching entries
def search(request):
    update_entries_list()
    # this list will save the search resutls
    results = []
    if request.method == 'GET':
        # get the search input into "input_search"
        input_search = request.GET['q']
        # this loop will convert input_search and all entries into uppercase 
        for e in entries_list:
            # if there is an exact match it will be rendered using the entry function
            if input_search.upper() == e.upper():
                return entry(request,e)
            # if there is an entry containing the value given in input_search it will be append to results
            elif input_search.upper() in e.upper():
                results.append(e)
        # if there is no exact match, a page with similar results will be displayed, if there's are any        
        if results:
            return render(request, "encyclopedia/search.html", {
                "results":results
            })
        # if there is no similar results a "not found" page will be displayed
        else:
            return render(request, "encyclopedia/not_found.html")

# function for rendering the new_entry page
def new_entry(request):
    return render(request, "encyclopedia/new_entry.html")

# function for saving the new entry given at new_entry.html form
def save_new_entry(request):
    # updating the entries list before saving a new entry
    update_entries_list()
    if request.method == "POST":
        # getting the title and entry content from the request
        new_entry_title = request.POST['entry_title']
        new_entry_content = request.POST['content']
        # checking if the new entry already exist
        for e in entries_list:
            # if the new entry already exists, an "already_exists" page will be displayed
            if new_entry_title.upper() == e.upper():
                return render(request, "encyclopedia/already_exists.html")
            # if the new entry doesn't exist:
            else:
                # it will be saved
                util.save_entry(new_entry_title, new_entry_content)
                # then the entries list will be updated again
                update_entries_list()
                # and the new page will be rendered making use of the entry function
                return entry(request, new_entry_title)

# this function will get the entry information from the "entry page"
# and will fill the form in "edit_entry.html"   
def edit_entry(request):
    # get the title from the current entry
    title = request.POST.get('entry_title')
    # get the content from the current entry in markdown format
    content = util.get_entry(title)
    # return the "edit entry" page with the form filled
    return render(request, "encyclopedia/edit_entry.html", {
        'entry_title':title,
        'content':content
    })

# function for saving the edited page
def save_edit(request):
    if request.method == "POST":
        # getting entry info to be saved
        entry_title = request.POST['entry_title']
        entry_content = request.POST['content']
        # saving the edited entry
        util.save_entry(entry_title, entry_content)
        # updating the entries list
        update_entries_list()
        # render the edited entry making use of "entry" function
        return entry(request, entry_title)

# fuction that will return a random entry
def random_entry(request):
    update_entries_list()
    # chooses a random entry in entries_list to be displayed
    return entry(request, random.choice(entries_list))