import random
import numpy as np
import sys

_upBound = []
_lowBound = []
NO_GENERATION = 0
POP_SIZE = 0
NO_VAR = 0
LGEN = 0
pCROSS = 0
pMU = 0

RATE = 1
_CurGeneration = 0
f = open("Bi-GA-Params.txt", "r")
f.readline()
f.readline()
line = f.readline().split(' ')
NO_GENERATION = int(line[0])
POP_SIZE = int(line[1])
NO_VAR = int(line[2])
LGEN = int(line[3])
f.readline()
line = f.readline().split(' ')
pCROSS = float(line[0])
pMU = float(line[1])
for i in range(NO_VAR):
    f.readline()
    line = f.readline().split(' ')
    min = float(line[0])
    max = float(line[1])
    _upBound.append(max)
    _lowBound.append(min)
f.close()

##################################################################
class BinGAIndividual:
    
    def __init__(self):
        self._schrom = []
        self._objectiveVariables = []
        self._objectiveFunctionValue = 0
        self._fitnessValue = 0

    @property
    def Schrom(self):
        return self._schrom
    @Schrom.setter
    def Schrom(self, value):
        self._schrom = value
    
    @property
    def ObjectiveVariables(self):
        return self._objectiveVariables
    @ObjectiveVariables.setter
    def ObjectiveVariables(self, value):
        self._objectiveVariables = value

    @property
    def ObjectiveFunctionValue(self):
        return self._objectiveFunctionValue
    @ObjectiveFunctionValue.setter
    def ObjectiveFunctionValue(self, value):
        self._objectiveFunctionValue = value

    @property
    def FitnessValue(self):
        return self._fitnessValue
    @FitnessValue.setter
    def FitnessValue(self, value):
        self._fitnessValue = value
    
    def Initial(self):
        for i in range(NO_VAR * LGEN):
            self._schrom.append(random.randint(0,1))
        for i in range(NO_VAR):
            self._objectiveVariables.append(0)
        self.Decode()

    def Mutation(self, c):
        if Flip(pMU) == 1:
            if c == 1:
                return 0
            else: 
                return 1
        else:
            return c

    def Crossover(self, other):
        c1 = self
        c2 = other 
        if random.random() < pCROSS:
            jcross = int(random.random() * LGEN * NO_VAR)
        else:
            jcross = LGEN * NO_VAR
        for i in range(jcross):
            c1.Schrom[i] = self.Mutation(self.Schrom[i])
            c2.Schrom[i] = self.Mutation(other.Schrom[i])
        j = jcross + 1
        for j in range(LGEN * NO_VAR):
                c1.Schrom[j] = self.Mutation(other.Schrom[j])
                c2.Schrom[j] = self.Mutation(self.Schrom[j])
        c1.Decode()
        c2.Decode()
        return c1,c2
    
    def Decode(self):
        for i in range(NO_VAR):
            sum = 0
            power = 1
            for j in range(LGEN):
                if self._schrom[i * LGEN + j] == 1:
                    sum += power
                    power *= 2
            power = sum / RATE
            x = _lowBound[i] + (_upBound[i] - _lowBound[i]) * power
            self._objectiveVariables[i] = x
        self._objectiveFunctionValue = 0

def Flip(x):
    if random.random() < x:
        return 1
    else:
        return 0

def f(x1,x2):
    return (x1 -2) * (x1 -2) + (x2 -4) * (x2 -4) 


#################################################################################
class BinGAPopulations:
    _totalFitnessValue = 1
    
    def __init__(self):
        self._parents = []
        self._chilpop = []
        self._ob = [None] * POP_SIZE
        self._optX = []
        for i in range(NO_VAR):
            self._optX.append(0)
        self._optValue = 0
        self._noElist = int(POP_SIZE * 0.1)

    def GetBestIndividual(self):
        return self._optX

    @property
    def OptimalValue(self):
        return self._optValue

    def InitPop(self):
        self._parents.clear()
        for i in range(POP_SIZE):
            idv = BinGAIndividual()
            idv.Initial()
            self._parents.append(idv)
    
    def selected(self):
        rand = random.random() * float(self._totalFitnessValue)
        partsum = 0
        for i in range(POP_SIZE):
            partsum = partsum + self._parents[i].FitnessValue
            if partsum >= rand:
                return i
        return POP_SIZE - 1

    def Generate(self):
        j = 0
        self._chilpop.clear()
        while True:
            mate1 = self.selected()
            mate2 = self.selected()
            child1,child2 = self._parents[mate1].Crossover(self._parents[mate2])
            self._chilpop.append(child1)
            self._chilpop.append(child2)
            j+=2
            if(j >= POP_SIZE): break
        
    def ScalePop(self):
        sum = sys.float_info.min
        max = sys.float_info.min
        min = sys.float_info.max
        for i in range(POP_SIZE):
            if sum < self._parents[i].ObjectiveFunctionValue:
                sum = self._parents[i].ObjectiveFunctionValue
        ave = 0
        for i in range(POP_SIZE):
            self._ob[i] = sum - self._parents[i].ObjectiveFunctionValue
            if max < self._ob[i]:
                max = self._ob[i]
            if min > self._ob[i]:
                min = self._ob[i]
            ave += self._ob[i]
        ave /= POP_SIZE
        if min > (2 * ave - max):
            a = ave / (max - ave)
            b = a * (max -2 * ave)
        else:
            a = ave / (ave - min)
            b = - min * a
        self._totalFitnessValue = 0
        for i in range(POP_SIZE):
            self._parents[i].FitnessValue = a * self._ob[i] + b
            self._totalFitnessValue += self._parents[i].FitnessValue

    def GA(self):
        self._optValue = sys.float_info.max
        self.InitPop()
        _CurGeneration = 0
        while _CurGeneration < NO_GENERATION:
            for i in range(POP_SIZE):
                self._parents[i].ObjectiveFunctionValue = f(self._parents[i].ObjectiveVariables[0], self._parents[i].ObjectiveVariables[1])
                if(self._optValue > self._parents[i].ObjectiveFunctionValue):
                    self._optValue > self._parents[i].ObjectiveFunctionValue
                    for k in range(NO_VAR):
                        self._optX[k] = self._parents[i].ObjectiveVariables[k]
            print(" The he thu: ", _CurGeneration + 1, " f = ", self._optValue)
            # xac dinh giaa tri thich nghi cua tung doi tuong
            self.ScalePop()
            # tao quan the moi
            _CurGeneration += 1
            if _CurGeneration < NO_GENERATION - 1:
                self.Generate()
        print("X1 = ", self._optX[0], " X2 = ", self._optX[1])
        self._parents.sort(key = lambda x : x.ObjectiveFunctionValue)
        for i in range(self._noElist):
            n = random.randrange(self._chilpop.__len__() - 1)
            self._chilpop.pop(n)
            self._chilpop.insert(n, self._parents[i])
        self._parents.clear()
        for j in range(POP_SIZE):
            self._parents.append(self._chilpop[j])

if __name__ == '__main__':
    ga = BinGAPopulations()
    ga.GA()