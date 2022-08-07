from http.client import HTTPResponse
from time import timezone
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Notebook, Group, Settings, User_Log
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.staticfiles.storage import staticfiles_storage
import json
import csv
from datetime import datetime
import pytz
from pytz import timezone


#This function logs the user request and renders the requested notepad
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
def notepad(request):
    name = request.GET["name"]
    group = request.GET["group"]
    log(request, "/notes/notepad/?name=" + name + "&group=" + group)
    context = {"store": 'let name = "' + name + '"; let group = "' + group + '";'}
    return render(request, "notes/notepad.html", context=context)

#This function logs the user request, gets the notebooks for the group, then renders the group page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
def menu(request):
    group = request.GET["group"]
    user = request.user.email
    log(request, "/notes/menu/?group=" + group)
    notebooks = Notebook.objects.filter(owner=user, group=group)
    context = {"notes": notebooks, "store": 'let group = "' + group + '";', "group": group}
    return render(request, "notes/menu.html", context=context)

#This function logs the request then creaes a new notebook and assigns it a user, name, and group
#Sends user to notebook page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
def new_notebook(request):
    name = request.GET["name"]
    user = request.user.email
    group = request.GET["group"]
    log(request, "/notes/newnotebook/?name=" + name + "&group=" + group)
    #check if name available
    notebooks = Notebook.objects.filter(owner=user, name=name, group=group)
    if len(notebooks) == 0:
        data = {
            "input": "",
            "code": {}
        }
        notebook = Notebook.objects.create_notebook(name=name, owner=user, group=group, data=json.dumps(data))
    return redirect("/notes/notepad/?name=" + name + "&group=" + group)

#This function shows the help page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
def help(request):
    #Figure out necessary page navigation
    if "name" in request.GET and "group" in request.GET:
        name = request.GET["name"]
        group = request.GET["group"]
        context = {"next_url" : "/notes/notepad/?name=" + name + "&group=" + group,
                    "next_label": "Back"}
    else:
        context = {"next_url": "/notes/groups",
                    "next_label": "Continue"}
    return render(request, "notes/help.html", context=context)

#This is is the edit api for to save to the database
#First it logs the request
#A get request returns the current stored data while a post updates it
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
@csrf_exempt
def edit(request):
    group = request.GET["group"]
    name = request.GET["name"]
    user = request.user.email
    log(request, "/notes/edit/?name=" + name + "&group=" + group)
    notebooks = Notebook.objects.filter(name=name, owner=user, group=group)

    #Check that the notebook exists
    if len(notebooks) == 0:
        name = name[0].lower() + name[1:]
        notebooks = Notebook.objects.filter(name=name, owner=user, group=group)

    if len(notebooks) == 0:
        return HttpResponse("Error: No File Called: " + name + " For User with Email: " + user) 
    else:
        notebook = notebooks[0]
    if request.method == "GET":
        data = notebook.data
        return HttpResponse(data)
    elif request.method == "POST":
        data = request.body.decode("UTF-8")
        notebook.data = data
        notebook.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

#This function logs the request then deletes a notebook within group belonging to user
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
def delete_notebook(request):
    name = request.GET["name"]
    user = request.user.email
    group = request.GET["group"]
    log(request, "/notes/deletenotebook/?name=" + name + "&group=" + group)
    notebook = Notebook.objects.filter(name=name, owner=user)[0]
    notebook.delete()
    return redirect("/notes/menu/?group=" + group)

#This function logs the request then renders a printable version of the notes
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
def printable(request):
    name = request.GET["name"]
    group = request.GET["group"]
    log(request, "/notes/printable/?name=" + name + "&group=" + group)
    context = {"store": 'let name = "' + name + '"; let group = "' + group + '";'}
    return render(request, "notes/printable.html", context=context)

#This function allows the user to rename a notebook. First the request is logged
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
@csrf_exempt
def rename(request):
    if request.method != "GET":
        return HttpResponse(status=400)
    oldName = request.GET["name"]
    user = request.user.email
    newName = request.GET["new"]
    group = request.GET["group"]
    log(request, "/notes/notepad/?oldname=" + oldName + "&new=" + newName + "&group=" + group)
    notebooks = Notebook.objects.filter(owner=user, name=newName, group=group)
    #Check that notebook exists
    if len(notebooks) != 0:
        return HttpResponse(status=500)
    #Change name
    notebook = Notebook.objects.filter(name=oldName, owner=user, group=group)[0]
    notebook.name = newName
    notebook.save()
    return HttpResponse(status=200)

#This function logs the request then returns the groups page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
def groups(request):
    user = request.user.email
    log(request, "/notes/groups")
    groups = Group.objects.filter(owner=user)
    context = {"groups": groups}
    return render(request, "notes/groups.html", context=context)

#This function logs the request then creates a new group
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
@csrf_exempt
def new_group(request):
    name = request.GET["name"]
    user = request.user.email
    log(request, "/notes/newgroup/?name=" + name)
    groups = Group.objects.filter(name=name, owner=user)
    #Check that group doesn't already exist
    if len(groups) == 0:
        group = Group.objects.create_group(name=name, owner=user)
    return redirect("/notes/menu/?group=" + name)

#This function logs the request then deletes a group
#There are no checks for if the group exists, might be worthwhile to add in future version
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
@csrf_exempt
def delete_group(request):
    user = request.user.email
    group = request.GET["group"]
    log(request, "/notes/deletegroup/&group=" + group)
    group = Group.objects.filter(name=group, owner=user)[0]
    #Delete group then delete all of group's notebooks
    group.delete()
    notebooks = Notebook.objects.filter(owner=user, group=group)
    for notebook in notebooks:
        notebook.delete()
    return redirect("/notes/groups")

#This function logs the request then loads the user's settings page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
def settings(request):
    notebook = request.GET["name"]
    group = request.GET["group"]
    log(request, "/notes/settings/?name=" + notebook + "&group=" + group)
    user = request.user.email
    context = get_settings(user)
    context["notebook"] = notebook
    context["group"] = group
    return render(request, "notes/settings.html", context=context)

#This is a helper function to return the user's settings as a dict in json format
def get_settings(user):
    settings = Settings.objects.filter(user=user)
    #If settings doesn't exist, create it
    if(len(settings) == 0):
        #Load default settings from static
        latex = []
        html = []
        latex_path = staticfiles_storage.path("notes/data/Latex_Codes.csv")
        html_path = staticfiles_storage.path("notes/data/HTML_Codes.csv")
        #First load latex settings
        with open(latex_path, "r", encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                latex.append({
                    "Letter": row["Letter"],
                    "Code": row["Code"],
                    "Latex": row["Latex"]
                })
        #Then load html settings
        with open(html_path, "r", encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                html.append({
                    "Letter": row["Letter"],
                    "Code": row["Code"],
                    "HTML": row["HTML"]
                })
        s = Settings.objects.create_settings(user, json.dumps(latex), json.dumps(html))
    else:
        s = settings[0]

    data = {"latex": json.loads(s.latex), "html": json.loads(s.html)}
    return data

#This function logs the request and lets the user edit settings
#A get request returns the current settings and a post request saves new settings
#Lacks checks if settings exist for get, might be worth an update
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
@csrf_exempt
def settings_edit(request):
    user = request.user.email
    log(request, "/notes/settingsdata/")
    if request.method == "GET":
        return HttpResponse(json.dumps(get_settings(user)))
    elif request.method == "POST":
        settings = Settings.objects.filter(user=user)[0]
        data = json.loads(request.body.decode("UTF-8"))
        settings.latex = json.dumps(data["latex"])
        settings.html = json.dumps(data["html"])
        settings.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

#Based off of the answer to https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django by yanchenko
#Gets the ip address of the request
def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')

#Logs a given request for a url
def log(request, url):
    #Save the ip, url, and time of the request
    ip = get_client_ip(request)
    user = request.user.email
    timezone = pytz.timezone("UTC")
    now = datetime.now()
    zoned = timezone.localize(now)
    User_Log.objects.create_log(user, ip, url, zoned)

#This function checks if the user is new. If they are it sends them to the help page
#Otherwise they are sent to their groups page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(redirect_field_name="/accounts/login")
def validate(request):
    user = request.user.email
    logs = User_Log.objects.filter(user=user)
    if(len(logs) == 0):
        redirect("/notes/help")
    else:
        redirect("/notes/groups")
