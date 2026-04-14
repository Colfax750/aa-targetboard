from django.urls import path
from . import views

app_name = "aa_targetboard"

urlpatterns = [
    path("", views.target_list, name="list"),
    path("new/", views.target_create, name="create"),
    path("<int:pk>/", views.target_detail, name="detail"),
    path("<int:pk>/edit/", views.target_edit, name="edit"),
    path("<int:pk>/delete/", views.target_delete, name="delete"),
]
