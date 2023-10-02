import random as rd
from datetime import datetime as dt
from uteis import Uteis


class Genetico:
    # Constantes
    PESO_HC1 = 0.8
    PESO_HC2 = 0.8
    PESO_SC1 = 0.3
    PESO_SC2 = 0.2
    TAM_POPULACAO_INICIAL = 2500
    GERACOES = TAM_POPULACAO_INICIAL * 8
    TAXA_MUTACAO = 0.3
    NUM_COMPARACOES = 1


    def __init__(self, dataset, verboso = False, modo_comparacao = False):
        rd.seed()

        self.utils = Uteis(self.TAM_POPULACAO_INICIAL, self.GERACOES, self.TAXA_MUTACAO, verboso)
        self.populacao = self.utils.gerar_populacao_inicial()
        self.populacao_fitness = []
        self.dataset = dataset
        self.verboso = verboso
        self.modo_comparacao = modo_comparacao
        self.hora_inicio = dt.now()

        self.ordenar_populacao()

        if self.verboso:
            self.utils.imprimir_populacao(self.populacao, self.populacao_fitness)

        self.resolver()

    
    def resolver(self):
        fitness_acumulado = 0

        if self.verboso:
            self.utils.imprimir_inicio_algoritmo(self.hora_inicio)

        for i in range(self.NUM_COMPARACOES):
            if self.modo_comparacao:
                print(f">>> Iniciando iteração {i + 1}.")

            for _ in range(self.GERACOES):
                cromossomos = []
                cromossomos.append(self.populacao[self.populacao_fitness[0][0]])
                cromossomos.append(self.populacao[self.populacao_fitness[1][0]])
                novo_cromossomo = self.crossover(cromossomos)
                remover_indice = self.populacao_fitness[-1][0]

                self.populacao.pop(remover_indice)
                self.populacao.append(novo_cromossomo)
                self.remover_fitness(remover_indice)
                self.inserir_novo_fitness()

                if rd.random() <= self.TAXA_MUTACAO:
                    self.mutacao()

            if self.modo_comparacao:
                fitness_iteracao = self.populacao_fitness[0][1]
                fitness_acumulado += fitness_iteracao
                print(f">>> Fitness da iteração {i + 1}: {fitness_iteracao}.\n")

        self.ordenar_populacao()
        
        if not self.modo_comparacao:
            self.utils.imprimir_resultado(self.hora_inicio, self.populacao, self.populacao_fitness)

        if self.modo_comparacao:
            print("=" * 100)
            print(f">>> Fitness médio da comparação: {fitness_acumulado / self.NUM_COMPARACOES}.")


    def fitness(self, cromossomo: list[int]):
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
        novo_cromossomo = [[], [], [], []]

        for i in range(20):
            violacoes_a = self.utils.calculo_violacao(cromossomo_a, i)
            violacoes_b = self.utils.calculo_violacao(cromossomo_b, i)

            if violacoes_a <= violacoes_b:
                novo_cromossomo[0].append(cromossomo_a[0][i])
                novo_cromossomo[1].append(cromossomo_a[1][i])
                novo_cromossomo[2].append(cromossomo_a[2][i])
                novo_cromossomo[3].append(cromossomo_a[3][i])

            else:
                novo_cromossomo[0].append(cromossomo_b[0][i])
                novo_cromossomo[1].append(cromossomo_b[1][i])
                novo_cromossomo[2].append(cromossomo_b[2][i])
                novo_cromossomo[3].append(cromossomo_b[3][i])

        return novo_cromossomo


    def mutacao(self):
        indice = rd.randint(0, len(self.populacao) - 1)
        turma = rd.randint(0, 3)
        ponto_corte = rd.randint(4, 15)

        cromossomo = self.populacao.pop(indice)
        embaralhado = cromossomo[turma][ponto_corte:]

        rd.shuffle(embaralhado)

        cromossomo[turma] = cromossomo[turma][:ponto_corte] + embaralhado

        self.populacao.append(cromossomo)
        self.remover_fitness(indice)
        self.inserir_novo_fitness()

    
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


    def remover_fitness(self, indice):
        i = 0

        for fitness in self.populacao_fitness:
            if fitness[0] == indice:
                self.populacao_fitness.pop(i)

            i += 1