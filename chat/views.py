# flake8: noqa
from django.shortcuts import render, get_object_or_404
from .models import Conversation, Messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
import json
from .pandascore_service import buscar_agenda_furia, buscar_elenco_furia
from .deepseek_service import enviar_para_deepseek
# Create your views here.


@login_required(login_url='users:login')
def chat_view(request):
    previous_chats = Conversation.objects.filter(
        user=request.user).order_by('-last_interaction_time')

    return render(
        request,
        'chat/chat.html',
        {
            'previous_chats': previous_chats,
        }
    )


@login_required(login_url='users:login')
def get_messages(request: HttpRequest, chat_id: int) -> JsonResponse:
    '''Este metodo vai ser chamado pelo js no frontend quando o usuario
       clicar em uma conversa, o js fara uma requisicao do tipo AJAX
    '''

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # tenta buscar uma conversa, se nao existir retorna um status 404
            conversation = get_object_or_404(
                Conversation, id=chat_id, user=request.user)

            # busca todas as mensagens associadas a esta conversa, ordenadas pelo timestamp
            messages = Messages.objects.filter(
                conversation=conversation).order_by('timestamp')

            # organiza a mensagem que sera enviada via json
            messages_data = []
            for message in messages:
                messages_data.append(
                    {
                        'id': message.id,  # type: ignore
                        'sender': message.sender.username,
                        'text': message.text,
                        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        'is_bot': message.is_bot,
                    }
                )

            return JsonResponse({'messages': messages_data})

        except Exception as e:
            # caso ocorra algum erro, retorno status 500
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'O request deve ser do tipo AJAX'})


@login_required(login_url='users:login')
def send_message(request, chat_id):
    '''
        Esta view sera responsavel por receber uma mensagem, identificar se e 
        comando, isto e, inicia-se com "/", e retornar uma resposta.

        Preciso conectar com a api do deep seek

        Preciso verificar se e um comando, e conectar com as apis que fornecem 
        o ranking da furia, o elenco da furia e o catalogo de jogos da furia

    '''

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            message_text = data.get('message')
            chat_id = data.get('chat_id')

            if not message_text:
                return JsonResponse({'error': 'Mensagem Vazia!'}, status=400)

            # verificando se existe uma conversa com o chat_id
            if chat_id:
                conversation = get_object_or_404(
                    Conversation, id=chat_id, user=request.user)
            else:
                conversation = Conversation.objects.create(user=request.user)

            # verificando se a mensagem e um comando
            if message_text.startswith('/'):
                if message_text == '/elenco':
                    bot_reponse = buscar_elenco_furia()
                elif message_text == '/agenda':
                    bot_reponse = buscar_agenda_furia()
                else:
                    bot_reponse = 'Comando nao reconhecido. Tente /elenco ' \
                        'ou /agenda.'
            else:
                # se nao for um comando, envio para a api do DeepSeek
                bot_response = enviar_para_deepseek(message_text)

            # salvando a mensagem do usuario no banco de dados
            user_message = Messages.objects.create(
                conversation=conversation,
                sender=request.user,
                text=message_text,
                is_bot=False,
            )

            # salvando a resposta do bot
            bot_message = Messages.objects.create(
                conversation=conversation,
                sender=request.user,
                text=bot_reponse,
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

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Requisicao Invalida!'}, status=400)


@login_required(login_url='users:login')
def get_previous_chat(request):
    '''
        Endpoint que o js pode chamar no frontend dinamicamente para obter os chats
        atualizados sem precisar de um refresh na pagina

        SOMENTE USUARIOS LOGADOS DEVEM TER ACESSO
    '''

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # buscaando todas as conversas de um usuario
        previous_chat = Conversation.objects.filter(
            user=request.user).order_by('-last_interaction_time')

        chats_data = []
        for chat in previous_chat:
            chats_data.append({
                'id': chat.id,
                'title': chat.title if chat.title else "Chat com Bot",
                'last_interaction': chat.last_interaction_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse({'previous_chat': chats_data})
    else:
        return JsonResponse({'error': 'A requisicao deve ser AJAX'}, status=400)
