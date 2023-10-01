import random as rd

class Genetico:

    # Constantes
    PESO_HC1 = 0.8
    PESO_HC2 = 0.8
    PESO_SC1 = 0.3
    PESO_SC2 = 0.2
    TAM_POPULACAO_INICIAL = 500
    GERACOES = 1000
    TAXA_MUTACAO = 0.02


    def __init__(self, dataset, verboso = False):
        rd.seed()

        self.populacao = []
        self.populacao_fitness = []
        self.dataset = dataset
        self.verboso = verboso

        self.gerar_populacao_inicial()
        self.ordenar_populacao()

        if self.verboso:
            self.imprimir_populacao()

        self.resolver()

    
    def resolver(self):
        for _ in range(self.GERACOES):
            cromossomos = []
            cromossomos.append(self.populacao[self.populacao_fitness[0][0]])
            cromossomos.append(self.populacao[self.populacao_fitness[1][0]])
            novo_cromossomo = self.crossover(cromossomos)

            self.populacao.pop(self.populacao_fitness[-1][0])
            self.populacao.append(novo_cromossomo)
            self.inserir_novo_fitness()

            if rd.random() <= self.TAXA_MUTACAO:
                self.mutacao()

        self.imprimir_melhores()


    def gerar_populacao_inicial(self):
        for _ in range(self.TAM_POPULACAO_INICIAL):
            auxiliar = []

            for _ in range(4):
                auxiliar.append([rd.randint(0, 8) for _ in range(20)])

            self.populacao.append(auxiliar)

    
    def imprimir_populacao(self):
        for i in range(len(self.populacao)):
            print(f"Indivíduo {i}:\n[")
            print(f"\t1° Ano   = {self.populacao[i][0]}")
            print(f"\t2° Ano   = {self.populacao[i][1]}")
            print(f"\t3° Ano   = {self.populacao[i][2]}")
            print(f"\tCursinho = {self.populacao[i][3]}\n")

            for individuo in self.populacao_fitness:
                if individuo[0] == i:
                    print(f"\tAptidão: {individuo[1]}")
                    break

            print("]\n")

        print("=" * 100)
        print("Melhor indivíduo da geração inicial:\n")

        indice_melhor, aptidao = self.populacao_fitness[0][0], self.populacao_fitness[0][1]

        print(f"Indivíduo {indice_melhor}:\n[")
        print(f"\t1° Ano   = {self.populacao[indice_melhor][0]}")
        print(f"\t2° Ano   = {self.populacao[indice_melhor][1]}")
        print(f"\t3° Ano   = {self.populacao[indice_melhor][2]}")
        print(f"\tCursinho = {self.populacao[indice_melhor][3]}\n")
        print(f"\tAptidão: {aptidao}")
        print("]\n")


    def imprimir_melhores(self):
        contador = 0

        print("=" * 100)
        print("Imprimindo resultados:\n")

        for elemento in self.populacao_fitness:
            if contador == 3:
                break

            print(f"Indivíduo {elemento[0]}:\n[")
            print(f"\t1° Ano   = {self.populacao[elemento[0]][0]}")
            print(f"\t2° Ano   = {self.populacao[elemento[0]][1]}")
            print(f"\t3° Ano   = {self.populacao[elemento[0]][2]}")
            print(f"\tCursinho = {self.populacao[elemento[0]][3]}\n")
            print(f"\tAptidão: {elemento[1]}")
            print("]\n")

            contador += 1
            
            
    def ordenar_populacao(self):
        auxiliar = []

        for i, cromossomo in enumerate(self.populacao):
            auxiliar.append((i, self.fitness(cromossomo)))

        self.populacao_fitness = sorted(auxiliar, key = lambda x: x[1], reverse = True)


    def inserir_novo_fitness(self):
        indice = len(self.populacao) - 1
        cromossomo = self.populacao[indice]

        self.populacao_fitness.append((indice, self.fitness(cromossomo)))
        self.populacao_fitness = sorted(self.populacao_fitness, key = lambda x: x[1], reverse = True)


    def fitness(self, cromossomo: list[int]) -> float:
        # Contadores de constraints.
        hc_1 = 0    # Um professor não pode estar em aula em duas turmas no mesmo horário.
        hc_2 = 0    # Todas as turmas devem cumprir as cargas horárias das disciplinas.
        sc_1 = 0    # Uma turma não deve ter duas aulas seguidas da mesma matéria.
        sc_2 = 0    # Deve-se evitar ao máximo que uma turma tenha aulas seguidas com o mesmo professor.

        p_ano, s_ano, t_ano, cursinho = cromossomo

        # hc1 -> Identificar se um mesmo professor está em aula em duas turmas no mesmo horário.
        for aula_p_ano, aula_s_ano, aula_t_ano, aula_cursinho in zip(p_ano, s_ano, t_ano, cursinho):
            professores = [
                self.dataset.loc[aula_p_ano]['Professor'],
                self.dataset.loc[aula_s_ano]['Professor'],
                self.dataset.loc[aula_t_ano]['Professor'],
                self.dataset.loc[aula_cursinho]['Professor']
            ]

            professores_unicos = set(professores)
            hc_1 += len(professores) - len(professores_unicos)

        # hc2 -> Todas as turmas devem cumprir as cargas horárias das disciplinas
        # sc1 -> Uma turma não deve ter duas aulas seguidas da mesma matéria
        for turma in cromossomo:
            # hc2
            aps = [turma.count(i) for i in range(len(self.dataset))]
            aps = [self.dataset.loc[i]['Aulas por Semana'] == aps[i] for i, _ in enumerate(aps)]

            # sc1
            aulas_seguidas = [turma[i] == turma[i+1] for i in range(len(turma) - 1)]

            # sc2
            professores = [self.dataset.loc[i]['Professor'] for i in turma]
            professores_seguidos = []
            for i in range(len(professores) - 1):
                # Índices correspondentes aos últimos horários dos dias (3, 7, 11...)
                if i % 4 == 3: continue

                professores_seguidos.append(professores[i] == professores[i+1])

            hc_2 += aps.count(False)
            sc_1 += aulas_seguidas.count(True)
            sc_2 += professores_seguidos.count(True)

        return (sc_1 * self.PESO_SC1 + sc_2 * self.PESO_SC2) - ((hc_1 * self.PESO_HC1 + hc_2 * self.PESO_HC2) ** 2)
    

    def crossover(self, individuos):
        cromossomo_a = individuos[0]
        cromossomo_b = individuos[1]
        novo_cromossomo = []

        for i in range(4):
            gene = []

            for j in range(20):
                if (cromossomo_a[i][j] != cromossomo_b[i][j]):
                    gene.append(rd.randint(0, 8))
                
                else:
                    gene.append(individuos[0][i][j])

            novo_cromossomo.append(gene)

        return novo_cromossomo


    def mutacao(self):
        cromossomo = self.populacao.pop(rd.randint(0, len(self.populacao) - 1))
        turma = rd.randint(0, 3)
        aula = rd.randint(0, 19)
        nova_aula = rd.randint(0, 8)

        while cromossomo[turma][aula] == nova_aula:
            nova_aula = rd.randint(0, 8)

        cromossomo[turma][aula] = nova_aula

        self.populacao.append(cromossomo)
        self.inserir_novo_fitness()
        
        