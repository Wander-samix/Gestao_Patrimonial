Sistema de Gestão Patrimonial

Este projeto consiste em uma API RESTful para cadastro e controle de produtos, fornecedores, clientes, fluxos de pedidos (aprovação, separação e retirada), movimentação de estoque e importação de Notas Fiscais Eletrônicas. Implementado em Django com princípios de Domain-Driven Design, a aplicação oferece uma solução escalável, testável e de fácil manutenção para a gestão patrimonial.

Funcionalidades Principais

- Cadastro de Produtos, Fornecedores e Clientes  
- Fluxo de Pedidos (aprovação, separação, entrega)  
- Movimentação de Estoque (entradas e saídas)  
- Importação de NF-e via XML  
- API RESTful com Django REST Framework  
- Auditoria de ações e logs  
- Princípios de DDD aplicados (entidades, agregados, serviços, repositórios)

Tecnologias e Arquitetura

- Python 3.x, Django, Django REST Framework  
- Docker / docker-compose (opcional)  
- Postgres (ou outro banco relacional)  
- Redis para cache (planejado - opcional)  
- OpenAPI/Swagger para documentação interativa (opcional)  
- Estrutura DDD: `domain/`, `application/`, `infrastructure/` (ideal)

Instalação e Uso

1. Clone o repositório:  
   bash
   git clone https://seu.git.repo/sistema-patrimonial.git
   cd sistema-patrimonial
   
2. Crie o arquivo `.env` com as variáveis necessárias (`SECRET_KEY`, `DATABASE_URL`, etc.).  
3. Levante os serviços com Docker Compose:  
   bash
   docker-compose up --build
   
4. Acesse `http://localhost:8000/` e consulte a API em `/api/` ou a documentação em `/swagger/`.

Estrutura de Pastas (ideal)

.
├── README.md
├── domain/
│   └── models.py
├── application/
│   └── services.py
├── infrastructure/
│   ├── repositories.py
│   ├── views.py
│   └── serializers.py
├── core/
│   └── templatetags/
├── tests/
│   ├── unit/
│   └── integration/
└── docker-compose.yml


Testes

- Unitários:  
  bash
  docker-compose exec web pytest tests/unit
  
- Integração:  
  bash
  docker-compose exec web pytest tests/integration
  

## Próximos Passos

- Modularizar ainda mais seguindo DDD  
- Melhorias de performance e caching  
- Cobertura de testes ≥ 90%

