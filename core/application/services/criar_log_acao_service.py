from typing import Dict, Any, Optional
from datetime import datetime
import ipaddress

from core.domain.entities.log_acao import Log_acao
from core.domain.repositories.log_acao_repository import ILog_acaoRepository
from infrastructure.repositories.django_log_acao_repository import DjangoLog_acaoRepository

class CriarLog_acaoService:
    def __init__(self, repo: ILog_acaoRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoLog_acaoRepository()

    def execute(self, dados: Dict[str, Any]) -> Log_acao:
        """
        dados esperados:
          - usuario_id: int (opcional, >0)
          - acao: str (obrigatório, max_length=255)
          - detalhes: str (opcional)
          - data_hora: datetime (opcional)
          - ip: str (opcional, formato IPv4/IPv6)
        Retorna a entidade Log_acao recém-criada.
        """
        # valida usuario_id (se fornecido)
        usuario_id: Optional[int] = dados.get('usuario_id')
        if usuario_id is not None:
            if not isinstance(usuario_id, int) or usuario_id < 1:
                raise ValueError("'usuario_id' deve ser um inteiro positivo, se informado.")

        # valida acao
        acao = dados.get('acao')
        if not acao or not isinstance(acao, str) or not acao.strip():
            raise ValueError("O campo 'acao' é obrigatório e não pode ser vazio.")
        acao = acao.strip()[:255]

        # valida detalhes
        detalhes = dados.get('detalhes', '')
        if detalhes is None:
            detalhes = ''
        elif not isinstance(detalhes, str):
            raise ValueError("'detalhes' deve ser uma string.")
        detalhes = detalhes.strip()

        # valida data_hora
        data_hora: Optional[datetime] = dados.get('data_hora')
        if data_hora is not None:
            if not isinstance(data_hora, datetime):
                raise ValueError("'data_hora' deve ser um objeto datetime.")

        # valida ip (se fornecido)
        ip: Optional[str] = dados.get('ip')
        if ip is not None:
            if not isinstance(ip, str):
                raise ValueError("'ip' deve ser uma string.")
            try:
                # valida formato de endereço IP
                ipaddress.ip_address(ip.strip())
                ip = ip.strip()
            except ValueError:
                raise ValueError(f"'{ip}' não é um endereço IP válido.")

        # monta a entidade de domínio
        log = Log_acao(
            usuario_id=usuario_id,
            acao=acao,
            detalhes=detalhes,
            data_hora=data_hora,
            ip=ip
        )

        # persiste e retorna
        return self.repo.save(log)
