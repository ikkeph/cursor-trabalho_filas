import unittest
from atendente import Atendente
from cliente import Cliente


class TestAtendente(unittest.TestCase):

    def test_estado_inicial_livre(self):
        a = Atendente(id_atendente=1)
        self.assertTrue(a.esta_livre())
        self.assertIsNone(a.cliente_atual)

    def test_fluxo_atendimento(self):
        a = Atendente(id_atendente=1)
        c = Cliente(id_cliente="C001", tipo="comum", tempo_chegada=0, tempo_duracao=2)

        a.iniciar_atendimento(c, tempo_atual=0)
        self.assertFalse(a.esta_livre())
        self.assertEqual(a.cliente_atual.id, "C001")

        # duração 2: o primeiro tick ainda não termina
        concluido = a.processar_unidade_tempo()
        self.assertIsNone(concluido)
        self.assertFalse(a.esta_livre())

        concluido = a.processar_unidade_tempo()
        self.assertIsNotNone(concluido)
        self.assertEqual(concluido.id, "C001")
        self.assertTrue(a.esta_livre())
        self.assertEqual(a.total_clientes_atendidos, 1)
        self.assertEqual(a.tempo_total_ocupado, 2)


if __name__ == "__main__":
    unittest.main()