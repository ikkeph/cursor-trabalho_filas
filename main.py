from configuracao import Configuracao
from simulacao import Simulacao


def main():
    # argparse e validação ficam na Configuracao; a lógica fica na Simulacao
    config = Configuracao.parse_args()
    simulador = Simulacao(config)
    simulador.executar()


if __name__ == "__main__":
    main()
