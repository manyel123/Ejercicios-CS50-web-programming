from asyncio.windows_events import NULL
from django.shortcuts import render

# importing the function Marcdown() whick converts md to html
from markdown2 import Markdown
markdowner = Markdown()

from . import util

import markdown

import random

# rendering the home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# converting a markdown into html by its name
def convert_to_html(entry_name):
    entry_to_convert = util.get_entry(entry_name)
    if entry_to_convert != None:
        entry_converted_to_html = markdown.markdown(entry_to_convert)
    else:
        return None
    return entry_converted_to_html

# defining an entry with its name as parameter
def entry(request, title):
    # gets the markdown from entries using get_entry function from utils
    markdown_entry = util.get_entry(title)

    # checks if entry_name exist
    if markdown_entry is None:
        # if not return the not found entry page
        return render(request, "encyclopedia/not_found_entry.html", {
            # uses entry_name as tittle for rendering at non_found_entry.html
            "entry_title": title 
        })
    else:
        # if found, return the converted md into entry.html for rendering
        return render(request, "encyclopedia/entry.html", {
            "entry": convert_to_html(title),
            # and page title as title
            "entry_title": title
        })

# defining a search function which must look for an entry and then renders it
def search(request):
    if request.method == 'GET':
        # catches the request into input
        search_input = request.GET.get('q')

        # converting the entry into html
        search_html = convert_to_html(search_input)

        # getting the list of all entries to compare them with the input
        entries = util.list_entries()

        # list of entries that match with input
        found_entries = []

        # loop for looking if input is included in entries also normalizes the search
        for entry in entries:
            if search_input.upper() in entry.upper():
                found_entries.append(entry)
        
        # loop for rendering an specific entry from found_entries
        for entry in entries:
            # if input equals an entry it will be rendered
            if search_input.upper() == entry.upper():
                return render(request, "encyclopedia/entry.html", {
                    "entry": search_html,
                    "entry_title": search_input
                })
            
            # if does not found exact same entry it will list all found entries
            elif found_entries != []:
                return render(request, "encyclopedia/entry.html", {
                    "entries": found_entries
                })

            # if no entries were found
            else:
                return render(request, "encyclopedia/not_found_entry.html", {
                    "entry_title": search_input
                })

# for rendering the new entry page
def new_entry(request):
    return render(request, "encyclopedia/new_entry.html")

# for saving the new entry
def save_new_entry(request):
    if request.method == 'POST':
        # new entry inputs
        input_title = request.POST['entry_title']
        input_content = request.POST['entry_content']

        # title for new entry
        new_entry_html = convert_to_html(input_title)

        # entries list for checking if new entry already exists
        entries = util.list_entries()
        already_existing_entry = False
        
        # validates if new entry already exists
        for entry in entries:
            if input_title.upper() == entry.upper():
                already_existing_entry = True

        # if new entry already exists
        if already_existing_entry == True:
            return render(request, "encyclopedia/already_existing_entry.html", {
                "entry": new_entry_html,
                "entry_title": input_title
            })
        
        # if new entry does not exist
        else:
            util.save_entry(input_title, input_content)
            return render(request, "encyclopedia/entry.html", {
                "entry": convert_to_html(input_title),
                "entry_title": input_title
            })

# getting a random entry
def random_entry(request):
    entries = util.list_entries()
    random_ent = random.choice(entries)

    random_entry_html = convert_to_html(random_ent)

    return render(request, "encyclopedia/entry.html", {
        "entry": random_entry_html,
        "entry_title": random_ent
    })

# editing an entry
def edit_entry(request):
    if request.method == 'POST':

        input_title = request.POST['title']
        input_content = util.get_entry(input_title)

        return render(request, "encyclopedia/edit_entry.html", {
            "entry": input_content,
            "entry_title": input_title
        })

# for saving the edited entry
def save_edit(request):
    if request.method == 'POST':
        entry_title = request.POST['entry_title']
        entry_content = request.POST['entry_content']

        util.save_entry(entry_title, entry_content)
        edited_entry_html = convert_to_html(entry_title)

        return render(request, "encyclopedia/entry.html", {
            "entry": edited_entry_html,
            "entry_title": entry_title
        })
