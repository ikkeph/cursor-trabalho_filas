from configuracao import Configuracao
from simulacao import Simulacao

def main():
    config = Configuracao.parse_args()
    simulador = Simulacao(config)
    simulador.executar()
    


if __name__ == "__main__":
    main()