from player import Player
from macrophage import Macrophage
from candida import Candida
from payoff import Payoff
from match import Match
import numpy as np

class Simulator():

    def __init__(self, m_no, c_no, m_strat, c_strat, payoff, steps, repl_steps, mut_rate_point, mut_rate_mem, nu, lam, alpha, delta, seed = 1234):
        self.generator = np.random.default_rng(seed)
        self.m_no = m_no
        self.c_no = c_no
        self.steps = steps
        self.replsteps = repl_steps
        self.mut_rate_point = mut_rate_point
        self.mut_rate_mem = mut_rate_mem
        self.m_strat = m_strat
        self.c_strat = c_strat
        self.payoff = payoff
        self.macrophages = list()
        self.candidas = list()
        self.m_population_history = [self.m_no]
        self.c_population_history = [self.c_no]
        self.nu = nu
        self.lam = lam
        self.alpha = alpha
        self.delta = delta

        # create players
        for _ in range(self.m_no):
            if self.m_strat != None:
                self.macrophages.append(Macrophage(self.m_strat, self.generator))
            else:
                strat = ''
                for i in range(2):
                    strat += self.generator.choice(['0', '1'])
                self.macrophages.append(Macrophage(strat, self.generator))
        for _ in range(self.c_no):
            if self.c_strat != None:
                self.candidas.append(Candida(self.c_strat, self.generator))
            else:
                strat = ''
                for i in range(2):
                    strat += self.generator.choice(['0', '1'])
                self.candidas.append(Candida(strat, self.generator))

    def wrap_indices(self, input_list, num_values):
        if len(input_list) == 0:
            return list()
        return [i % len(input_list) for i in range(num_values)]

    def run(self):
        repl_steps = self.generator.choice(range(self.replsteps[0], self.replsteps[1]))
        for step in range(self.steps):
            if len(self.macrophages) >= len(self.candidas):
                c_choices = self.wrap_indices(self.candidas, len(self.macrophages))
                if len(c_choices) == 0:
                    pass
                else:
                    self.generator.shuffle(c_choices)            
                    for m in range(len(self.macrophages)):
                        match = Match(self.macrophages[m], self.candidas[c_choices[m]], self.payoff, 1, 0)
                        score = match.play()
                        self.macrophages[m].add_score(score[0])
                        self.candidas[c_choices[m]].add_score(score[1])
            else:
                m_choices = self.wrap_indices(self.macrophages, len(self.candidas))
                if len(m_choices) == 0:
                    pass
                else:
                    self.generator.shuffle(m_choices)            
                    for c in range(len(self.candidas)):
                        match = Match(self.macrophages[m_choices[c]], self.candidas[c], self.payoff, 1, 0)
                        score = match.play()
                        self.candidas[c].add_score(score[1])
                        self.macrophages[m_choices[c]].add_score(score[0])


            if step % repl_steps == 0:
                # Sort macrophages and candida according to score
                sorted_candida = self.sort_population_by_score(self.candidas)
                sorted_macrophages = self.sort_population_by_score(self.macrophages)
            
                # removal
                remove_candida = self.compute_removal_rate(self.lam, self.macrophages, self.candidas)
                remove_macrophage = self.compute_removal_rate(self.nu, self.candidas, self.macrophages)
                self.macrophages = self.remove_lowest_x(self.macrophages, sorted_macrophages, remove_macrophage)
                self.candidas = self.remove_lowest_x(self.candidas, sorted_candida, remove_candida)

                print()
                print((len(self.macrophages), len(self.candidas)))
                print((remove_macrophage, remove_candida))

                sorted_candida = self.sort_population_by_score(self.candidas)
                sorted_macrophages = self.sort_population_by_score(self.macrophages)

                # replication
                repl_macrophage = self.compute_replication_rate(self.alpha, self.macrophages)
                repl_candida = self.compute_replication_rate(self.delta, self.candidas)
                print((repl_macrophage, repl_candida))
                print("----------------------")
                print((len(self.macrophages), len(self.candidas)))
                for _ in range(repl_candida):
                    new_candida = Candida(self.candidas[sorted_candida[-_]].strategy, self.generator)
                    new_candida.mutate(self.mut_rate_point, self.mut_rate_mem, self.generator)
                    self.candidas[sorted_candida[-_]].mutate(self.mut_rate_point, self.mut_rate_mem, self.generator)
                    self.candidas.append(new_candida)
                for _ in range(repl_macrophage):
                    new_macrophage = Macrophage(self.macrophages[sorted_macrophages[-_]].strategy, self.generator)
                    new_macrophage.mutate(self.mut_rate_point, self.mut_rate_mem, self.generator)
                    self.macrophages[sorted_macrophages[-_]].mutate(self.mut_rate_point, self.mut_rate_mem, self.generator)
                    self.macrophages.append(new_macrophage)
                #repl_ready = self.get_replication_ready(self.macrophages, sorted_macrophages, repl_steps)
                #print(len(repl_ready))
                #for _ in range(min(len(repl_ready), repl_macrophage)):
                #    new_macrophage = Macrophage(self.macrophages[repl_ready[-_]].strategy, self.generator)
                #    new_macrophage.mutate(self.mut_rate_point, self.mut_rate_mem, self.generator)
                #    self.macrophages[repl_ready[-_]].mutate(self.mut_rate_point, self.mut_rate_mem, self.generator)
                #    self.macrophages.append(new_macrophage)
                #print((len(self.macrophages), len(self.candidas)))
                repl_steps = self.generator.choice(range(self.replsteps[0], self.replsteps[1]))
            self.m_population_history.append(len(self.macrophages))
            self.c_population_history.append(len(self.candidas))


    def get_history(self):
        return [self.m_population_history, self.c_population_history]
        
    def remove_lowest_x(self, population, indices, x):
        for i in indices[:x]:
            population[i] = None
        population = [individual for individual in population if individual is not None]
        return population

    def get_replication_ready(self, population, indices, repl_steps) -> [int]:
        return [i for i in indices if population[i].get_replication_state(repl_steps, self.generator) == True]
    
    def sort_population_by_score(self, population, rev = True) -> [int]:
        return sorted(range(len(population)), key=lambda individual: population[individual].get_score(), reverse=rev)
            
    def get_mean_fitness(self, population: [Player]):
        fitness = 0
        if len(population) > 0:
            for individual in population:
                fitness += individual.get_score()
            fitness = fitness/len(population)
        return fitness

    def compute_removal_rate(self, rate: float, population_a: [Player], population_b: [Player]) -> int:
        mean_fitness_a = self.get_mean_fitness(population_a)
        mean_fitness_b = self.get_mean_fitness(population_b)
        
        div = (mean_fitness_b/mean_fitness_a) if mean_fitness_a > 0 else 0
        return round(rate * len(population_a))

    def compute_replication_rate(self, rate, population) -> int:
        return round(rate*len(population))