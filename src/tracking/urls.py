from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("see_all/", views.see_all, name="see_all"),
    path("download/", views.download_data, name="download"),
    path("delete/<int:expense_id>/", views.delete_expense, name="delete_expense"),
]
