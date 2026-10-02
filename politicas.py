from typing import Optional
from cliente import Cliente
from fila import Fila

#Não tem construtor porque não há atributo comum entre as classes filhas
class PoliticaAtendimento:
    """Classe base (interface) para as políticas de atendimento."""
    def enfileirar(self, cliente: Cliente, fila_comum: Fila, fila_prioritaria: Fila) -> None:
        raise NotImplementedError

    def proximo_cliente(self, fila_comum: Fila, fila_prioritaria: Fila) -> Optional[Cliente]:
        raise NotImplementedError


class PoliticaFIFO(PoliticaAtendimento):
    """Política A — FIFO: Todos entram na fila comum e são atendidos por ordem de chegada."""

    def enfileirar(self, cliente: Cliente, fila_comum: Fila, fila_prioritaria: Fila) -> None:
        fila_comum.enfileira(cliente)

    def proximo_cliente(self, fila_comum: Fila, fila_prioritaria: Fila) -> Optional[Cliente]:
        if not fila_comum.vazia():
            return fila_comum.desinfileira()
        return None


class PoliticaPrioridade(PoliticaAtendimento):
    """
    Política B — Prioridade com Anti-Starvation.
    Atende até 'max_prioritarios' consecutivos antes de forçar o atendimento de 1 comum.
    """

    def __init__(self, max_prioritarios_consecutivos: int = 3):
        self.max_prioritarios = max_prioritarios_consecutivos
        self.consecutivos_prioritarios = 0

    def enfileirar(self, cliente: Cliente, fila_comum: Fila, fila_prioritaria: Fila) -> None:
        if cliente.eh_prioritario:
            fila_prioritaria.enfileira(cliente)
        else:
            fila_comum.enfileira(cliente)

    def proximo_cliente(self, fila_comum: Fila, fila_prioritaria: Fila) -> Optional[Cliente]:
        # Se ambas estiverem vazias
        if fila_prioritaria.vazia() and fila_comum.vazia():
            return None

        # Regra Anti-Starvation: se atingiu o limite de prioritários seguidos e há cliente comum aguardando
        if self.consecutivos_prioritarios >= self.max_prioritarios and not fila_comum.vazia():
            self.consecutivos_prioritarios = 0
            return fila_comum.desinfileira()

        # Atende da fila prioritária se houver cliente
        if not fila_prioritaria.vazia():
            self.consecutivos_prioritarios += 1
            return fila_prioritaria.desinfileira()

        # Se não há prioritários, atende da fila comum
        if not fila_comum.vazia():
            self.consecutivos_prioritarios = 0
            return fila_comum.desinfileira()

        return None


def criar_politica(nome_politica: str) -> PoliticaAtendimento:
    """Factory para instanciar a política correta com base no argumento do CLI."""
    nome = nome_politica.lower()
    if nome == "fifo":
        return PoliticaFIFO()
    elif nome in ["prioridade", "priority"]:
        return PoliticaPrioridade(max_prioritarios_consecutivos=3)
    else:
        raise ValueError(f"Política desconhecida: {nome_politica}")