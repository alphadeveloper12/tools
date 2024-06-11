from django.urls import path
from .views import plagiarism_removal_view

urlpatterns = [
    path('plagiarism-remover/', plagiarism_removal_view, name='plagiarism_remover'),
]