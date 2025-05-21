from typing import Any, Optional
from datetime import datetime
import ipaddress

from core.application.contracts.log_acao_service_contract import ILogAcaoService
from core.application.dtos.log_acao_dto import CreateLogAcaoDTO, LogAcaoDTO
from core.domain.entities.log_acao import LogAcao
from core.domain.repositories.log_acao_repository import ILogAcaoRepository
from infrastructure.repositories.django_log_acao_repository import DjangoLogAcaoRepository

class LogAcaoService(ILogAcaoService):
    def __init__(self, repo: ILogAcaoRepository = None):
        self.repo = repo or DjangoLogAcaoRepository()

    def create(self, dto: CreateLogAcaoDTO) -> LogAcaoDTO:
        # usuario_id
        if dto.usuario_id is not None:
            if not isinstance(dto.usuario_id, int) or dto.usuario_id < 1:
                raise ValueError("'usuario_id' deve ser inteiro positivo, se informado.")

        # acao (obrigatório)
        if not dto.acao or not isinstance(dto.acao, str) or not dto.acao.strip():
            raise ValueError("O campo 'acao' é obrigatório e não pode ser vazio.")
        acao = dto.acao.strip()[:255]

        # detalhes
        detalhes = dto.detalhes or ""
        if not isinstance(detalhes, str):
            raise ValueError("'detalhes' deve ser uma string.")
        detalhes = detalhes.strip()

        # data_hora
        if dto.data_hora is not None and not isinstance(dto.data_hora, datetime):
            raise ValueError("'data_hora' deve ser um datetime, se informado.")
        data_hora: Optional[datetime] = dto.data_hora

        # ip
        ip = dto.ip
        if ip is not None:
            if not isinstance(ip, str):
                raise ValueError("'ip' deve ser uma string.")
            try:
                ip = ip.strip()
                ipaddress.ip_address(ip)
            except ValueError:
                raise ValueError(f"'{ip}' não é um IP válido.")

        # monta entidade e persiste
        log = LogAcao(
            usuario_id=dto.usuario_id,
            acao=acao,
            detalhes=detalhes,
            data_hora=data_hora,
            ip=ip
        )
        criado = self.repo.save(log)

        return LogAcaoDTO(
            id=criado.id,
            usuario_id=criado.usuario_id,
            acao=criado.acao,
            detalhes=criado.detalhes,
            data_hora=criado.data_hora,
            ip=criado.ip
        )
