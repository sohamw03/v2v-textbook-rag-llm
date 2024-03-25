from django.urls import path
from main import views


urlpatterns = [
    path('', views.test, name='test'),
    path("chat", views.chat, name="chat")
]
