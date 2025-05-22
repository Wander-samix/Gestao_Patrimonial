from enum import Enum

class PendingStatus(Enum):
    AGUARDANDO = "aguardando"
    APROVADO   = "aprovado"
    REJEITADO  = "rejeitado"
    CANCELADO  = "cancelado"

# Um helper para labels (opcional)
pending_statuses = {
    PendingStatus.AGUARDANDO: "Aguardando",
    PendingStatus.APROVADO:   "Aprovado",
    PendingStatus.REJEITADO:  "Rejeitado",
    PendingStatus.CANCELADO:  "Cancelado",
}
