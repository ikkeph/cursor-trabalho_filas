'''
import unittest
from cliente import Cliente


class TestCliente(unittest.TestCase):

    def test_inicializacao_cliente(self):
        c = Cliente(id_cliente="C001", tipo="comum", tempo_chegada=5, tempo_duracao=3)
        self.assertEqual(c.id, "C001")
        self.assertEqual(c.tipo, "comum")
        self.assertEqual(c.tempo_chegada, 5)
        self.assertEqual(c.tempo_duracao, 3)

    def test_calculo_tempos_espera_e_sistema(self):
        # Cliente chega no tick 2 e precisa de 4 ticks de atendimento
        c = Cliente(id_cliente="C002", tipo="prioritario", tempo_chegada=2, tempo_duracao=4)
        
        # Inicia atendimento no tick 5 (esperou do tick 2 ao 5 = 3 ticks)
        c.registrar_inicio_atendimento(tempo_atual=5)
        self.assertEqual(c.get_tempo_espera(), 3)

        # Termina atendimento no tick 9 (durou do tick 5 ao 9 = 4 ticks, total no sistema = 7 ticks)
        c.registrar_fim_atendimento(tempo_atual=9)
        self.assertEqual(c.get_tempo_total_sistema(), 7)


if __name__ == "__main__":
    unittest.main()
'''

import unittest
from cliente import Cliente


class TestCliente(unittest.TestCase):

    def test_inicializacao_cliente(self):
        c = Cliente(id_cliente="C001", tipo="comum", tempo_chegada=5, tempo_duracao=3)
        self.assertEqual(c.id, "C001")
        self.assertEqual(c.tipo, "comum")
        self.assertEqual(c.tempo_chegada, 5)
        self.assertEqual(c.tempo_duracao, 3)
        self.assertIsNone(c.tempo_inicio_atendimento)
        self.assertIsNone(c.tempo_fim_atendimento)

    def test_tipo_e_normalizado(self):
        c = Cliente("C001", "  PrioriTARIO ", 0, 1)
        self.assertEqual(c.tipo, "prioritario")

    def test_atributos_sao_somente_leitura(self):
        c = Cliente("C001", "comum", 0, 2)
        with self.assertRaises(AttributeError):
            c.id = "outro"
        with self.assertRaises(AttributeError):
            c.tempo_duracao = 10
        with self.assertRaises(AttributeError):
            c.tempo_inicio_atendimento = 3

    def test_parametros_invalidos(self):
        with self.assertRaises(ValueError):
            Cliente("C001", "comum", -1, 2)   # chegada negativa
        with self.assertRaises(ValueError):
            Cliente("C001", "comum", 0, 0)    # duração zero
        with self.assertRaises(ValueError):
            Cliente("C001", "comum", 0, -3)   # duração negativa
        with self.assertRaises(ValueError):
            Cliente("C001", "   ", 0, 2)      # tipo vazio

    def test_eh_prioritario(self):
        self.assertTrue(Cliente("A", "prioritario", 0, 1).eh_prioritario)
        self.assertTrue(Cliente("B", "Prioritária", 0, 1).eh_prioritario)
        self.assertTrue(Cliente("C", "prioritaria", 0, 1).eh_prioritario)
        self.assertFalse(Cliente("D", "comum", 0, 1).eh_prioritario)
        self.assertFalse(Cliente("E", "tecnico", 0, 1).eh_prioritario)

    def test_calculo_tempos_espera_e_sistema(self):
        # Cliente chega no tick 2 e precisa de 4 ticks de atendimento
        c = Cliente(id_cliente="C002", tipo="prioritario", tempo_chegada=2, tempo_duracao=4)

        # Inicia atendimento no tick 5 (esperou do tick 2 ao 5 = 3 ticks)
        c.registrar_inicio_atendimento(tempo_atual=5)
        self.assertEqual(c.get_tempo_espera(), 3)

        # Termina atendimento no tick 9 (durou do tick 5 ao 9 = 4 ticks, total no sistema = 7 ticks)
        c.registrar_fim_atendimento(tempo_atual=9)
        self.assertEqual(c.get_tempo_total_sistema(), 7)

    def test_espera_zero_quando_atendido_no_tick_da_chegada(self):
        c = Cliente("C001", "comum", 4, 2)
        c.registrar_inicio_atendimento(4)
        self.assertEqual(c.get_tempo_espera(), 0)

    def test_tempos_antes_de_atendimento_levantam_erro(self):
        c = Cliente("C001", "comum", 0, 2)
        with self.assertRaises(RuntimeError):
            c.get_tempo_espera()
        with self.assertRaises(RuntimeError):
            c.get_tempo_total_sistema()

    def test_inicio_antes_da_chegada_levanta_erro(self):
        c = Cliente("C001", "comum", 5, 2)
        with self.assertRaises(ValueError):
            c.registrar_inicio_atendimento(4)

    def test_fim_sem_inicio_levanta_erro(self):
        c = Cliente("C001", "comum", 0, 2)
        with self.assertRaises(RuntimeError):
            c.registrar_fim_atendimento(3)

    def test_fim_antes_do_inicio_levanta_erro(self):
        c = Cliente("C001", "comum", 0, 2)
        c.registrar_inicio_atendimento(5)
        with self.assertRaises(ValueError):
            c.registrar_fim_atendimento(4)

    def test_str_e_repr(self):
        c = Cliente("C001", "comum", 2, 3)
        self.assertEqual(str(c), "Cliente C001 [comum]")
        self.assertIn("C001", repr(c))


if __name__ == "__main__":
    unittest.main()