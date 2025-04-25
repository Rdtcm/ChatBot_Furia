# flake8: noqa
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
# decorator para validar se o usuario esta logado
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from users.forms import RegisterForm, RegisterUpdateForm


# Create your views here.

'''views relacionadas aos formularios de usuarios'''


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado com sucesso')
            return redirect('home')

    return render(
        request,
        'users/register.html',
        {
            'form': form,
        }
    )


@login_required(login_url='users:login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method != 'POST':
        return render(
            request,
            'users/user_update.html',
            {
                'form': form,
            }
        )

    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'contact/user_update.html',
            {
                'form': form,
            }
        )

    form.save()
    return redirect('users:user_update')


def login_view(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Logado com sucesso!')
            return redirect('home')
        messages.error(request, 'Login invalido!')

    return render(
        request,
        'users/login.html',
        {
            'form': form
        }
    )


@login_required(login_url='users:login')
def logout_view(request):
    auth.logout(request)
    return redirect('users:login')
