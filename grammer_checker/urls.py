
from django.urls import path
from . import views

urlpatterns = [
    path('grammer-check/', views.grammar_correction, name='process_text_api'),  # Mapping for the REST API endpoint
]