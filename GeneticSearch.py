import NeuralNetwork as nn
import random
#import numpy as np

class GeneticSearch:
    def __init__(self, crossoverRate, mutationRate, populationSize, neuralConfiguration):
        self.crossoverRate = crossoverRate
        self.mutationRate = mutationRate
        self.populationSize = populationSize
        self.neuralConfiguration = neuralConfiguration
        self.population = []
        for i in range(populationSize):
            self.population.append(nn.NeuralNetwork(neuralConfiguration))

    def getPopulation(self):
        return self.population.copy()

    def mutation(self,new_population):
        new_population_aux = new_population[:]
        for i in range(len(new_population_aux)):
            network_aux = new_population_aux[i].getNetwork()
            for layer in network_aux:
                for neuron in layer:
                    for k in range(len(neuron)):
                        if random.random() <= self.mutationRate:
                            neuron[k] += random.gauss(0,1)
            new_population_aux[i].setNetwork(network_aux)
        return new_population_aux.copy()

    def crossOver(self, p1, p2):
        alpha = random.random()
        f1 = nn.NeuralNetwork([self.neuralConfiguration])
        f2 = nn.NeuralNetwork([self.neuralConfiguration])
        f1.setNetwork(p1.getNetwork())
        f2.setNetwork(p2.getNetwork())
        if random.random() <= self.crossoverRate:
            p1_aux = p1.getNetwork()
            p2_aux = p2.getNetwork()
            f1_aux = f1.getNetwork()
            f2_aux = f2.getNetwork()
            for i in range(len(p1_aux)):
                for j in range(len(p1_aux[i])):
                    for k in range(len(p1_aux[i][j])):
                        f1_aux[i][j][k] = alpha*p1_aux[i][j][k] + (1-alpha)*p2_aux[i][j][k]
                        f2_aux[i][j][k] = (1-alpha)*p1_aux[i][j][k] + alpha*p2_aux[i][j][k]
            f1.setNetwork(f1_aux)
            f2.setNetwork(f2_aux)
            
        return f1,f2

    def reproduction(self, parents_list):
        new_population = []
        for i in range(1,len(parents_list),2):
            children = self.crossOver(parents_list[i-1],parents_list[i])
            for j in range(2):
                new_population.append(children[j])
        new_population = self.mutation(new_population)
        return new_population.copy()

    def selection(self,fitness):
        F = sum(fitness)
        probs = []
        acum_probs = []
        index_pop = []
        parents_list = []
        for i in range(len(fitness)):
            probs.append(fitness[i]/F)
            if i > 0:
                acum_probs.append(probs[i] + acum_probs[i-1])
            else:
                acum_probs.append(probs[i])
        for i in range(len(fitness)):
            index = 0
            num = random.random()
            for j in range(len(acum_probs)):
                if acum_probs[j] >= num:
                    index = j
                    break
            parents_list.append(self.population[index])
        return parents_list.copy()

    def evolution(self, fitness):
        parents_list = self.selection(fitness)
        self.population = self.reproduction(parents_list)

