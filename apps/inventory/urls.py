from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("lotes/", views.lote_list, name="lote_list"),
]