import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_nfe_service import CriarNfeService

@require_POST
def criar_nfe(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarNfeService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        nfe = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': nfe.id,
        'numero': nfe.numero,
        'data_emissao': nfe.data_emissao.isoformat(),
        'cnpj_fornecedor': nfe.cnpj_fornecedor,
        'peso': nfe.peso,
        'valor_total': float(nfe.valor_total),
        'itens_vinculados_ids': nfe.itens_vinculados_ids,
        'area_id': nfe.area_id,
    }, status=201)
