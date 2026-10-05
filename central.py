from typing import Any, Dict, List, Optional
from cliente import Cliente
from atendente import Atendente
from fila import Fila
from politicas import PoliticaAtendimento, criar_politica
from estatisticas import Estatisticas


# Um tick: chega cliente, termina atendimento, ocupa mesa livre, anota a fila.
class CentralAtendimento:

    def __init__(self, atendentes: List[Atendente], politica: str = "fifo", verbose: bool = False):
        self._atendentes = atendentes
        self._verbose = verbose
        self._politica: PoliticaAtendimento = criar_politica(politica)

        # duas Filas da disciplina; a política decide em qual o cliente entra
        self._fila_comum = Fila()
        self._fila_prioritaria = Fila()

        self._clientes_que_chegaram: List[Cliente] = []
        self._clientes_atendidos: List[Cliente] = []
        self._historico_tamanho_fila: List[int] = []
        self._tempo_decorrido: int = 0

    @property
    def atendentes(self):
        return self._atendentes

    @property
    def verbose(self):
        return self._verbose

    @property
    def politica(self):
        return self._politica

    @property
    def fila_comum(self):
        return self._fila_comum

    @property
    def fila_prioritaria(self):
        return self._fila_prioritaria

    @property
    def clientes_que_chegaram(self):
        return self._clientes_que_chegaram

    @property
    def clientes_atendidos(self):
        return self._clientes_atendidos

    @property
    def historico_tamanho_fila(self):
        return self._historico_tamanho_fila

    @property
    def tempo_decorrido(self):
        return self._tempo_decorrido

    # Enfileira o cliente (a política escolhe a fila) e guarda que ele chegou.
    def receber_cliente(self, cliente: Cliente) -> None:
        self._clientes_que_chegaram.append(cliente)
        self._politica.enfileirar(cliente, self._fila_comum, self._fila_prioritaria)

        if self._verbose:
            nome_fila = "prioritária" if cliente.eh_prioritario else "comum"
            print(f"[{self._tempo_decorrido:03d}] Cliente {cliente.id} [{cliente.tipo}] chegou ao sistema")
            print(f"[{self._tempo_decorrido:03d}] Cliente {cliente.id} entrou na fila {nome_fila}")

    # Pergunta à política quem sai da fila agora.
    def obter_proximo_cliente(self) -> Optional[Cliente]:
        return self._politica.proximo_cliente(self._fila_comum, self._fila_prioritaria)

    def tamanho_total_filas(self) -> int:
        return self._fila_comum.tamanho() + self._fila_prioritaria.tamanho()

    # Ordem do minuto: chega → termina → senta quem está livre → anota a fila.
    def processar_tick(self, novos_clientes: List[Cliente]) -> None:
        for cliente in novos_clientes:
            self.receber_cliente(cliente)

        # termina antes de puxar o próximo, senão a mesa nunca fica livre neste tick
        for atendente in self._atendentes:
            cliente_concluido = atendente.processar_unidade_tempo()
            if cliente_concluido is not None:
                cliente_concluido.registrar_fim_atendimento(self._tempo_decorrido)
                self._clientes_atendidos.append(cliente_concluido)
                if self._verbose:
                    print(f"[{self._tempo_decorrido:03d}] Cliente {cliente_concluido.id} terminou o atendimento no Atendente {atendente.id}")

        for atendente in self._atendentes:
            if atendente.esta_livre():
                proximo = self.obter_proximo_cliente()
                if proximo is not None:
                    atendente.iniciar_atendimento(proximo, tempo_atual=self._tempo_decorrido)
                    if self._verbose:
                        print(f"[{self._tempo_decorrido:03d}] Atendente {atendente.id} iniciou atendimento do Cliente {proximo.id}")

        # tamanho no fim do tick (quem sentou agora já saiu da fila)
        self._historico_tamanho_fila.append(self.tamanho_total_filas())
        self._tempo_decorrido += 1

    # A Central só guarda histórico; quem fecha as contas é Estatisticas.
    def calcular_metricas(self) -> Dict[str, Any]:
        return Estatisticas.calcular(self)
