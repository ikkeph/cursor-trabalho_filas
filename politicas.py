from typing import Optional
from cliente import Cliente
from fila import Fila


# Interface das políticas: em qual fila entra e de qual fila sai.
# Sem estado comum, por isso não tem __init__.
class PoliticaAtendimento:

    def enfileirar(self, cliente: Cliente, fila_comum: Fila, fila_prioritaria: Fila) -> None:
        raise NotImplementedError

    def proximo_cliente(self, fila_comum: Fila, fila_prioritaria: Fila) -> Optional[Cliente]:
        raise NotImplementedError


# Todo mundo na fila comum, ordem de chegada. A prioritária fica vazia.
class PoliticaFIFO(PoliticaAtendimento):

    def enfileirar(self, cliente: Cliente, fila_comum: Fila, fila_prioritaria: Fila) -> None:
        fila_comum.enfileira(cliente)

    def proximo_cliente(self, fila_comum: Fila, fila_prioritaria: Fila) -> Optional[Cliente]:
        if not fila_comum.vazia():
            return fila_comum.desinfileira()
        return None


# Prioritário na fila dele; depois de 3 seguidos, atende 1 comum se houver.
class PoliticaPrioridade(PoliticaAtendimento):

    def __init__(self, max_prioritarios_consecutivos: int = 3):
        self.max_prioritarios = max_prioritarios_consecutivos
        self.consecutivos_prioritarios = 0

    def enfileirar(self, cliente: Cliente, fila_comum: Fila, fila_prioritaria: Fila) -> None:
        if cliente.eh_prioritario:
            fila_prioritaria.enfileira(cliente)
        else:
            fila_comum.enfileira(cliente)

    def proximo_cliente(self, fila_comum: Fila, fila_prioritaria: Fila) -> Optional[Cliente]:
        if fila_prioritaria.vazia() and fila_comum.vazia():
            return None

        # anti-starvation: 3 prioritários seguidos e tem comum esperando → comum
        if self.consecutivos_prioritarios >= self.max_prioritarios and not fila_comum.vazia():
            self.consecutivos_prioritarios = 0
            return fila_comum.desinfileira()

        if not fila_prioritaria.vazia():
            self.consecutivos_prioritarios += 1
            return fila_prioritaria.desinfileira()

        # só comuns na fila (o contador zera)
        if not fila_comum.vazia():
            self.consecutivos_prioritarios = 0
            return fila_comum.desinfileira()

        return None


# Devolve FIFO ou Prioridade a partir da string do argparse.
def criar_politica(nome_politica: str) -> PoliticaAtendimento:
    nome = nome_politica.lower()
    if nome == "fifo":
        return PoliticaFIFO()
    elif nome in ["prioridade", "priority"]:
        return PoliticaPrioridade(max_prioritarios_consecutivos=3)
    else:
        raise ValueError(f"Política desconhecida: {nome_politica}")
