from datetime import datetime as dt
import random as rd


class Uteis:
    def __init__(self, tam_populacao_inicial, geracoes, taxa_mutacao, verboso = False):
        self.verboso = verboso
        self.tam_populacao_inicial = tam_populacao_inicial
        self.geracoes = geracoes
        self.taxa_mutacao = taxa_mutacao


    def gerar_populacao_inicial(self):
        populacao = []

        for _ in range(self.tam_populacao_inicial):
            auxiliar = []

            for _ in range(4):
                auxiliar.append([rd.randint(0, 8) for _ in range(20)])

            populacao.append(auxiliar)

        return populacao


    def imprimir_resultado(self, hora_inicio, populacao, populacao_fitness):
        contador = 0
        hora_fim = dt.now()

        print("=" * 100)
        print(">>> Imprimindo resultados:\n\n" +
              f"Tempo decorrido: {hora_fim - hora_inicio}.\n")

        for elemento in populacao_fitness:
            if contador == 3:
                break

            print(f"Indivíduo {elemento[0]}:\n[")
            print(f"\t1° Ano   = {populacao[elemento[0]][0]}")
            print(f"\t2° Ano   = {populacao[elemento[0]][1]}")
            print(f"\t3° Ano   = {populacao[elemento[0]][2]}")
            print(f"\tCursinho = {populacao[elemento[0]][3]}\n")
            print(f"\tAptidão: {elemento[1]}")
            print("]\n")

            contador += 1


    def imprimir_populacao(self, populacao, populacao_fitness):
        print("=" * 100)
        print(">>> Imprimindo população inicial:\n")

        for i in range(len(populacao)):
            print(f"Indivíduo {i}:\n[")
            print(f"\t1° Ano   = {populacao[i][0]}")
            print(f"\t2° Ano   = {populacao[i][1]}")
            print(f"\t3° Ano   = {populacao[i][2]}")
            print(f"\tCursinho = {populacao[i][3]}\n")

            for individuo in populacao_fitness:
                if individuo[0] == i:
                    print(f"\tAptidão: {individuo[1]}")
                    break

            print("]\n")

        print("=" * 100)
        print(">>> Melhor indivíduo da geração inicial:\n")

        indice_melhor, aptidao = populacao_fitness[0][0], populacao_fitness[0][1]

        print(f"Indivíduo {indice_melhor}:\n[")
        print(f"\t1° Ano   = {populacao[indice_melhor][0]}")
        print(f"\t2° Ano   = {populacao[indice_melhor][1]}")
        print(f"\t3° Ano   = {populacao[indice_melhor][2]}")
        print(f"\tCursinho = {populacao[indice_melhor][3]}\n")
        print(f"\tAptidão: {aptidao}")
        print("]\n")

    
    def imprimir_inicio_algoritmo(self, hora_inicio):
        print("=" * 100)
        print(f">>> Iniciando algoritmo genético.\n\n" +
                f"Hora de início: {hora_inicio}.\n" +
                f"População inicial: {self.tam_populacao_inicial} indivíduos.\n" + 
                f"Gerações: {self.geracoes}.\n" +
                f"Taxa de mutação: {self.taxa_mutacao * 100}%.\n")
        

    def calculo_violacao(self, cromossomo, indice):
        aulas = []

        aulas.append(cromossomo[0][indice])
        aulas.append(cromossomo[1][indice])
        aulas.append(cromossomo[2][indice])
        aulas.append(cromossomo[3][indice])

        return 4 - len(set(aulas))