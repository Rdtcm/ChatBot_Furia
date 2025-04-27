# flake8: noqa
from django.shortcuts import render, get_object_or_404
from .models import Conversation, Messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
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
def get_messages(request, chat_id):
    '''Este metodo vai ser chamado pelo js no frontend quando o usuario
       clicar em uma conversa, o js fara uma requisicao do tipo AJAX
    '''

    if request.is_ajax():
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
                        'id': message.id,
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


@login_required(login_url='users:login')
def send_message(request, chat_id):
    '''
        Esta view sera responsavel por receber uma mensagem, identificar se e 
        comando, isto e, inicia-se com "/", e retornar uma resposta.

        Preciso conectar com a api do deep seek

        Preciso verificar se e um comando, e conectar com as apis que fornecem 
        o ranking da furia, o elenco da furia e o catalogo de jogos da furia

    '''

    if request.is_ajax():
        try:
            data = json.loads(request.body)
            message_text = data.get('message')
            chat_id = data.get('chat_id')

            if not message_text:
                return JsonResponse({'error': 'Mensagem Vazia!'}, status=400)
            
            # verificando se existe uma conversa com o chat_id
            if chat_id:
                Conversation = get_object_or_404(Conversation, id=chat_id, user=request.user)
            else:
                Conversation = Conversation.objects.create(user=request.user)
            
            

        except Exception as e:
            return JsonResponse({'error': 'Requisicao Invalida!'}, status=400)




@login_required(login_url='users:login')
def get_previous_chat(request):
    '''
        Endpoint que o js pode chamar no frontend dinamicamente para obter os chats
        atualizados sem precisar de um refresh na pagina

        SOMENTE USUARIOS LOGADOS DEVEM TER ACESSO
    '''

    if request.is_ajax():
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
    
