from django.urls import path    
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload_file, name="upload_file"),
    path("generate-chart/", views.generate_chart_ajax, name="generate_chart"),
    path("download-excel/", views.download_cleaned_excel, name="download_excel"),
    path("download-chart-pdf/", views.download_chart_pdf, name="download_chart_pdf"),
]