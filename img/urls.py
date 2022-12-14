from django.urls import path
from img.views import *

urlpatterns = [
    path('upload/',ImageViews.as_view()),
]