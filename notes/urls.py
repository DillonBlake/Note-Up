from django.urls import path
from . import views

# Url mappings for the notes app
urlpatterns = [
    path("notepad/", views.notepad, name="notepad"),
    path("menu/", views.menu, name="menu"),
    path("newnotebook/", views.new_notebook, name="new notebook"),
    path("help/", views.help, name="help"),
    path("edit/", views.edit, name="edit"),
    path("deletenotebook/", views.delete_notebook, name="delete notebook"),
    path("printable/", views.printable, name="printable"),
    path("rename/", views.rename, name="rename"),
    path("groups/", views.groups, name="groups"),
    path("newgroup/", views.new_group, name="new group"),
    path("deletegroup/", views.delete_group, name="delete group"),
    path("settings/", views.settings, name="settings"),
    path("settingsdata/", views.settings_edit, name="settings edit"),
    path("validate/", views.validate, name="validate")
]