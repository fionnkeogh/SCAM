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
        cells.append(Macrophage('0000', rng))

    return (cells)

def initialise_c(rng):
    """
    Create a population of Cells - all less aggressive to begin
    """

    cells = []

    for _ in range(100):
        cells.append(Candida('0000', rng))

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

    rows_m = []
    rows_c = []

    params = (5, 8, 2, 3, 1, 4, 1, 1, 4, 2, 0.54)

    for _ in range(10000):
        if (_ % 50) == 0:
            print(_)
        # add the counts to a new row
        strategy_m = [macrophage.strategy for macrophage in macrophages]
        n_m_0000 = strategy_m.count('0000')
        n_m_0001 = strategy_m.count('0001')
        n_m_0010 = strategy_m.count('0010')
        n_m_0011 = strategy_m.count('0011')
        n_m_0100 = strategy_m.count('0100')
        n_m_0101 = strategy_m.count('0101')
        n_m_0110 = strategy_m.count('0110')
        n_m_0111 = strategy_m.count('0111')
        n_m_1000 = strategy_m.count('1000')
        n_m_1001 = strategy_m.count('1001')
        n_m_1010 = strategy_m.count('1010')
        n_m_1011 = strategy_m.count('1011')
        n_m_1100 = strategy_m.count('1100')
        n_m_1101 = strategy_m.count('1101')
        n_m_1110 = strategy_m.count('1110')
        n_m_1111 = strategy_m.count('1111')
        strategy_c = [conidia.strategy for conidia in candida]
        n_c_0000 = strategy_c.count('0000')
        n_c_0001 = strategy_c.count('0001')
        n_c_0010 = strategy_c.count('0010')
        n_c_0011 = strategy_c.count('0011')
        n_c_0100 = strategy_c.count('0100')
        n_c_0101 = strategy_c.count('0101')
        n_c_0110 = strategy_c.count('0110')
        n_c_0111 = strategy_c.count('0111')
        n_c_1000 = strategy_c.count('1000')
        n_c_1001 = strategy_c.count('1001')
        n_c_1010 = strategy_c.count('1010')
        n_c_1011 = strategy_c.count('1011')
        n_c_1100 = strategy_c.count('1100')
        n_c_1101 = strategy_c.count('1101')
        n_c_1110 = strategy_c.count('1110')
        n_c_1111 = strategy_c.count('1111')
        row_m = {
            "n_m_0000": n_m_0000,
            "n_m_0001": n_m_0001,
            "n_m_0010": n_m_0010,
            "n_m_0011": n_m_0011,
            "n_m_0100": n_m_0100,
            "n_m_0101": n_m_0101,
            "n_m_0110": n_m_0110,
            "n_m_0111": n_m_0111,
            "n_m_1000": n_m_1000,
            "n_m_1001": n_m_1001,
            "n_m_1010": n_m_1010,
            "n_m_1011": n_m_1011,
            "n_m_1100": n_m_1100,
            "n_m_1101": n_m_1101,
            "n_m_1110": n_m_1110,
            "n_m_1111": n_m_1111}
        rows_m.append(row_m)
        row_c = {
            "n_c_0000": n_c_0000,
            "n_c_0001": n_c_0001,
            "n_c_0010": n_c_0010,
            "n_c_0011": n_c_0011,
            "n_c_0100": n_c_0100,
            "n_c_0101": n_c_0101,
            "n_c_0110": n_c_0110,
            "n_c_0111": n_c_0111,
            "n_c_1000": n_c_1000,
            "n_c_1001": n_c_1001,
            "n_c_1010": n_c_1010,
            "n_c_1011": n_c_1011,
            "n_c_1100": n_c_1100,
            "n_c_1101": n_c_1101,
            "n_c_1110": n_c_1110,
            "n_c_1111": n_c_1111}
        rows_c.append(row_c)

        # run the timestep function
        macrophages, candida = timestep(macrophages, candida, params, rng)


    # create dataframe and save output

    df = pd.DataFrame(rows_m)
    #df.to_csv('simulation.csv')
    fig = df.plot(y=["n_m_0000","n_m_0001","n_m_0010","n_m_0011","n_m_0100","n_m_0101","n_m_0110","n_m_0111","n_m_1000","n_m_1001","n_m_1010","n_m_1011","n_m_1100","n_m_1101","n_m_1110","n_m_1111"]).get_figure()
    fig.savefig('simulation_m.pdf')
    df = pd.DataFrame(rows_c)
    #df.to_csv('simulation.csv')
    fig = df.plot(y=["n_c_0000","n_c_0001","n_c_0010","n_c_0011","n_c_0100","n_c_0101","n_c_0110","n_c_0111","n_c_1000","n_c_1001","n_c_1010","n_c_1011","n_c_1100","n_c_1101","n_c_1110","n_c_1111"]).get_figure()
    fig.savefig('simulation_c.pdf')

if __name__ == "__main__":
    main()