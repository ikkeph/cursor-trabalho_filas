import unittest
from central import CentralAtendimento
from atendente import Atendente
from cliente import Cliente


class TestCentralAtendimento(unittest.TestCase):

    def test_politica_fifo(self):
        atendentes = [Atendente(id_atendente=1)]
        central = CentralAtendimento(atendentes=atendentes, politica="fifo")

        c1 = Cliente("C001", "comum", 0, 2)
        c2 = Cliente("C002", "prioritario", 0, 2)

        central.receber_cliente(c1)
        central.receber_cliente(c2)

        # Na FIFO, C001 deve sair primeiro, mesmo C2 sendo prioritário
        self.assertEqual(central.obter_proximo_cliente().id, "C001")
        self.assertEqual(central.obter_proximo_cliente().id, "C002")

    def test_politica_prioridade_e_antistarvation(self):
        atendentes = [Atendente(id_atendente=1)]
        central = CentralAtendimento(atendentes=atendentes, politica="prioridade")

        p1 = Cliente("P001", "prioritario", 0, 2)
        p2 = Cliente("P002", "prioritario", 0, 2)
        p3 = Cliente("P003", "prioritario", 0, 2)
        p4 = Cliente("P004", "prioritario", 0, 2)
        c1 = Cliente("C001", "comum", 0, 2)

        # Insere 4 prioritários e 1 comum
        for p in [p1, p2, p3, p4]:
            central.receber_cliente(p)
        central.receber_cliente(c1)

        # Atende os 3 primeiros prioritários
        self.assertEqual(central.obter_proximo_cliente().id, "P001")
        self.assertEqual(central.obter_proximo_cliente().id, "P002")
        self.assertEqual(central.obter_proximo_cliente().id, "P003")

        # O 4º atendimento DEVE ser o cliente comum C001 (regra de Anti-Starvation)
        self.assertEqual(central.obter_proximo_cliente().id, "C001")

        # O próximo volta a ser o prioritário restante
        self.assertEqual(central.obter_proximo_cliente().id, "P004")


if __name__ == "__main__":
    unittest.main()