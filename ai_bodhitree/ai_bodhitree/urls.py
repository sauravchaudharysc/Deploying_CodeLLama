# In ai_bodhitree/urls.py
from django.contrib import admin
from django.urls import path, include
from llmpredictor.views import home  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('llmpredictor/', include('llmpredictor.urls')),  # Include app URLs
    path('', home),  # Add this line to include the home view
]
