from typing import Optional


# Pessoa na simulação. Chegada e duração nascem prontas; início e fim a Central que carimba.
class Cliente:

    # grafias que a política trata como prioritário; 
    _TIPOS_PRIORITARIOS = ("prioritario", "prioritaria", "prioritária")

    def __init__(self, id_cliente, tipo: str, tempo_chegada: int, tempo_duracao: int):
        tipo_normalizado = tipo.strip().lower()
        if not tipo_normalizado:
            raise ValueError("O tipo do cliente não pode ser vazio.")
        if tempo_chegada < 0:
            raise ValueError("O tempo de chegada não pode ser negativo.")
        if tempo_duracao <= 0:
            raise ValueError("A duração do atendimento deve ser maior que zero.")

        self._id = id_cliente
        self._tipo = tipo_normalizado
        self._tempo_chegada = tempo_chegada
        self._tempo_duracao = tempo_duracao
        self._tempo_inicio_atendimento: Optional[int] = None
        self._tempo_fim_atendimento: Optional[int] = None

    @property
    def id(self):
        return self._id

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def tempo_chegada(self) -> int:
        return self._tempo_chegada

    @property
    def tempo_duracao(self) -> int:
        return self._tempo_duracao

    @property
    def tempo_inicio_atendimento(self) -> Optional[int]:
        return self._tempo_inicio_atendimento

    @property
    def tempo_fim_atendimento(self) -> Optional[int]:
        return self._tempo_fim_atendimento

    # Único lugar que define quem fura fila. Usado pela política de prioridade.
    @property
    def eh_prioritario(self) -> bool:
        return self._tipo in self._TIPOS_PRIORITARIOS

    def registrar_inicio_atendimento(self, tempo_atual: int) -> None:
        if tempo_atual < self._tempo_chegada:
            raise ValueError("O início do atendimento não pode ser anterior ao tempo de chegada.")
        self._tempo_inicio_atendimento = tempo_atual

    def registrar_fim_atendimento(self, tempo_atual: int) -> None:
        if self._tempo_inicio_atendimento is None:
            raise RuntimeError("Não é possível finalizar um atendimento que não foi iniciado.")
        if tempo_atual < self._tempo_inicio_atendimento:
            raise ValueError("O fim do atendimento não pode ser anterior ao seu início.")
        self._tempo_fim_atendimento = tempo_atual

    # Espera na fila = início − chegada. Só existe depois que sentou no guichê.
    def get_tempo_espera(self) -> int:
        if self._tempo_inicio_atendimento is None:
            raise RuntimeError(f"Cliente {self._id} ainda não iniciou o atendimento.")
        return self._tempo_inicio_atendimento - self._tempo_chegada

    # Tempo no sistema = fim − chegada. Só existe depois que o atendimento acabou.
    def get_tempo_total_sistema(self) -> int:
        if self._tempo_fim_atendimento is None:
            raise RuntimeError(f"Cliente {self._id} ainda não finalizou o atendimento.")
        return self._tempo_fim_atendimento - self._tempo_chegada
