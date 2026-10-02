class FilaNo():


    #Cada nó recebe um dado e um marcador do próximio índice
    #O valor padrão None representa o fim da fila
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

class Fila():

    def __init__(self):    
            
            self._cabeca = None
            self._cauda = None
            self._tamanho = 0
                

    def enfileira(self, elemento):

        novo_no = FilaNo(elemento)

        #Se a fila estiver vazia, tanto cauda e cabeça apontam pro novo nó.
        #Como é o primeiro nó, o atr _próximo recebe -1
        if self.vazia():

            self._cabeca = novo_no
            self._cauda = novo_no

            self._tamanho += 1

        else:

            #Colocamos a informação de próximo dentro do novo nó
            
            self._cauda.set_prox(novo_no)

            #Coloca o novo nó no fim da fila
            self._cauda = novo_no

            #
            self._tamanho +=1

        


    def desinfileira(self):

        if self.vazia():

            return None

        #Pegamos o dado que está no nó da cabeça
        dado = self._cabeca.get_dado()

        #Definimos qual o próxino elemento:
        #É o nó que estava salvo como próximo dentro do nó atual.
        #Essa informação foi definida na hora de enfileirar.
        self._cabeca = self._cabeca.get_prox()

        self._tamanho -= 1

        # Se a fila ficou vazia após a remoção, limpamos a cauda também
        if self.vazia():

            self._cauda = None

        return dado


    def tamanho(self):

        return self._tamanho

    def cabeca(self):

        if self.vazia():

            return None

        return self._cabeca.get_dado()

 
    #Retorna falso se não existir nenhum elemento na fila
    def vazia(self):

        return self._tamanho == 0


    def imprime(self):

        if (self.vazia()):

            print()

        no_atual = self._cabeca

        while no_atual is not None:

            #Um check pra saber se ten próximo
            if no_atual.get_prox() == None:

                print(f'{no_atual.get_dado()} ', end='')
                
                #Pula para o próximo nó
                no_atual = no_atual.get_prox()
                        
            else:

                
                print(f'{no_atual.get_dado()} -> ', end='')

                #Pula para o próximo nó
                no_atual = no_atual.get_prox()
        
        # Quebra de linha no final da impressão
        print()