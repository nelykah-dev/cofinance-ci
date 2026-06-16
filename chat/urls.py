from django.urls import path
from .views import chat_page

app_name = 'chat'

urlpatterns = [
    path('interface/', chat_page, name='chat-interface'),
]