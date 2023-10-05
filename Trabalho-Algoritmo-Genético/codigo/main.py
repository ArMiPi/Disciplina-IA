from genetico import Genetico
import pandas as pd


if __name__ == "__main__":
    dataset = pd.read_csv('../disciplinas.csv', sep = ';')
    genetico = Genetico(dataset, verboso = False)