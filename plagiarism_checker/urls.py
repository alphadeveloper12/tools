from django.urls import path
from .views import PlagiarismCheckView

urlpatterns = [
    path('check-plagiarism/', PlagiarismCheckView.as_view(), name='check_plagiarism'),
]
