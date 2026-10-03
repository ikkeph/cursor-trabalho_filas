import unittest
from atendente import Atendente
from central import CentralAtendimento
from cliente import Cliente
from estatisticas import Estatisticas


class TestEstatisticas(unittest.TestCase):

    def test_sem_clientes(self):
        central = CentralAtendimento(atendentes=[Atendente(1)], politica="fifo")
        metricas = Estatisticas.calcular(central)
        self.assertEqual(metricas["total_chegaram"], 0)
        self.assertEqual(metricas["total_atendidos"], 0)
        self.assertEqual(metricas["tempo_medio_espera"], 0.0)
        self.assertEqual(metricas["utilizacao_media"], 0.0)
        self.assertEqual(metricas["vazao"], 0.0)

    def test_espera_conhecida_na_mao(self):
        # C1 chega em 0, começa em 2, termina em 5 → espera 2, sistema 5
        # C2 (prioritário) chega em 1, começa em 3, termina em 6 → espera 2, sistema 5
        c1 = Cliente("C1", "comum", 0, 3)
        c1.registrar_inicio_atendimento(2)
        c1.registrar_fim_atendimento(5)

        c2 = Cliente("C2", "prioritario", 1, 3)
        c2.registrar_inicio_atendimento(3)
        c2.registrar_fim_atendimento(6)

        atendente = Atendente(1)
        central = CentralAtendimento(atendentes=[atendente], politica="fifo")
        central.clientes_que_chegaram.extend([c1, c2])
        central.clientes_atendidos.extend([c1, c2])
        central.historico_tamanho_fila.extend([1, 1, 0, 0, 0])
        central._tempo_decorrido = 5
        atendente._tempo_total_ocupado = 4

        metricas = Estatisticas.calcular(central)
        self.assertEqual(metricas["total_chegaram"], 2)
        self.assertEqual(metricas["total_atendidos"], 2)
        self.assertEqual(metricas["tempo_medio_espera"], 2.0)
        self.assertEqual(metricas["tempo_medio_sistema"], 5.0)
        self.assertEqual(metricas["espera_media_comuns"], 2.0)
        self.assertEqual(metricas["espera_media_prioritarios"], 2.0)
        self.assertAlmostEqual(metricas["utilizacao_media"], 80.0)
        self.assertAlmostEqual(metricas["vazao"], 0.4)


if __name__ == "__main__":
    unittest.main()
