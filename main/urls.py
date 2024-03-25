from django.urls import path
from main import views


urlpatterns = [
    path('', views.chat, name='chat'),
    path("test", views.test, name="test")
]
