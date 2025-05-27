# interface/controllers/usuario_controller.py
from django.shortcuts       import render, redirect, get_object_or_404
from django.contrib         import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls            import reverse
from django.contrib.auth    import get_user_model, update_session_auth_hash
from interface.forms.forms  import UsuarioForm
from interface.forms.forms  import ProfileForm
from django.http        import JsonResponse
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


def is_admin(user):
    return user.is_authenticated and user.papel == 'admin'


@login_required
@user_passes_test(lambda u: u.papel == 'admin')
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'core/usuarios.html', {
        'usuarios': usuarios
    })

@login_required
@user_passes_test(lambda u: u.papel == 'admin')
def novo_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            form.save_m2m()
            messages.success(request, "Usuário criado com sucesso.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'core/novo_usuario.html', {
        'form': form
    })

@login_required
@user_passes_test(lambda u: u.papel == 'admin')
def editar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            form.save_m2m()
            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'core/editar_usuario.html', {
        'form': form,
        'usuario': usuario
    })

@login_required
@user_passes_test(lambda u: u.papel == 'admin')
def excluir_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    usuario.delete()
    messages.success(request, "Usuário excluído com sucesso.")
    return redirect('lista_usuarios')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.papel == 'admin'

@login_required
@user_passes_test(is_admin)
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'core/usuarios.html', {
        'usuarios': usuarios,
    })

@login_required
@user_passes_test(is_admin)
def novo_usuario(request):
    # sua lógica de criação...
    pass

@login_required
@user_passes_test(is_admin)
def editar_usuario(request, id):
    # sua lógica de edição...
    pass

@login_required
@user_passes_test(is_admin)
def ativar_usuario(request, id):
    user = get_object_or_404(User, id=id)
    user.ativo = True
    user.save()
    messages.success(request, f"Usuário {user.username} ativado.")
    return redirect('lista_usuarios')

@login_required
@user_passes_test(is_admin)
def desativar_usuario(request, id):
    user = get_object_or_404(User, id=id)
    user.ativo = False
    user.save()
    messages.success(request, f"Usuário {user.username} desativado.")
    return redirect('lista_usuarios')

@login_required
@user_passes_test(is_admin)
def deletar_usuario(request, id):
    user = get_object_or_404(User, id=id)
    username = user.username
    user.delete()
    messages.success(request, f"Usuário {username} excluído com sucesso.")
    return redirect('lista_usuarios')

@login_required
def editar_perfil(request):
    """
    Permite ao usuário logado alterar seu username, email e senha.
    """
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        # Se a senha for alterada, mantém o usuário logado:
        update_session_auth_hash(request, request.user)
        messages.success(request, "Perfil atualizado com sucesso.")
        return redirect('editar_perfil')
    return render(request, 'core/editar_perfil.html', {
        'form': form,
    })
    
@csrf_exempt
@login_required
def salvar_usuario_inline(request):
    """
    Recebe JSON via POST e cria um novo usuário.
    """
    if request.method != 'POST':
        return JsonResponse({'sucesso': False, 'erro': 'Método não permitido'}, status=405)

    try:
        data = json.loads(request.body)
        form = UsuarioForm(data)
        if not form.is_valid():
            return JsonResponse({'sucesso': False, 'erro': form.errors}, status=400)
        usuario = form.save(commit=False)
        usuario.set_password(data.get('password') or User.objects.make_random_password())
        usuario.save()
        return JsonResponse({
            'sucesso': True,
            'id': usuario.id,
            'username': usuario.username,
        })
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=500)