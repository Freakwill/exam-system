#!/usr/bin/env python

import random

def rand(problems, n=1, excluded=True, rate=0.25):
    ret = []
    for _ in range(n):
        if problems:
            p = random.choice(problems)
            problems.remove(p)
            if excluded:
                problems = [problem for problem in problems if problem.realm != p.realm or random.random()<rate]
            ret.append(p)
    return ret


def deap(problems, n=1, n_fills=20, excluded=True):
    import toolz
    import numpy as np
    from deap import base, creator, tools, algorithms

    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))  # 两个目标
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMulti)

    IND_SIZE = len(problems)  # 决策变量个数

    toolbox = base.Toolbox()

    def create_individual():
        return creator.Individual(np.random.randint(0, 2, IND_SIZE))

    toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluate(individual):
        ps = [p for k, p in zip(individual, problems) if k]
        obj1 = abs(sum(p.n_fills for p in ps) - n_fills)
        obj2 = len(list(toolz.unique([p.realm for p in ps])))
        return obj1, obj2

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxUniform, indpb=0.5)  # 均匀交叉
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)  # 位翻转变异
    toolbox.register("select", tools.selNSGA2)  # NSGA-II选择

    POP_SIZE = 80
    GENERATIONS = 100
    CXPB, MUTPB = 0.72, 0.2

    pop = toolbox.population(n=POP_SIZE)
    
    algorithms.eaMuPlusLambda(
        pop, toolbox,
        mu=POP_SIZE,
        lambda_=POP_SIZE,
        cxpb=CXPB, mutpb=MUTPB,
        ngen=GENERATIONS,
        verbose=False
    )
    
    best = min(pop, key=lambda ind: ind.fitness.values[1])

    return [p for k, p in zip(best, problems) if k]

