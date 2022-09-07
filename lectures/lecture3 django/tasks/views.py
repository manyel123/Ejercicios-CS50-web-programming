from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

tasks = []

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

# Create your views here.
def index(request):
    # task for every session
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        # Valid form
        if form.is_valid(): 
            task = form.cleaned_data["task"]
            # Get the user tasks from sessions
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        # Invalid form
        else:
            # return the form so the user can make corrections
            return render(request, "tasks/add.html", {
                "form": form
            })
    # return an empty form
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })