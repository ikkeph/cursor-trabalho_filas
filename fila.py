# Nó da lista encadeada da Fila.
class FilaNo():

    # dado + ponteiro para o próximo; None = fim da fila
    def __init__(self, dado, indice_proximo = None):

        self._dado = dado
        self._proximo = indice_proximo

    def set_prox(self, prox):
        self._proximo = prox

    def get_dado(self):

        return self._dado

    def get_prox(self):

        return self._proximo

    def set_dado(self, dado):

        self._dado = dado

# Fila da disciplina. A Central só usa enfileira, desinfileira, vazia, cabeca e tamanho.
class Fila():

    def __init__(self):    
            
            self._cabeca = None
            self._cauda = None
            self._tamanho = 0
                

    def enfileira(self, elemento):

        novo_no = FilaNo(elemento)

        # fila vazia: cabeça e cauda são o mesmo nó
        if self.vazia():

            self._cabeca = novo_no
            self._cauda = novo_no

            self._tamanho += 1

        else:

            self._cauda.set_prox(novo_no)
            self._cauda = novo_no
            self._tamanho +=1

        


    def desinfileira(self):

        if self.vazia():

            return None

        dado = self._cabeca.get_dado()
        self._cabeca = self._cabeca.get_prox()
        self._tamanho -= 1

        # último elemento saiu: a cauda também aponta para ninguém
        if self.vazia():

            self._cauda = None

        return dado


    def tamanho(self):

        return self._tamanho

    def cabeca(self):

        if self.vazia():

            return None

        return self._cabeca.get_dado()

 
    def vazia(self):

        return self._tamanho == 0


    def imprime(self):

        if (self.vazia()):

            print()

        no_atual = self._cabeca

        while no_atual is not None:

            if no_atual.get_prox() == None:
                print(f'{no_atual.get_dado()} ', end='')
            else:
                print(f'{no_atual.get_dado()} -> ', end='')
            no_atual = no_atual.get_prox()

        print()