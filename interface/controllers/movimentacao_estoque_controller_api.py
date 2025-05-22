import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.dtos.movimentacao_estoque_dto import CreateMovimentacaoEstoqueDTO
from core.application.services.criar_movimentacao_estoque_service import MovimentacaoEstoqueService

@require_POST
def criar_movimentacao_estoque(request):
    # 1) Parse do JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) DTO de entrada
    dto = CreateMovimentacaoEstoqueDTO(
        tipo=payload.get('tipo', ''),
        data=payload.get('data'),
        usuario_id=payload.get('usuario_id'),
        quantidade=payload.get('quantidade'),
        produto_id=payload.get('produto_id'),
        nota_fiscal_id=payload.get('nota_fiscal_id'),
        cliente_id=payload.get('cliente_id'),
    )

    # 3) Chama serviço
    service = MovimentacaoEstoqueService()
    try:
        out = service.create(dto)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 4) Serializa datetime e retorna
    return JsonResponse({
        'id': out.id,
        'tipo': out.tipo,
        'data': out.data.isoformat(),
        'usuario_id': out.usuario_id,
        'quantidade': out.quantidade,
        'produto_id': out.produto_id,
        'nota_fiscal_id': out.nota_fiscal_id,
        'cliente_id': out.cliente_id,
    }, status=201)
