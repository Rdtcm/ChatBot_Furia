# chat/views.py
# flake8: noqa
import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpRequest
from .models import Conversation, Messages
from .pandascore_service import buscar_agenda_furia, buscar_elenco_furia
from .deepseek_service import enviar_para_openrouter


@login_required(login_url='users:login')
def chat_view(request):
    previous_chats = Conversation.objects.filter(
        user=request.user
    ).order_by('-last_interaction_time')
    return render(request, 'chat/chat.html', {
        'previous_chats': previous_chats,
    })


@login_required(login_url='users:login')
@require_http_methods(['GET'])
def get_messages(request: HttpRequest, chat_id: int) -> JsonResponse:
    conversation = get_object_or_404(
        Conversation, id=chat_id, user=request.user)
    messages = Messages.objects.filter(
        conversation=conversation).order_by('timestamp')
    messages_data = [{
        'id': m.id,  # type: ignore
        'sender': m.sender.username,
        'text': m.text,
        'timestamp': m.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'is_bot': m.is_bot,
    } for m in messages]
    return JsonResponse({'messages': messages_data})


@login_required(login_url='users:login')
@require_http_methods(['POST'])
def send_message(request) -> JsonResponse:
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido.'}, status=400)

    message_text = data.get('message')
    chat_id = data.get('chat_id')

    if not message_text:
        return JsonResponse({'error': 'Mensagem vazia.'}, status=400)

    if chat_id:
        conversation = get_object_or_404(
            Conversation, id=chat_id, user=request.user)
    else:
        conversation = Conversation.objects.create(user=request.user)

    # pegando as mensagens anteriores
    mensagens_anteriores = Messages.objects.filter(
        conversation=conversation
    ).order_by('timestamp')

    historico = []
    for m in mensagens_anteriores:
        role = "assistant" if m.is_bot else "user"
        historico.append({"role": role, "content": m.text})

    if message_text.startswith('/'):
        if message_text == '/elenco':
            bot_response = buscar_elenco_furia()
        elif message_text == '/agenda':
            bot_response = buscar_agenda_furia()
        else:
            bot_response = 'Comando não reconhecido. Use /elenco ou /agenda.'
    else:
        bot_response = enviar_para_openrouter(message_text, historico).strip()

    user_message = Messages.objects.create(
        conversation=conversation,
        sender=request.user,
        text=message_text,
        is_bot=False,
    )
    bot_message = Messages.objects.create(
        conversation=conversation,
        sender=request.user,
        text=bot_response,
        is_bot=True,
    )

    conversation.last_interaction_time = user_message.timestamp
    conversation.save()

    return JsonResponse({
        'user_message': {
            'id': user_message.id,  # type: ignore
            'text': user_message.text,
            'timestamp': user_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        },
        'bot_message': {
            'id': bot_message.id,  # type: ignore
            'text': bot_message.text,
            'timestamp': bot_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        },
        'chat_id': conversation.id,
    })


@login_required(login_url='users:login')
@require_http_methods(['GET'])
def get_previous_chat(request) -> JsonResponse:
    previous_chats = Conversation.objects.filter(
        user=request.user).order_by('-last_interaction_time')
    chats_data = [{
        'id': c.id,
        'title': c.title or "Chat com Bot",
        'last_interaction': c.last_interaction_time.strftime('%Y-%m-%d %H:%M:%S'),
    } for c in previous_chats]
    return JsonResponse({'previous_chat': chats_data})
