import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_saida_produto_por_pedido_service import CriarSaida_produto_por_pedidoService

@require_POST
def criar_saida_produto_por_pedido(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarSaida_produto_por_pedidoService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        saida = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': saida.id,
        'produto_id': saida.produto_id,
        'pedido_id': saida.pedido_id,
        'quantidade': saida.quantidade,
        'data_saida': saida.data_saida.isoformat()
    }, status=201)
