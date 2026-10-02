from typing import Optional


class Cliente:
    """
    Representa um cliente no sistema de simulação de atendimento.
 
    Os atributos são privados (convenção ``_atributo``) e expostos por
    ``@property`` somente leitura. O estado do atendimento só é alterado
    pelos métodos ``registrar_inicio_atendimento`` e
    ``registrar_fim_atendimento``, que preservam as validações.
 
    Propriedades:
        id: Identificador único do cliente.
        tipo: Tipo de atendimento, normalizado em minúsculas
            (ex: 'comum', 'prioritario', 'tecnico').
        tempo_chegada: Instante (tick) em que o cliente entra no sistema.
        tempo_duracao: Tempo necessário para concluir o atendimento.
        tempo_inicio_atendimento: Instante em que o atendimento começa
            (None enquanto o cliente aguarda).
        tempo_fim_atendimento: Instante em que o atendimento termina
            (None enquanto não concluído).
    """
 
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
 
        # Atributos atualizados ao longo do ciclo de vida
        self._tempo_inicio_atendimento: Optional[int] = None
        self._tempo_fim_atendimento: Optional[int] = None
 
    # ------------------------------------------------------------------
    # Acesso somente leitura aos atributos
    # ------------------------------------------------------------------
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
 
    @property
    def eh_prioritario(self) -> bool:
        """Única definição de 'cliente prioritário' do sistema (usada pelas políticas)."""
        return self._tipo in self._TIPOS_PRIORITARIOS
 
    # ------------------------------------------------------------------
    # Mudanças de estado
    # ------------------------------------------------------------------
    def registrar_inicio_atendimento(self, tempo_atual: int) -> None:
        """Registra o momento em que o cliente sai da fila e começa a ser atendido."""
        if tempo_atual < self._tempo_chegada:
            raise ValueError("O início do atendimento não pode ser anterior ao tempo de chegada.")
        self._tempo_inicio_atendimento = tempo_atual
 
    def registrar_fim_atendimento(self, tempo_atual: int) -> None:
        """Registra o momento em que o atendimento é concluído."""
        if self._tempo_inicio_atendimento is None:
            raise RuntimeError("Não é possível finalizar um atendimento que não foi iniciado.")
        if tempo_atual < self._tempo_inicio_atendimento:
            raise ValueError("O fim do atendimento não pode ser anterior ao seu início.")
        self._tempo_fim_atendimento = tempo_atual
 
    # ------------------------------------------------------------------
    # Valores calculados (métodos, pois podem levantar exceção)
    # ------------------------------------------------------------------
    def get_tempo_espera(self) -> int:
        """
        Retorna o tempo total gasto na fila (início do atendimento - chegada).
        Levanta RuntimeError se o atendimento ainda não tiver iniciado.
        """
        if self._tempo_inicio_atendimento is None:
            raise RuntimeError(f"Cliente {self._id} ainda não iniciou o atendimento.")
        return self._tempo_inicio_atendimento - self._tempo_chegada
 
    def get_tempo_total_sistema(self) -> int:
        """
        Retorna o tempo total de permanência no sistema (fim - chegada).
        Levanta RuntimeError se o atendimento ainda não tiver terminado.
        """
        if self._tempo_fim_atendimento is None:
            raise RuntimeError(f"Cliente {self._id} ainda não finalizou o atendimento.")
        return self._tempo_fim_atendimento - self._tempo_chegada
 
    def __repr__(self) -> str:
        return (
            f"Cliente(id={self._id!r}, tipo={self._tipo!r}, "
            f"chegada={self._tempo_chegada}, duracao={self._tempo_duracao})"
        )
 
    def __str__(self) -> str:
        return f"Cliente {self._id} [{self._tipo}]"
 