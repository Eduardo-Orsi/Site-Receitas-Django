import email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

def cadastro(request):
    """Cadastra uma nova pessoa no sistema"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email_input = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'O campo nome não pode ficar em branco')
            return render(request, 'usuarios/cadastro.html')
        if campo_vazio(email_input):
            messages.error(request, 'O campo e-mail não pode ficar vazio')
            return render(request, 'usuarios/cadastro.html')
        if senhas_nao_sao_iguais(senha, senha2):
            messages.error(request, 'As senhas não são iguais')
            return render(request, 'usuarios/cadastro.html')
        if User.objects.filter(email=email_input).exists():
            messages.error(request, 'E-mail já utilizado')
            return render(request, 'usuarios/cadastro.html')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Nome já utilizado')
            return render(request, 'usuarios/cadastro.html')
        user = User.objects.create_user(username=nome, email=email_input, password=senha)
        user.save()
        print('Usuário criado com sucesso')
        messages.success(request, 'Cadastro realizado sucesso!')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    """Realiza o login de uma pessoa no sistema"""
    if request.method == 'POST':
        email_input = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email_input) or campo_vazio(senha):
            messages.error(request, 'Os campos e-mail e senha não podem ficar em branco')
            return redirect('login')
        if User.objects.filter(email=email_input).exists():
            nome = User.objects.filter(email=email_input).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso!')
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')

def logout(request):
    """Desloga a pessoa do sistema"""
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    """Exibe um dasboard com as apenas as receitas criadas pela pessoa"""
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)
        
        dados = {
            'nome_das_receitas': receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    return redirect('index')

def campo_vazio(campo):
    """Verifica se algum campo do formulário está vazio"""
    return not campo.strip()

def senhas_nao_sao_iguais(senha, senha2):
    """Verifica se as senhas inseridas no cadastro são iguais"""
    return senha != senha2
