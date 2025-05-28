# interface/controllers/usuario_controller.py

import json
from datetime import datetime
from io import BytesIO

from django.shortcuts            import render, redirect, get_object_or_404
from django.contrib              import messages
from django.contrib.auth         import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http                 import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions  import TruncMonth
from django.db.models            import Count
from django.utils.crypto         import get_random_string
from openpyxl                    import Workbook

from interface.forms.forms       import UsuarioForm, ProfileForm
from core.models                 import Area, MovimentacaoEstoque

User = get_user_model()


def is_admin(user):
    return user.is_authenticated and user.papel == 'admin'


@login_required
@user_passes_test(is_admin)
def lista_usuarios(request):
    usuarios = User.objects.all()
    areas    = Area.objects.all()
    return render(request, 'core/usuarios.html', {
        'usuarios': usuarios,
        'areas':    areas,
    })


@login_required
@user_passes_test(is_admin)
def novo_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            pwd  = form.cleaned_data.get('password1')
            if pwd:
                user.set_password(pwd)
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
@user_passes_test(is_admin)
def editar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            pwd  = form.cleaned_data.get('password1')
            if pwd:
                user.set_password(pwd)
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
@user_passes_test(is_admin)
def excluir_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    usuario.delete()
    messages.success(request, "Usuário excluído com sucesso. (excluir_usuario)")
    return redirect('lista_usuarios')


@login_required
@user_passes_test(is_admin)
def deletar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    username = usuario.username
    usuario.delete()
    messages.success(request, f"Usuário {username} excluído com sucesso. (deletar_usuario)")
    return redirect('lista_usuarios')


@login_required
@user_passes_test(is_admin)
def ativar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    usuario.ativo = True
    usuario.save()
    messages.success(request, f"Usuário {usuario.username} ativado.")
    return redirect('lista_usuarios')


@login_required
@user_passes_test(is_admin)
def desativar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    usuario.ativo = False
    usuario.save()
    messages.success(request, f"Usuário {usuario.username} desativado.")
    return redirect('lista_usuarios')


@login_required
def editar_perfil(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Perfil atualizado com sucesso.")
        return redirect('editar_perfil')
    return render(request, 'core/editar_perfil.html', {
        'form': form,
    })


@csrf_exempt
@login_required
def salvar_usuario_inline(request):
    if request.method != 'POST':
        return JsonResponse({'sucesso': False, 'erro': 'Método não permitido'}, status=405)

    try:
        data = json.loads(request.body)
        form = UsuarioForm(data)
        if not form.is_valid():
            return JsonResponse({'sucesso': False, 'erro': form.errors}, status=400)

        usuario = form.save(commit=False)
        # usa get_random_string para fallback
        pwd = data.get('password1') or get_random_string(8)
        usuario.set_password(pwd)
        usuario.save()
        form.save_m2m()

        return JsonResponse({
            'sucesso': True,
            'id': usuario.id,
            'username': usuario.username,
        })
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=500)


@login_required
@user_passes_test(is_admin)
def exportar_sessoes_excel(request):
    sessoes = (
        MovimentacaoEstoque.objects
            .annotate(mes=TruncMonth('data'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('mes')
    )
    wb = Workbook()
    ws = wb.active
    ws.title = "Sessões por Mês"
    ws.append(["Mês", "Total de Sessões"])
    for s in sessoes:
        ws.append([s['mes'].strftime("%Y-%m"), s['total']])
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    hoje = datetime.now().strftime("%Y%m%d")
    filename = f"sessoes_por_mes_{hoje}.xlsx"
    resp = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp
