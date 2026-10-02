from typing import List, Optional
from cliente import Cliente


class Atendente:
    """
    Representa um servidor ou guichê de atendimento.
    
    Atributos:
        id (int/str): Identificador único do atendente.
        tipos_atendimento (Optional[List[str]]): Tipos de atendimento que este guichê realiza.
                                             Se None ou vazio, atende qualquer tipo.
        cliente_atual (Optional[Cliente]): Cliente em atendimento no momento.
        tempo_restante (int): Quantidade de unidades de tempo restantes para terminar
                              o atendimento do cliente atual.
        total_clientes_atendidos (int): Quantidade acumulada de clientes finalizados.
        tempo_total_ocupado (int): Total de unidades de tempo em que esteve ocupado.
    """

    def __init__(self, id_atendente, tipos_atendimento: Optional[List[str]] = None):
        self._id = id_atendente
        self._tipos_atendimento = [t.strip().lower() for t in tipos_atendimento] if tipos_atendimento else []
        
        # Estado do atendente
        self._cliente_atual: Optional[Cliente] = None
        self._tempo_restante: int = 0
        
        # Métricas individuais
       
        self._total_clientes_atendidos: int = 0
        self._tempo_total_ocupado: int = 0

    @property
    def id(self):
        return self._id

    @property
    def tipos_atendimento(self):
        return self._tipos_atendimento

    @property
    def cliente_atual(self):
        return self._cliente_atual

    @property
    def tempo_restante(self):
        return self._tempo_restante

    @property
    def total_clientes_atendidos(self):
        return self._total_clientes_atendidos

    @property
    def tempo_total_ocupado(self):
        return self._tempo_total_ocupado

    def esta_livre(self) -> bool:
        """Retorna True se o atendente não estiver com nenhum cliente no momento."""
        return self._cliente_atual is None

    def pode_atender(self, tipo_cliente: str) -> bool:
        """
        Verifica se o atendente é capacitado para o tipo de atendimento solicitado.
        Se a lista de tipos do atendente for vazia, assume-se que atende a todos os tipos.
        """
        if not self._tipos_atendimento:
            return True
        return tipo_cliente.strip().lower() in self.tipos_atendimento

    def iniciar_atendimento(self, cliente: Cliente, tempo_atual: int) -> None:
        """
        Associa um cliente ao atendente e registra o tempo de início no cliente.
        
        Lança exceção se o atendente já estiver ocupado.
        """
        if not self.esta_livre():
            raise RuntimeError(f"Atendente {self._id} já está ocupado com o Cliente {self._cliente_atual.id}.")

        self._cliente_atual = cliente
        self._tempo_restante = cliente.tempo_duracao
        
        # Atualiza o estado do próprio cliente
        cliente.registrar_inicio_atendimento(tempo_atual)

    def processar_unidade_tempo(self) -> Optional[Cliente]:
        """
        Avança 1 unidade de tempo (tick) na simulação.
        
        Se houver cliente sendo atendido:
        - Decrementa o tempo restante;
        - Soma 1 ao tempo total ocupado;
        - Se o tempo restante chegar a 0, finaliza o atendimento e retorna o Cliente concluído;
        - Caso contrário, retorna None.
        
        Se estiver livre, apenas retorna None.
        """
        if self.esta_livre():
            return None

        self._tempo_total_ocupado += 1
        self._tempo_restante -= 1

        # Atendimento concluído neste tick
        if self._tempo_restante == 0:
            return self.finalizar_atendimento()

        return None

    def finalizar_atendimento(self) -> Cliente:
        """
        Finaliza o atendimento do cliente atual, limpa o estado do atendente
        e incrementa o número total de atendimentos concluídos.
        """
        if self._cliente_atual is None:
            raise RuntimeError(f"Atendente {self.id} tentou finalizar atendimento sem nenhum cliente ativo.")

        cliente_concluido = self._cliente_atual
        self._total_clientes_atendidos += 1
        
        # O tempo final será definido pela CentralAtendimento no tick atual
        self._cliente_atual = None
        self._tempo_restante = 0

        return cliente_concluido

    def calcular_taxa_utilizacao(self, tempo_total_simulacao: int) -> float:
        """
        Calcula a porcentagem de utilização do atendente em relação ao tempo da simulação.
        """
        if tempo_total_simulacao <= 0:
            return 0.0
        return (self._tempo_total_ocupado / tempo_total_simulacao) * 100.0

    # método de representação
    def __repr__(self) -> str:
        status = f"Ocupado (Restante: {self._tempo_restante})" if not self.esta_livre() else "Livre"
        return f"Atendente(id={self._id!r}, status={status!r})"

    def __str__(self) -> str:
        return f"Atendente {self._id}"


