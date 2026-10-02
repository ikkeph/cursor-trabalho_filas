import random
from atendente import Atendente
from central import CentralAtendimento
from configuracao import Configuracao
from gerador_clientes import GeradorClientes
from relatorio import Relatorio

class Simulacao:
    def __init__(self, config: Configuracao):
        self.config = config
        if config.seed is not None:
            random.seed(config.seed)

        self.agenda = GeradorClientes.criar_agenda(config)
        self.atendentes = [Atendente(id_atendente=i + 1) for i in range(config.atendentes)]
        self.central = CentralAtendimento(
            atendentes=self.atendentes,
            politica=config.politica,
            verbose=config.verbose
        )

    def executar(self) -> None:
        if self.config.modo == "arquivo":
            tempo_limite = max(self.agenda.keys(), default=0) + 100
        else:
            tempo_limite = self.config.tempo

        if self.config.verbose:
            print("[000] Simulação iniciada")

        for t in range(tempo_limite):
            novos = self.agenda.get(t, [])
            self.central.processar_tick(novos)

        metricas = self.central.calcular_metricas()
        Relatorio.exibir(metricas)