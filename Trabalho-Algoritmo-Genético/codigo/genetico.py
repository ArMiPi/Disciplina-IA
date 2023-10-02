import random as rd
from datetime import datetime as dt
from uteis import Uteis


class Genetico:
    # Constantes
    PESO_HC1 = 0.8
    PESO_HC2 = 0.8
    PESO_SC1 = 0.3
    PESO_SC2 = 0.2
    TAM_POPULACAO_INICIAL = 2100
    GERACOES = TAM_POPULACAO_INICIAL * 9
    TAXA_MUTACAO = 0.35


    def __init__(self, dataset, verboso = False):
        rd.seed()

        self.utils = Uteis(self.TAM_POPULACAO_INICIAL, self.GERACOES, self.TAXA_MUTACAO, verboso)
        self.populacao = self.utils.gerar_populacao_inicial()
        self.populacao_fitness = []
        self.dataset = dataset
        self.verboso = verboso
        self.hora_inicio = dt.now()

        self.ordenar_populacao()

        if self.verboso:
            self.utils.imprimir_populacao(self.populacao, self.populacao_fitness)

        self.resolver()

    
    def resolver(self):
        if self.verboso:
            self.utils.imprimir_inicio_algoritmo(self.hora_inicio)

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

        self.ordenar_populacao()
        self.utils.imprimir_resultado(self.hora_inicio, self.populacao, self.populacao_fitness)


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