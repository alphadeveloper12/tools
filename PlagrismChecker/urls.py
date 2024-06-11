from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('plagiarism_checker.urls')),
    path('api/', include('plagiarism_remover.urls')),
    path('api/', include('grammer_checker.urls')),
]
