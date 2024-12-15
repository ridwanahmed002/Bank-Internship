from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload_file, name="upload_file"),
    path("check-header/", views.check_header, name="check_header"),
    path("visualize-data/", views.visualize_data, name="visualize_data"),
    path("extract-csv/", views.extract_csv, name="extract_csv"),
    path("visualize-data/", views.visualize_data, name="visualize_data"),

]
