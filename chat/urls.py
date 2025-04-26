# flake8: noqa
from django.urls import path
from . import views

app_name = 'Chat'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    # path('api/messages/<int:chat_id>/', views.get_messages, name='get_messages'),
    # path('api/send/', views.send_message, name='send_message'),
    # path('api/chats/', views.get_previous_chat, name='get_previous_chats'),
]
