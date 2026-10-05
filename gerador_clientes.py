import random
import sys
from typing import Dict, List, Optional
from cliente import Cliente
from configuracao import Configuracao


# Monta a agenda {tick: [clientes]}. Só métodos estáticos, não guarda estado.
class GeradorClientes:

    # Lê o CSV ou sorteia e agrupa pelo horário de chegada.
    @staticmethod
    def criar_agenda(config: Configuracao) -> Dict[int, List[Cliente]]:
        if config.modo == "arquivo":
            clientes = GeradorClientes._carregar_arquivo(config.entrada)
        else:
            clientes = GeradorClientes._gerar_aleatorio(config)

        # o CSV pode ter vários no mesmo tick; o aleatório no máximo um
        chegadas_por_tick: Dict[int, List[Cliente]] = {}
        for cliente in clientes:
            chegadas_por_tick.setdefault(cliente.tempo_chegada, []).append(cliente)
        return chegadas_por_tick

    # Lê CSV id,tipo,chegada,duracao.
    @staticmethod
    def _carregar_arquivo(caminho: Optional[str]) -> List[Cliente]:
        if not caminho:
            sys.exit("Erro: Caminho do arquivo inválido.")
        clientes = []
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha or linha.startswith("#") or linha.lower().startswith("id"):
                        continue
                    partes = [p.strip() for p in linha.split(",")]
                    if len(partes) >= 4:
                        clientes.append(Cliente(partes[0], partes[1], int(partes[2]), int(partes[3])))
        except FileNotFoundError:
            sys.exit(f"Erro: Arquivo '{caminho}' não encontrado.")
        return clientes

    # No máximo um cliente por tick. Usa a seed que a Simulacao já plantou.
    @staticmethod
    def _gerar_aleatorio(config: Configuracao) -> List[Cliente]:
        clientes = []
        contador_id = 1
        for t in range(config.tempo):
            if random.random() < config.prob_chegada:
                tipo = "prioritario" if random.random() < config.prioritarios else "comum"
                duracao = random.randint(config.tempo_min, config.tempo_max)
                clientes.append(Cliente(f"C{contador_id:03d}", tipo, t, duracao))
                contador_id += 1
        return clientes
