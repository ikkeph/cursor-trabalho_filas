from typing import Any, Dict, List, Tuple
from cliente import Cliente


class Estatisticas:
    """
    Fecha as contas do enunciado a partir do estado final da Central.
    A Central só coleta o histórico; o Relatorio só imprime.
    """

    @staticmethod
    def _resumo_espera(clientes: List[Cliente]) -> Tuple[float, int]:
        """Média e máximo do tempo de espera; (0.0, 0) se a lista estiver vazia."""
        if not clientes:
            return 0.0, 0
        esperas = [c.get_tempo_espera() for c in clientes]
        return sum(esperas) / len(esperas), max(esperas)

    @staticmethod
    def calcular(central) -> Dict[str, Any]:
        """Monta o dicionário de métricas obrigatórias (+ espera por tipo)."""
        total_chegaram = len(central.clientes_que_chegaram)
        total_atendidos = len(central.clientes_atendidos)
        total_aguardando = central.tamanho_total_filas()
        tempo = central.tempo_decorrido

        if total_atendidos > 0:
            tempos_espera = [c.get_tempo_espera() for c in central.clientes_atendidos]
            tempos_sistema = [c.get_tempo_total_sistema() for c in central.clientes_atendidos]
            tempo_medio_espera = sum(tempos_espera) / total_atendidos
            menor_tempo_espera = min(tempos_espera)
            maior_tempo_espera = max(tempos_espera)
            tempo_medio_sistema = sum(tempos_sistema) / total_atendidos
        else:
            tempo_medio_espera = 0.0
            menor_tempo_espera = 0
            maior_tempo_espera = 0
            tempo_medio_sistema = 0.0

        prioritarios = [c for c in central.clientes_atendidos if c.eh_prioritario]
        comuns = [c for c in central.clientes_atendidos if not c.eh_prioritario]
        espera_media_prioritarios, espera_max_prioritarios = Estatisticas._resumo_espera(prioritarios)
        espera_media_comuns, espera_max_comuns = Estatisticas._resumo_espera(comuns)

        if central.historico_tamanho_fila:
            tamanho_medio_fila = sum(central.historico_tamanho_fila) / len(central.historico_tamanho_fila)
            tamanho_maximo_fila = max(central.historico_tamanho_fila)
        else:
            tamanho_medio_fila = 0.0
            tamanho_maximo_fila = 0

        vazao = total_atendidos / tempo if tempo > 0 else 0.0

        utilizacao_atendentes = {}
        for atendente in central.atendentes:
            utilizacao_atendentes[f"Atendente {atendente.id}"] = atendente.calcular_taxa_utilizacao(tempo)

        if utilizacao_atendentes:
            utilizacao_media = sum(utilizacao_atendentes.values()) / len(utilizacao_atendentes)
        else:
            utilizacao_media = 0.0

        return {
            "total_chegaram": total_chegaram,
            "total_atendidos": total_atendidos,
            "total_aguardando": total_aguardando,
            "tempo_medio_espera": tempo_medio_espera,
            "menor_tempo_espera": menor_tempo_espera,
            "maior_tempo_espera": maior_tempo_espera,
            "tempo_medio_sistema": tempo_medio_sistema,
            "tamanho_medio_fila": tamanho_medio_fila,
            "tamanho_maximo_fila": tamanho_maximo_fila,
            "vazao": vazao,
            "utilizacao_atendentes": utilizacao_atendentes,
            "utilizacao_media": utilizacao_media,
            "atendidos_prioritarios": len(prioritarios),
            "atendidos_comuns": len(comuns),
            "espera_media_prioritarios": espera_media_prioritarios,
            "espera_max_prioritarios": espera_max_prioritarios,
            "espera_media_comuns": espera_media_comuns,
            "espera_max_comuns": espera_max_comuns,
        }
