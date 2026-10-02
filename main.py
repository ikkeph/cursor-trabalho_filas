from configuracao import Configuracao
from simulacao import Simulacao

def main():
    config = Configuracao.parse_args()
    simulador = Simulacao(config)
    simulador.executar()
    
    input("[Pressione ENTER para encerrar o programa...]")

if __name__ == "__main__":
    main()