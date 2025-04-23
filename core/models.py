from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.conf import settings
from django.db.models import Max, Sum
from django.db import transaction
from datetime import date, datetime


# --- USUÁRIO ---
class Usuario(AbstractUser):
    matricula = models.CharField(
        "Matrícula",
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )
    papel = models.CharField(
        max_length=20,
        choices=[("admin", "Admin"), ("operador", "Operador"), ("tecnico", "Técnico")],
        default="operador"
    )
    ativo = models.BooleanField(default=True)
    areas = models.ManyToManyField("Area", blank=True, related_name="usuarios")
    groups = models.ManyToManyField(Group, related_name="usuarios_grupo", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="usuarios_permissao", blank=True)

    def __str__(self):
        return self.username

    @property
    def todas_areas(self):
        """
        Retorna todas as áreas se for admin ou técnico,
        senão retorna apenas as áreas associadas.
        """
        if self.papel in ['admin', 'tecnico']:
            return Area.objects.all()
        return self.areas.all()

# --- ÁREA ---
class Area(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


# --- FORNECEDOR ---
class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, blank=True, null=True)
    endereco = models.TextField(blank=True)
    telefone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


PENDING_STATUSES = ['aguardando_aprovacao', 'aprovado', 'separado']

class Produto(models.Model):
    nfe_numero = models.CharField("NFe Nº", max_length=20, blank=True, null=True)
    codigo_barras = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255)
    fornecedor = models.ForeignKey('Fornecedor', on_delete=models.CASCADE)
    area = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True, blank=True)
    lote = models.PositiveIntegerField(editable=False)
    validade = models.DateField(blank=True, null=True)

    quantidade = models.PositiveIntegerField(
        verbose_name="Quantidade Atual",
        default=0,
        help_text="Estoque bruto cadastrado"
    )
    quantidade_inicial = models.PositiveIntegerField(
        verbose_name="Quantidade Cadastrada",
        default=0,
        help_text="Não é alterado após criação"
    )

    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=10,
        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
        default="ativo"
    )
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            # Define o próximo lote
            ultimo = Produto.objects.filter(
                codigo_barras=self.codigo_barras
            ).aggregate(max_lote=Max('lote'))['max_lote'] or 0
            self.lote = ultimo + 1
            # Na criação, fixa quantidade_inicial
            self.quantidade_inicial = self.quantidade
        super().save(*args, **kwargs)

    def __str__(self):
        nfe = f" (NFe Nº {self.nfe_numero})" if self.nfe_numero else ""
        return f"{self.descricao} - {self.codigo_barras} - Lote {self.lote}{nfe}"

    @property
    def estoque_total(self):
        # Soma de quantidade atual em todos os lotes desse código+área
        resultado = Produto.objects.filter(
            codigo_barras=self.codigo_barras,
            area=self.area
        ).aggregate(total=Sum('quantidade'))
        return resultado['total'] or 0

    @property
    def estoque_minimo(self):
        if not self.area_id:
            return 0
        from .models import ConfiguracaoEstoque
        cfg = ConfiguracaoEstoque.objects.filter(area_id=self.area_id).first()
        return cfg.estoque_minimo if cfg else 0

    def estoque_info(self, data_limite=None):
        """
        Retorna um dict com:
          - real: estoque físico atual (lotes - saídas entregues)
          - reservado: total em pedidos ainda não entregues
          - disponivel: real - reservado
        """
        # 1) Total de lotes
        total_lotes = (
            Produto.objects
                   .filter(codigo_barras=self.codigo_barras, area=self.area)
                   .aggregate(total_lotes=Sum('quantidade'))
                   .get('total_lotes') or 0
        )

        # 2) Saídas entregues
        from .models import SaidaProdutoPorPedido
        saidas_qs = SaidaProdutoPorPedido.objects.filter(
            produto=self, pedido__status='entregue'
        )
        if data_limite:
            saidas_qs = saidas_qs.filter(pedido__data_aprovacao__date__lte=data_limite)
        total_saidas = saidas_qs.aggregate(total_saidas=Sum('quantidade'))['total_saidas'] or 0

        estoque_real = max(total_lotes - total_saidas, 0)

        # 3) Reservas não entregues
        from .models import ItemPedido
        reservas_qs = ItemPedido.objects.filter(produto=self).exclude(pedido__status='entregue')
        if data_limite:
            reservas_qs = reservas_qs.filter(pedido__data_solicitacao__date__lte=data_limite)
        total_reservas = reservas_qs.aggregate(total_reservas=Sum('quantidade'))['total_reservas'] or 0

        # 4) Disponível projetado
        disponivel = max(estoque_real - total_reservas, 0)

        return {
            'real':      estoque_real,
            'reservado': total_reservas,
            'disponivel': disponivel
        }

    def estoque_disponivel(self, data_limite=None):
        """
        Compatibilidade com view/template antigos:
        - se data_limite for passado, devolve o dict completo;
        - caso contrário, só o int disponivel.
        """
        info = self.estoque_info(data_limite)
        if data_limite is not None:
            return info
        return info['disponivel']
    

class Cliente(models.Model):
    matricula = models.CharField(max_length=50, unique=True)
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    curso = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_completo


class NFe(models.Model):
    numero = models.CharField(max_length=50, unique=True)
    data_emissao = models.DateField()
    cnpj_fornecedor = models.CharField(max_length=14)
    peso = models.FloatField()
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    itens_vinculados = models.ManyToManyField(Produto)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"NF {self.numero}"


class MovimentacaoEstoque(models.Model):
    TIPO_MOVIMENTACAO = [("entrada", "Entrada"), ("saida", "Saída")]
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMENTACAO)
    data = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nota_fiscal = models.ForeignKey(NFe, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo.upper()} - {self.produto} ({self.quantidade})"


class LogAcao(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    acao = models.CharField(max_length=255)
    detalhes = models.TextField(blank=True)
    data_hora = models.DateTimeField(default=timezone.now)
    ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario} - {self.acao} em {self.data_hora.strftime('%d/%m/%Y %H:%M:%S')}"


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('aguardando_aprovacao', 'Aguardando Aprovação'),
        ('aprovado', 'Aprovado (Aguardando Separação)'),
        ('separado', 'Separado'),
        ('entregue', 'Entregue'),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos')
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='aguardando_aprovacao')
    aprovado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='pedidos_aprovados')
    data_separacao = models.DateTimeField(null=True, blank=True)
    data_retirada = models.DateTimeField(null=True, blank=True)
    retirado_por = models.CharField(max_length=100, null=True, blank=True)
    observacao = models.TextField(blank=True, null=True)
    data_necessaria = models.DateField(null=True, blank=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    

    def aprovar(self, usuario_aprovador):
        """
        Só marca como aprovado e armazena quem aprovou.
        Não altera Produto.quantidade aqui.
        """
        if self.status == 'aguardando_aprovacao':
            self.status        = 'aprovado'
            self.aprovado_por  = usuario_aprovador
            self.data_aprovacao = timezone.now()
            self.save()

    def marcar_como_separado(self):
        """
        Apenas avança para 'separado', sem mexer no estoque.
        """
        if self.status == 'aprovado':
            self.status         = 'separado'
            self.data_separacao = timezone.now()
            self.save()

    def registrar_retirada(self, nome_retirado_por):
        
        if self.status != 'separado':
            return
    
        with transaction.atomic():
            for item in self.itens.all():
                restante = item.liberado or item.quantidade

                lotes = Produto.objects.filter(
                    codigo_barras=item.produto.codigo_barras,
                    area=item.produto.area,
                    quantidade__gt=0
                ).order_by('validade', 'criado_em')

                for lote in lotes:
                    if restante <= 0:
                        break

                    disponivel_lote = lote.quantidade

                    if disponivel_lote >= restante:
                        lote.quantidade -= restante
                        lote.save(update_fields=['quantidade'])
                        SaidaProdutoPorPedido.objects.create(
                            produto=lote,
                            pedido=self,
                            quantidade=restante
                        )
                        restante = 0
                    else:
                        lote.quantidade = 0
                        lote.save(update_fields=['quantidade'])
                        SaidaProdutoPorPedido.objects.create(
                            produto=lote,
                            pedido=self,
                            quantidade=disponivel_lote
                        )
                        restante -= disponivel_lote

                if restante > 0:
                    raise ValueError(
                        f"Estoque insuficiente ao retirar {item.produto.descricao}"
                    )

            # só depois de tudo ter saído com sucesso:
            self.status        = 'entregue'
            self.retirado_por  = nome_retirado_por
            self.data_retirada = timezone.now()
            self.save()



class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    liberado = models.IntegerField(null=True, blank=True)
    observacao = models.CharField(max_length=255, blank=True)

    # Novo campo persistente
    estoque_no_pedido = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Estoque disponível no momento do pedido"
    )

    def __str__(self):
        return f"{self.quantidade}x {self.produto.descricao}"

    @property
    def estoque_disponivel(self):
        return self.estoque_no_pedido if self.estoque_no_pedido is not None else self.produto.estoque_disponivel(self.pedido.data_solicitacao)



class SubItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="subitens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    # Campo para registrar o estoque no momento do pedido
    estoque_no_pedido = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Estoque disponível no momento do pedido"
    )

    def __str__(self):
        return f"{self.produto.descricao} x{self.quantidade}"

    @property
    def estoque_disponivel(self):
        return self.estoque_no_pedido if self.estoque_no_pedido is not None else self.produto.estoque_disponivel(self.pedido.data_solicitacao)



    def __str__(self):
        return f"{self.produto.descricao} x{self.quantidade}"

class SaidaProdutoPorPedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_saida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.descricao} (Pedido {self.pedido.codigo})"

class ConfiguracaoEstoque(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    estoque_minimo = models.PositiveIntegerField()

    class Meta:
        unique_together = ('area',)

    def __str__(self):
        return f"{'Geral' if not self.area else self.area.nome} - Mínimo: {self.estoque_minimo}"

class SessionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_key  = models.CharField("Chave de Sessão", max_length=40)
    login_time   = models.DateTimeField("Login em")
    logout_time  = models.DateTimeField("Logout em", null=True, blank=True)
    duration     = models.DurationField("Duração da Sessão", null=True, blank=True)
    ip           = models.GenericIPAddressField("Endereço IP", null=True, blank=True)

    class Meta:
        ordering = ['-login_time']
        verbose_name = "Log de Sessão"
        verbose_name_plural = "Logs de Sessão"

    def save(self, *args, **kwargs):
        # calcula duration quando tiver logout_time
        if self.logout_time and not self.duration:
            self.duration = self.logout_time - self.login_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} — {self.login_time.strftime('%d/%m/%Y %H:%M')}"
    
    
