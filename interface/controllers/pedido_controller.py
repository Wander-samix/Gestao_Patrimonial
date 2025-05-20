import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_pedido_service import CriarPedidoService

@require_POST
def criar_pedido(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarPedidoService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        pedido = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': pedido.id,
        'codigo': pedido.codigo,
        'usuario_id': pedido.usuario_id,
        'data_solicitacao': pedido.data_solicitacao.isoformat(),
        'status': pedido.status,
        'aprovado_por_id': pedido.aprovado_por_id,
        'data_aprovacao': pedido.data_aprovacao.isoformat() if pedido.data_aprovacao else None,
        'data_separacao': pedido.data_separacao.isoformat() if pedido.data_separacao else None,
        'data_retirada': pedido.data_retirada.isoformat() if pedido.data_retirada else None,
        'retirado_por': pedido.retirado_por,
        'observacao': pedido.observacao,
        'data_necessaria': pedido.data_necessaria.isoformat() if pedido.data_necessaria else None,
    }, status=201)
