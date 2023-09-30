import random as rd

class Genetico:

    # Constantes
    PESO_HC1 = 0.8
    PESO_HC2 = 0.8
    PESO_SC1 = 0.3
    PESO_SC2 = 0.2
    TAM_POPULACAO_INICIAL = 100
    GERACOES = 500
    TAXA_MUTACAO = 0.1


    def __init__(self, imprimir_populacao = False) -> None:
        self.populacao = []
        self.gerar_populacao_inicial()

        if (imprimir_populacao):
            self.imprimir_populacao()

    
    def resolver(self) -> None:
        pass


    def gerar_populacao_inicial(self) -> None:
        for _ in range(self.TAM_POPULACAO_INICIAL):
            temp = []

            for _ in range(4):
                temp.append([rd.randrange(0, 9) for _ in range(20)])

            self.populacao.append(temp)

    
    def imprimir_populacao(self) -> None:
        indice = 1

        for individuo in self.populacao:
            print(f"Indivíduo {indice}:\n[")

            for i in individuo:
                print(f"\t{i}")

            print("]\n")
            indice += 1