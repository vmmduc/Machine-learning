import random

POP_SIZE = 8
ELITE_SCHROM_NUMBER = 1
SELECTION_SIZE = 4
RATE = 0.25
TARGET_SCHROM = [1, 1, 0 ,1, 0, 0, 1, 1, 1, 0]
class schrom:
    def __init__(self):
        self._gens = []
        self.fitness = 0
        i = 0
        while i < TARGET_SCHROM.__len__():
            if random.random() >= 0.5:
                self._gens.append(1)
            else:
                self._gens.append(0)
            i += 1

    def get_gens(self):
        return self._gens

    def get_fitness(self):
        self.fitness = 0
        for i in range(self._gens.__len__()):
            if self._gens[i] == TARGET_SCHROM[i]:
                self.fitness +=1
        return self.fitness

    def __str__(self):
        return self._gens.__str__()

class Population:
    def __init__(self, size):
        self._schrom = []
        i = 0
        while i < size:
            self._schrom.append(schrom())
            i += 1
    
    def get_schrom(self):
        return self._schrom
    
class GA:
    @staticmethod
    def evol(pop):
        return GA._mutate(GA._crossover(pop))

    @staticmethod
    def _crossover(pop):
        crossover = Population(0)
        for i in range(ELITE_SCHROM_NUMBER):
            crossover.get_schrom().append(pop.get_schrom()[i])
        i = ELITE_SCHROM_NUMBER
        while i < POP_SIZE:
            schrom1 = GA.selected(pop).get_schrom()[0]
            schrom2 = GA.selected(pop).get_schrom()[0]
            crossover.get_schrom().append(GA._crossover_schrom(schrom1,schrom2))
            i += 1
        return pop
    

    @staticmethod
    def _mutate(pop):
        for i in range(ELITE_SCHROM_NUMBER, POP_SIZE):
            GA._mutate_schrom(pop.get_schrom()[i])
        return pop

    @staticmethod
    def _crossover_schrom(schrom1, schrom2):
        crossover_schrom = schrom()
        for i in range(TARGET_SCHROM.__len__()):
            if random.random() > 0.75:
                crossover_schrom.get_gens()[i] = schrom1.get_gens()[i]
            else:
                crossover_schrom.get_gens()[i] = schrom2.get_gens()[i]
        return crossover_schrom

    @staticmethod
    def _mutate_schrom(schrom):
        for i in range(TARGET_SCHROM.__len__()):
            if random.random() < RATE:
                schrom.get_gens()[i] = 1
            else:
                schrom.get_gens()[i] = 0

    @staticmethod
    def selected(pop):
        select_pop = Population(0)
        i = 0
        while i < SELECTION_SIZE:
            select_pop.get_schrom().append(pop.get_schrom()[random.randrange(0,POP_SIZE)])
            i += 1
        select_pop.get_schrom().sort(key = lambda x: x.get_fitness(), reverse = True)
        return select_pop

def _output(Pop, gen_Number):
    print("Generation: ", gen_Number," | fitness: ", Pop.get_schrom()[0].get_fitness())
    print("Target Chromosome:", TARGET_SCHROM)
    print("------------------------------------")
    i = 0
    for x in Pop.get_schrom():
        print(i," : ", x, " fitness: ", x.get_fitness())
        i += 1

pop = Population(POP_SIZE)
pop.get_schrom().sort(key = lambda x : x.get_fitness(), reverse = True)
_output(pop,0)
generation_number = 1
while pop.get_schrom()[0].get_fitness() < TARGET_SCHROM.__len__():
    pop = GA.evol(pop)
    pop.get_schrom().sort(key = lambda x : x.get_fitness(), reverse = True)
    _output(pop, generation_number)
    generation_number += 1
    