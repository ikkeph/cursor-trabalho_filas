import argparse
import sys
from dataclasses import dataclass
from typing import Optional


# Parâmetros da simulação, lidos da linha de comando.
@dataclass
class Configuracao:

    modo: str
    entrada: Optional[str] = None
    tempo: int = 1000
    atendentes: int = 3
    prob_chegada: float = 0.30
    tempo_min: int = 2
    tempo_max: int = 8
    prioritarios: float = 0.20
    politica: str = "fifo"
    seed: Optional[int] = None
    verbose: bool = False

    # Monta o argparse e devolve uma Configuracao já validada.
    @classmethod
    def parse_args(cls) -> "Configuracao":
        parser = argparse.ArgumentParser(
            description="Simulador de Central de Atendimento com Filas (Programação II - UFSC)"
        )
        parser.add_argument("--modo", choices=["arquivo", "aleatorio"], required=True)
        parser.add_argument("--entrada", type=str)
        parser.add_argument("--tempo", type=int, default=1000)
        parser.add_argument("--atendentes", type=int, default=3)
        parser.add_argument("--prob-chegada", type=float, default=0.30)
        parser.add_argument("--tempo-min", type=int, default=2)
        parser.add_argument("--tempo-max", type=int, default=8)
        parser.add_argument("--prioritarios", type=float, default=0.20)
        parser.add_argument("--politica", choices=["fifo", "prioridade"], default="fifo")
        parser.add_argument("--seed", type=int)
        parser.add_argument("--verbose", action="store_true")

        args = parser.parse_args()
        config = cls(**vars(args))  # preenche os campos com os mesmos nomes dos argumentos
        config.validar()
        return config

    # Encerra o programa se algum valor da linha de comando não fizer sentido.
    def validar(self) -> None:
        if self.atendentes <= 0:
            sys.exit("Erro: O número de atendentes deve ser maior que 0.")
        if self.modo == "arquivo" and not self.entrada:
            sys.exit("Erro: O argumento '--entrada' é obrigatório no modo 'arquivo'.")
        if self.modo == "aleatorio":
            if self.tempo <= 0:
                sys.exit("Erro: '--tempo' deve ser maior que 0.")
            if not (0.0 <= self.prob_chegada <= 1.0):
                sys.exit("Erro: '--prob-chegada' deve estar entre 0 e 1.")
            if not (0.0 <= self.prioritarios <= 1.0):
                sys.exit("Erro: '--prioritarios' deve estar entre 0 e 1.")
            if self.tempo_min <= 0 or self.tempo_max < self.tempo_min:
                sys.exit("Erro: Garanta que 0 < '--tempo-min' <= '--tempo-max'.")
