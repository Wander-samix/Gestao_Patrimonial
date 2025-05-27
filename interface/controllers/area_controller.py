# interface/controllers/area_controller.py

from django.shortcuts                  import render, redirect, get_object_or_404
from django.contrib.auth.decorators   import login_required, user_passes_test
from django.http                       import JsonResponse
from django.views.decorators.http      import require_GET
from django.contrib                    import messages

from core.models                       import Area, Produto
from django.db.models                  import Max, Min, Sum

# Importa a função que calcula estoque disponível
from interface.controllers.pedido_controller import calcular_estoque_disponivel

def is_admin(user):
    return user.is_authenticated and user.papel == 'admin'


@login_required
def lista_areas(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        Area.objects.create(nome=nome)
        return redirect("lista_areas")
    return render(request, "core/areas.html", {
        "areas": Area.objects.all()
    })


@login_required
@user_passes_test(is_admin)
def nova_area(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        Area.objects.create(nome=nome)
        messages.success(request, "Área criada com sucesso.")
        return redirect("lista_areas")
    return render(request, "core/nova_area.html")


@login_required
@user_passes_test(is_admin)
def editar_area(request, id):
    area = get_object_or_404(Area, id=id)
    if request.method == "POST":
        area.nome = request.POST.get("nome", area.nome)
        area.save()
        messages.success(request, "Área atualizada com sucesso.")
        return redirect("lista_areas")
    return render(request, "core/editar_area.html", {"area": area})


@login_required
@user_passes_test(is_admin)
def excluir_area(request, id):
    area = get_object_or_404(Area, id=id)
    area.delete()
    messages.success(request, "Área removida com sucesso.")
    return redirect("lista_areas")


@login_required
@require_GET
def produtos_por_area(request, area_id):
    """
    Retorna JSON com os produtos ativos de uma área, 
    agrupados por código de barras e calculando o estoque disponível.
    """
    # Busca produtos ativos naquela área
    qs = Produto.objects.filter(area_id=area_id, status="ativo")

    # Agrupa para pegar um registro representante de cada combo (código_barras, área)
    agrupados = qs.values("codigo_barras", "area_id") \
                  .annotate(
                      produto_id    = Max("id"),
                      descricao     = Max("descricao"),
                      validade      = Min("validade"),
                      total_estoque = Sum("quantidade"),
                  )

    resultados = []
    for item in agrupados:
        disp = calcular_estoque_disponivel(
            item["codigo_barras"],
            item["area_id"]
        )
        if disp <= 0:
            continue

        resultados.append({
            "id":         item["produto_id"],
            "descricao":  item["descricao"],
            "validade":   item["validade"].strftime("%Y-%m-%d") if item["validade"] else "",
            "disponivel": disp,
        })

    return JsonResponse(resultados, safe=False)
