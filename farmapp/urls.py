from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_report_view, name='create_report'),
    path('download/<int:report_id>/', views.download_pdf_view, name='download_pdf'),
]
