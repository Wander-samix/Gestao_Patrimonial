import json
from datetime import date
from decimal import Decimal
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from core.application.dtos.produto_dto import CreateProdutoDTO
from core.application.services.criar_produto_service import ProdutoService

@require_POST
def criar_produto(request):
    # 1) Parse do JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) Converte validade (ISO) se for string
    val_str = payload.get('validade')
    if isinstance(val_str, str):
        try:
            payload['validade'] = date.fromisoformat(val_str)
        except ValueError:
            return JsonResponse({'error': "Formato de 'validade' inválido, use YYYY-MM-DD."}, status=400)

    # 3) Converte preco_unitario para Decimal (se vier como string)
    prec = payload.get('preco_unitario')
    if isinstance(prec, str):
        try:
            payload['preco_unitario'] = Decimal(prec)
        except:
            return JsonResponse({'error': "'preco_unitario' inválido."}, status=400)

    # 4) Monta DTO
    dto = CreateProdutoDTO(
        codigo_barras=payload.get('codigo_barras', ''),
        descricao=payload.get('descricao', ''),
        fornecedor_id=payload.get('fornecedor_id', 0),
        quantidade=payload.get('quantidade', -1),
        preco_unitario=payload.get('preco_unitario', Decimal("0")),
        nfe_numero=payload.get('nfe_numero'),
        area_id=payload.get('area_id'),
        validade=payload.get('validade'),
    )

    # 5) Executa serviço
    service = ProdutoService()
    try:
        out = service.create(dto)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 6) Retorna JSON
    return JsonResponse({
        'id': out.id,
        'codigo_barras': out.codigo_barras,
        'descricao': out.descricao,
        'fornecedor_id': out.fornecedor_id,
        'quantidade': out.quantidade,
        'preco_unitario': str(out.preco_unitario),
        'nfe_numero': out.nfe_numero,
        'area_id': out.area_id,
        'validade': out.validade.isoformat() if out.validade else None,
        'lote': out.lote,
        'criado_em': out.criado_em.isoformat(),
    }, status=201)
