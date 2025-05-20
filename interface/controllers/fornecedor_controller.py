import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_fornecedor_service import CriarFornecedorService

@require_POST
def criar_fornecedor(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarFornecedorService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        fornecedor = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': fornecedor.id,
        'nome': fornecedor.nome,
        'cnpj': fornecedor.cnpj,
        'endereco': fornecedor.endereco,
        'telefone': fornecedor.telefone,
        'email': fornecedor.email,
        'ativo': fornecedor.ativo,
    }, status=201)
