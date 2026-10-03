from typing import Any, Dict, List, Optional
from cliente import Cliente
from atendente import Atendente
from fila import Fila
from politicas import PoliticaAtendimento, criar_politica
from estatisticas import Estatisticas


class CentralAtendimento:
    """
    Coordenador principal da simulação.
    Gerencia o fluxo de clientes, aloca os guichês/atendentes disponíveis,
    avança a simulação a cada tick e calcula as métricas do sistema.
    """

    def __init__(self, atendentes: List[Atendente], politica: str = "fifo", verbose: bool = False):
        self._atendentes = atendentes
        self._verbose = verbose

        # Instancia a política de atendimento selecionada (FIFO ou Prioridade)
        self._politica: PoliticaAtendimento = criar_politica(politica)

        # Utiliza estritamente a classe Fila própria para ambas as filas
        self._fila_comum = Fila()
        self._fila_prioritaria = Fila()

        # Registos históricos para métricas
        self._clientes_que_chegaram: List[Cliente] = []
        self._clientes_atendidos: List[Cliente] = []

        # Histórico do tamanho combinado das filas a cada tick (para a média)
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

    def receber_cliente(self, cliente: Cliente) -> None:
        """Adiciona o cliente à fila correspondente de acordo com a política."""
        self._clientes_que_chegaram.append(cliente)
        self._politica.enfileirar(cliente, self._fila_comum, self._fila_prioritaria)

        if self._verbose:
            nome_fila = "prioritária" if cliente.eh_prioritario else "comum"
            print(f"[{self._tempo_decorrido:03d}] Cliente {cliente.id} [{cliente.tipo}] chegou ao sistema")
            print(f"[{self._tempo_decorrido:03d}] Cliente {cliente.id} entrou na fila {nome_fila}")

    def obter_proximo_cliente(self) -> Optional[Cliente]:
        """Solicita à política ativa o próximo cliente a ser atendido."""
        return self._politica.proximo_cliente(self._fila_comum, self._fila_prioritaria)

    def tamanho_total_filas(self) -> int:
        """Retorna a soma do número de clientes em ambas as filas."""
        return self._fila_comum.tamanho() + self._fila_prioritaria.tamanho()

    def processar_tick(self, novos_clientes: List[Cliente]) -> None:
        """Executa a sequência de eventos de uma unidade discreta de tempo (tick)."""
        # 1. Entrada de novos clientes
        for cliente in novos_clientes:
            self.receber_cliente(cliente)

        # 2. Atualização dos atendimentos em andamento e conclusão
        for atendente in self._atendentes:
            cliente_concluido = atendente.processar_unidade_tempo()
            if cliente_concluido is not None:
                cliente_concluido.registrar_fim_atendimento(self._tempo_decorrido)
                self._clientes_atendidos.append(cliente_concluido)
                if self._verbose:
                    print(f"[{self._tempo_decorrido:03d}] Cliente {cliente_concluido.id} terminou o atendimento no Atendente {atendente.id}")

        # 3. Início de novos atendimentos nos guichês livres
        for atendente in self._atendentes:
            if atendente.esta_livre():
                proximo = self.obter_proximo_cliente()
                if proximo is not None:
                    atendente.iniciar_atendimento(proximo, tempo_atual=self._tempo_decorrido)
                    if self._verbose:
                        print(f"[{self._tempo_decorrido:03d}] Atendente {atendente.id} iniciou atendimento do Cliente {proximo.id}")

        # 4. Registo de estado da fila neste tick
        self._historico_tamanho_fila.append(self.tamanho_total_filas())
        self._tempo_decorrido += 1

    def calcular_metricas(self) -> Dict[str, Any]:
        """Delega o fechamento das contas para Estatisticas."""
        return Estatisticas.calcular(self)
