from core.application.contracts.item_pedido_service_contract import IItemPedidoService
from core.application.dtos.item_pedido_dto import CreateItemPedidoDTO, ItemPedidoDTO
from core.domain.repositories.item_pedido_repository import IItem_pedidoRepository
from infrastructure.repositories.django_item_pedido_repository import DjangoItem_pedidoRepository
from core.domain.entities.item_pedido import Item_pedido

class ItemPedidoService(IItemPedidoService):
    def __init__(self, repo: IItem_pedidoRepository = None):
        self.repo = repo or DjangoItem_pedidoRepository()

    def create(self, dto: CreateItemPedidoDTO) -> ItemPedidoDTO:
        # Aqui reaplicamos a mesma validação do antigo CriarItem_pedidoService
        # para manter as regras de negócio juntas no serviço.

        # pedido_id
        if dto.pedido_id < 1:
            raise ValueError("O campo 'pedido_id' deve ser um inteiro positivo.")
        # produto_id
        if dto.produto_id < 1:
            raise ValueError("O campo 'produto_id' deve ser um inteiro positivo.")
        # quantidade
        if dto.quantidade < 1:
            raise ValueError("O campo 'quantidade' deve ser > 0.")
        # liberado
        if dto.liberado is not None and dto.liberado < 0:
            raise ValueError("Se fornecido, 'liberado' deve ser >= 0.")
        # observacao
        if not isinstance(dto.observacao, str):
            raise ValueError("'observacao' deve ser uma string.")
        obs = dto.observacao.strip()[:255]
        # estoque_no_pedido
        if dto.estoque_no_pedido is not None and dto.estoque_no_pedido < 0:
            raise ValueError("Se fornecido, 'estoque_no_pedido' deve ser >= 0.")

        # monta entidade
        item = Item_pedido(
            pedido_id=dto.pedido_id,
            produto_id=dto.produto_id,
            quantidade=dto.quantidade,
            liberado=dto.liberado,
            observacao=obs,
            estoque_no_pedido=dto.estoque_no_pedido
        )
        criado = self.repo.save(item)

        return ItemPedidoDTO(
            id=criado.id,
            pedido_id=criado.pedido_id,
            produto_id=criado.produto_id,
            quantidade=criado.quantidade,
            liberado=criado.liberado,
            observacao=criado.observacao,
            estoque_no_pedido=criado.estoque_no_pedido
        )
