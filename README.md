# Gestão Patrimonial

Este repositório contém uma aplicação Django para controle patrimonial. O projeto pode ser executado localmente com Docker, mas também está preparado para implantação em produção.

## Configuração

1. Copie `.env.example` para `.env` e ajuste os valores.
2. Defina `DEBUG=False` e preencha `ALLOWED_HOSTS` com o domínio desejado ao hospedar na internet.
3. Execute `docker-compose up --build` para iniciar.

Para mais detalhes consulte `core/README.md`.
