import unittest
from configuracao import Configuracao
from simulacao import Simulacao


class TestSimulacaoCenarioDeterministico(unittest.TestCase):

    def test_execucao_cenario_conhecido(self):
        config = Configuracao(
            modo="aleatorio",
            tempo=100,
            atendentes=2,
            prob_chegada=0.30,
            tempo_min=2,
            tempo_max=5,
            prioritarios=0.20,
            politica="fifo",
            seed=42,
            verbose=False
        )

        simulacao = Simulacao(config)
        simulacao.executar()

        metricas = simulacao.central.calcular_metricas()

        # Contabiliza os clientes que estão sendo atendidos nos guichês no fim do tempo
        em_atendimento = sum(1 for a in simulacao.central.atendentes if not a.esta_livre())

        self.assertGreater(metricas["total_chegaram"], 0)
        
        # Conservação de clientes: Chegaram = Atendidos + Na Fila + Em Atendimento
        self.assertEqual(
            metricas["total_chegaram"],
            metricas["total_atendidos"] + metricas["total_aguardando"] + em_atendimento
        )
        self.assertGreaterEqual(metricas["tempo_medio_espera"], 0.0)


if __name__ == "__main__":
    unittest.main()