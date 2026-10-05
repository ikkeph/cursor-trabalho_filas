from typing import List, Optional
from cliente import Cliente


# Mesa da central: pega um cliente, conta os ticks e devolve quando termina.
class Atendente:

    def __init__(self, id_atendente, tipos_atendimento: Optional[List[str]] = None):
        self._id = id_atendente
        self._tipos_atendimento = [t.strip().lower() for t in tipos_atendimento] if tipos_atendimento else []
        self._cliente_atual: Optional[Cliente] = None
        self._tempo_restante: int = 0
        self._total_clientes_atendidos: int = 0
        self._tempo_total_ocupado: int = 0

    @property
    def id(self):
        return self._id

    @property
    def tipos_atendimento(self):
        return self._tipos_atendimento

    @property
    def cliente_atual(self):
        return self._cliente_atual

    @property
    def tempo_restante(self):
        return self._tempo_restante

    @property
    def total_clientes_atendidos(self):
        return self._total_clientes_atendidos

    @property
    def tempo_total_ocupado(self):
        return self._tempo_total_ocupado

    def esta_livre(self) -> bool:
        return self._cliente_atual is None

    # Lista vazia = generalista (é o caso deste trabalho).
    def pode_atender(self, tipo_cliente: str) -> bool:
        if not self._tipos_atendimento:
            return True
        return tipo_cliente.strip().lower() in self.tipos_atendimento

    def iniciar_atendimento(self, cliente: Cliente, tempo_atual: int) -> None:
        if not self.esta_livre():
            raise RuntimeError(f"Atendente {self._id} já está ocupado com o Cliente {self._cliente_atual.id}.")

        self._cliente_atual = cliente
        self._tempo_restante = cliente.tempo_duracao
        cliente.registrar_inicio_atendimento(tempo_atual)

    # Anda 1 tick. Se o tempo restante chegou a 0, devolve o cliente terminado.
    def processar_unidade_tempo(self) -> Optional[Cliente]:
        if self.esta_livre():
            return None

        self._tempo_total_ocupado += 1
        self._tempo_restante -= 1

        if self._tempo_restante == 0:
            return self.finalizar_atendimento()

        return None

    # Libera a mesa. O carimbo do fim fica a cargo da Central, no tick atual.
    def finalizar_atendimento(self) -> Cliente:
        if self._cliente_atual is None:
            raise RuntimeError(f"Atendente {self.id} tentou finalizar atendimento sem nenhum cliente ativo.")

        cliente_concluido = self._cliente_atual
        self._total_clientes_atendidos += 1
        self._cliente_atual = None
        self._tempo_restante = 0
        return cliente_concluido

    # Porcentagem do relógio em que a mesa esteve ocupada.
    def calcular_taxa_utilizacao(self, tempo_total_simulacao: int) -> float:
        if tempo_total_simulacao <= 0:
            return 0.0
        return (self._tempo_total_ocupado / tempo_total_simulacao) * 100.0
