import random as rd

class Genetico:

    # Constantes
    PESO_HC1 = 0.8
    PESO_HC2 = 0.8
    PESO_SC1 = 0.3
    PESO_SC2 = 0.2
    TAM_POPULACAO_INICIAL = 1
    GERACOES = 500
    TAXA_MUTACAO = 0.1


    def __init__(self, dataset, imprimir_populacao = False) -> None:
        self.populacao = [
            [0, 1, 4, 5, 2, 3, 8, 6, 0, 1, 4, 5, 2, 7, 4, 6, 0, 5, 8, 3],
            [1, 0, 5, 4, 3, 2, 6, 8, 1, 0, 5, 4, 3, 2, 6, 4, 5, 0, 7, 8],
            [4, 5, 0, 1, 8, 6, 2, 3, 4, 5, 0, 1, 4, 6, 2, 3, 8, 7, 0, 5],
            [5, 4, 1, 0, 6, 8, 3, 2, 5, 4, 1, 0, 5, 4, 3, 2, 7, 8, 6, 0]  
        ], []
        self.dataset = dataset
        # self.gerar_populacao_inicial()

        if (imprimir_populacao):
            self.imprimir_populacao()

        self.fitness(self.populacao[0])

    
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
            print(f"\t1° Ano   = {individuo[0]}")
            print(f"\t2° Ano   = {individuo[1]}")
            print(f"\t3° Ano   = {individuo[2]}")
            print(f"\tCursinho = {individuo[3]}")
            print("]\n")

            indice += 1
            break


    def fitness(self, cromossomo: list[int]) -> float:
        # Contadores constraints.
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

        print(f"Violações de HC 1: {hc_1}")

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

        print(f"Violações de HC 2: {hc_2}")
        print(f"Violações de SC 1: {sc_1}")
        print(f"Violações de SC 2: {sc_2}")
        print(f"Fitness: {(sc_1 * self.PESO_SC1 + sc_2 * self.PESO_SC2) - ((hc_1 * self.PESO_HC1 + hc_2 * self.PESO_HC2) ** 2)}")

        return (sc_1 * self.PESO_SC1 + sc_2 * self.PESO_SC2) - ((hc_1 * self.PESO_HC1 + hc_2 * self.PESO_HC2) ** 2)