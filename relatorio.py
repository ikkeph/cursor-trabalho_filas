class Relatorio:
    @staticmethod
    def exibir(metricas: dict) -> None:
        print("\n" + "=" * 50)
        print("      RESULTADOS DA SIMULAÇÃO DE ATENDIMENTO      ")
        print("=" * 50)
        print(f"Total de clientes que chegaram : {metricas['total_chegaram']}")
        print(f"Total de clientes atendidos   : {metricas['total_atendidos']}")
        print(f"Clientes ainda na fila         : {metricas['total_aguardando']}")
        print("-" * 50)
        print(f"Tempo médio de espera          : {metricas['tempo_medio_espera']:.2f} ticks")
        print(f"Menor tempo de espera          : {metricas['menor_tempo_espera']} ticks")
        print(f"Maior tempo de espera          : {metricas['maior_tempo_espera']} ticks")
        print(f"Tempo médio no sistema         : {metricas['tempo_medio_sistema']:.2f} ticks")
        print("-" * 50)
        print("Espera por tipo (clientes atendidos):")
        print(f"  Prioritários ({metricas['atendidos_prioritarios']}): "
              f"média {metricas['espera_media_prioritarios']:.2f} / "
              f"máx {metricas['espera_max_prioritarios']} ticks")
        print(f"  Comuns ({metricas['atendidos_comuns']}): "
              f"média {metricas['espera_media_comuns']:.2f} / "
              f"máx {metricas['espera_max_comuns']} ticks")
        print("-" * 50)
        print(f"Tamanho médio da fila          : {metricas['tamanho_medio_fila']:.2f}")
        print(f"Tamanho máximo da fila         : {metricas['tamanho_maximo_fila']}")
        print(f"Vazão do sistema               : {metricas['vazao']:.2f} clientes/tick")
        print(f"Utilização média dos atendentes: {metricas['utilizacao_media']:.1f}%")
        print("-" * 50)
        print("Taxa de Utilização dos Atendentes:")
        for nome, util in metricas["utilizacao_atendentes"].items():
            print(f"  - {nome}: {util:.1f}%")
        print("=" * 50 + "\n")