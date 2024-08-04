from macrophage import Macrophage
from candida import Candida
import numpy as np
import pandas as pd
import matplotlib

# release = 0
# attack = 1

def initialise_m(rng):
    """
    Create a population of Cells - all less aggressive to begin
    """

    cells = []

    for _ in range(100):
        cells.append(Macrophage(1, rng))

    return (cells)

def initialise_c(rng):
    """
    Create a population of Cells - all less aggressive to begin
    """

    cells = []

    for _ in range(100):
        cells.append(Candida(1, rng))

    return (cells)


def timestep(macrophages, candidas, params, rng):
    """
    Pair up the macrophages with candida, make them compete
    Then produce next generation, weighted by fitness
    """

    next_m_generation = []
    next_c_generation = []

    rng.shuffle(macrophages)
    rng.shuffle(candidas)

    for _ in range(1000):

        # pair up random birds to contest
        a, b = rng.choice(macrophages, 1)[0], rng.choice(candidas, 1)[0]
        a.contest(b, params)

    # generate next generation
    sorted_macrophages = sorted(macrophages, key=lambda macrophage: macrophage.fitness)[20:]
    sorted_candidas = sorted(candidas, key=lambda candida: candida.fitness)[20:]
    draw_m = [*sorted_macrophages, *rng.choice(sorted_macrophages[-50:], size=20)]
    draw_c = [*sorted_candidas, *rng.choice(sorted_candidas[-50:], size=20)]
    next_m_generation = [macrophage.spawn() for macrophage in draw_m]
    next_c_generation = [candida.spawn() for candida in draw_c]

    return (next_m_generation, next_c_generation)


def main():
    rng = np.random.default_rng(1234)

    macrophages = initialise_m(rng)
    candida = initialise_c(rng)

    rows = []

    params = (5, 8, 2, 3, 1, 4, 1, 5, 2, 1, 0.54)

    for _ in range(500):
        if (_ % 50) == 0:
            print(_)
        # add the counts to a new row
        strategy_m = [macrophage.strategy for macrophage in macrophages]
        n_attack = sum(strategy_m)
        n_releases =  len(strategy_m) - n_attack
        strategy_c = [conidia.strategy for conidia in candida]
        n_aggressive = sum(strategy_c)
        n_less_aggressive =  len(strategy_c) - n_aggressive
        row = {'n_attack': n_attack, 'n_releases': n_releases, 'n_aggressive': n_aggressive, 'n_less_aggressive': n_less_aggressive}
        rows.append(row)

        # run the timestep function
        macrophages, candida = timestep(macrophages, candida, params, rng)


    # create dataframe and save output

    df = pd.DataFrame(rows)
    df.to_csv('simulation.csv')
    fig = df.plot(y=["n_attack", "n_releases", "n_aggressive", "n_less_aggressive"]).get_figure()
    fig.savefig('simulation.pdf')

if __name__ == "__main__":
    main()