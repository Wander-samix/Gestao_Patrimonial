# interface/controllers/fornecedor_controller.py
import json

from django.shortcuts           import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http                import JsonResponse
from django.contrib             import messages
from django.views.decorators.csrf import csrf_exempt

from core.models import Fornecedor

@login_required
def lista_fornecedores(request):
    """
    Exibe a lista de fornecedores.
    """
    fornecedores = Fornecedor.objects.all().order_by('nome')
    return render(request, "core/fornecedores.html", {
        "fornecedores": fornecedores
    })

@login_required
def novo_fornecedor(request):
    """
    Cria um novo fornecedor via POST.
    """
    if request.method == "POST":
        nome     = request.POST.get("nome", "").strip()
        cnpj     = request.POST.get("cnpj", "").strip()
        telefone = request.POST.get("telefone", "").strip()
        email    = request.POST.get("email", "").strip()

        if not nome or not cnpj:
            messages.error(request, "Nome e CNPJ são obrigatórios.")
            return redirect("lista_fornecedores")

        Fornecedor.objects.create(
            nome     = nome,
            cnpj     = cnpj,
            telefone = telefone,
            email    = email,
            ativo    = True
        )
        messages.success(request, "Fornecedor criado com sucesso.")
        return redirect("lista_fornecedores")

    # Em GET, simplesmente redireciona de volta à lista
    return redirect("lista_fornecedores")


@login_required
def editar_fornecedor(request, id):
    """
    Exibe formulário e salva alterações de um fornecedor existente.
    """
    f = get_object_or_404(Fornecedor, pk=id)

    if request.method == "POST":
        f.nome     = request.POST.get("nome", f.nome).strip()
        f.cnpj     = request.POST.get("cnpj", f.cnpj).strip()
        f.telefone = request.POST.get("telefone", f.telefone).strip()
        f.email    = request.POST.get("email", f.email).strip()
        f.save()
        messages.success(request, f"Fornecedor “{f.nome}” atualizado com sucesso.")
        return redirect("lista_fornecedores")

    # GET → exibe template de edição
    return render(request, "core/editar_fornecedor.html", {
        "fornecedor": f
    })


@login_required
def excluir_fornecedor(request, id):
    """
    Exclui um fornecedor.
    """
    f = get_object_or_404(Fornecedor, pk=id)
    f.delete()
    messages.success(request, f"Fornecedor “{f.nome}” excluído com sucesso.")
    return redirect("lista_fornecedores")


@login_required
def ativar_fornecedor(request, pk):
    """
    Marca um fornecedor como ativo.
    """
    f = get_object_or_404(Fornecedor, pk=pk)
    f.ativo = True
    f.save()
    messages.success(request, f"Fornecedor “{f.nome}” ativado com sucesso.")
    return redirect("lista_fornecedores")


@login_required
def desativar_fornecedor(request, pk):
    """
    Marca um fornecedor como inativo.
    """
    f = get_object_or_404(Fornecedor, pk=pk)
    f.ativo = False
    f.save()
    messages.success(request, f"Fornecedor “{f.nome}” desativado com sucesso.")
    return redirect("lista_fornecedores")


@csrf_exempt
@login_required
def salvar_fornecedor_inline(request):
    """
    AJAX JSON para criar um fornecedor inline.
    """
    if request.method != "POST":
        return JsonResponse({"sucesso": False, "erro": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
        nome     = data.get("nome", "").strip()
        cnpj     = data.get("cnpj", "").strip()
        telefone = data.get("telefone", "").strip()
        email    = data.get("email", "").strip()

        if not nome or not cnpj:
            return JsonResponse({"sucesso": False, "erro": "Nome e CNPJ são obrigatórios."})

        f = Fornecedor.objects.create(
            nome     = nome,
            cnpj     = cnpj,
            telefone = telefone,
            email    = email,
            ativo    = True
        )
        return JsonResponse({"sucesso": True, "id": f.id})

    except Exception as e:
        return JsonResponse({"sucesso": False, "erro": str(e)}, status=400)
