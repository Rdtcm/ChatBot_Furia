from django.shortcuts import render

# Create your views here.


def chat_view(request):
    # Falta implementar:
    # Logica Para buscar conversas anteriores
    # previous_chat = ...

    return render(
        request,
        'chat/chat.html',
    )


def get_messages(request):
    ...


def send_message(request):
    ...


def get_previous_chat(request):
    ...
