Sistema de Gestão Patrimonial

1. Visão Geral
Este sistema implementa uma API RESTful para gestão de patrimônio, incluindo cadastro de produtos, fornecedores, clientes, movimentação de estoque, pedidos com fluxo de aprovação/separação/entrega e importação de Notas Fiscais Eletrônicas (NF-e). Baseado em Django/Django REST Framework e orientado por princípios de Domain‑Driven Design (DDD), o projeto foi apresentado a operadores e técnicos em abril/2025, resultando em feedbacks para exclusão em lote e registro de número de NF-e.

2. Arquitetura e Abordagem DDD
- Camadas:
  - Domain: Entidades, agregados, regras de negócio (core/models.py).  
  - Application: Serviços de aplicação (e.g., `PedidoService`, `MovimentacaoEstoqueService`).  
  - Infrastructure: Repositórios, persistência (ORM), serializers, views/routers (DRF).  
- Linguagem Ubíqua: Termos padronizados (`aprovar`, `separar`, `entregar`) garantem consistência.

3. Modelagem de Domínio
- Produto: código de barras, descrição, fornecedor, lote, validade, quantidade (atual/inicial), preço, status, área. Método `estoque_disponivel()` considera apenas pedidos não aprovados.  
- Fornecedor: nome, CNPJ, contato. Relacionamento 1:N com Produto.  
- Cliente: matrícula, nome, e-mail, telefone, curso. Relacionamento 1:N com MovimentaçãoEstoque e Pedidos.  
- NFe: número, data de emissão, CNPJ do fornecedor, peso, valor total. M2M com Produto.  
- MovimentacaoEstoque: tipo (entrada/saída), data, usuário, quantidade, produto, NF-e, cliente.  
- Pedido: fluxo de status (`aguardando_aprovacao` → `aprovado` → `separado` → `entregue`) com métodos `aprovar()`, `marcar_como_separado()`, `registrar_retirada()`.  
- ItemPedido e SaidaProdutoPorPedido: armazenam quantidades solicitadas, liberadas e baixas definitivas.

4. Serviços e Casos de Uso
- ImportacaoNFeService: parse de XML, criação de NFe, associação de Produtos, transacional.  
- MovimentacaoEstoqueService: validações (estoque mínimo, vencimento), registro de movimentações, atualização de saldo.  
- PedidoService: orquestra fluxos de aprovação, separação e entrega, uso de repositórios e notificações por e-mail.

5. API Endpoints (DRF)
- `/api/produtos/` (GET, POST, PUT, DELETE) via `ProdutoViewSet`.  
- `/api/pedidos/` com ações customizadas: `approve`, `separar`, `retirar`.  
- `/api/movimentar-estoque/` (POST) para entradas e saídas rápidas.  
- Documentação interativa via OpenAPI/Swagger.

6. Autenticação, Autorização e Segurança
- Autenticação padrão Django + tokens JWT (opcional).  
- Permissões de papel: apenas admins e técnicos aprovam pedidos; operadores criam pedidos e movimentam estoques.  
- Logs de auditoria (`LogAcao`) para rastrear ações críticas.

7. Testes e Qualidade
- Unitários: métodos de domínio (`Pedido.aprovar()`, `Produto.is_vencido()`).  
- Integração: fluxo completo de pedido e importação NF-e.  
- Contrato: validação de schemas JSON.  
- E2E: simulação via Postman/Cypress.  
- Cobertura meta: >90%.

8. Deploy e Infraestrutura
- Empacotamento Docker + docker-compose para dev.  
- CI/CD com GitHub Actions: lint, testes, build de imagem.  
- Deploy azul-verde ou canary para minimizar downtime.

9. Feedback e Evolução
- Abril/2025: operadores e técnicos sugeriram exclusão em lote no estoque e inserção do número da NF-e.  
- Alta satisfação geral com usabilidade e desempenho.  

10. Próximos Passos
- Modularizar em pacotes `domain/`, `application/`, `infrastructure/`.  
- Revisar e refinar DTOs/serializers.  
- Implementar repositórios especializados e patterns de caching (Redis).  
- Adicionar testes de performance, segurança e mutation testing.

11. Conformidade e Governança
- Adequação à LGPD: anonimização e consentimento de dados de clientes.  





