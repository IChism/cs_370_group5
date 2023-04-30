from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    # Reports
    path("categories", views.categories, name="categories"),
    path("customers", views.customers, name="customers"),
    path("ratings", views.ratings, name="ratings"),
    path("import", views.imports, name="imports")
]