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

    def mutation(self):
        for i in range(len(self.population)):
            network_aux = self.population[i].getNetwork()
            for layer in network_aux:
                for neuron in layer:
                    for i in range(len(neuron)):
                        if random.random() <= self.mutationRate:
                            neuron[i] += random.gauss(0,1)
            self.population[i].setNetwork(network_aux)

    def crossOver(self, p1, p2):
        alpha = random.random()
        print("alpha =",alpha)
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
        for i in range(self.populationSize/2):
            for j in range(2):
                children = self.crossOver(parents_list[],)
                new_population.append()
        

    def evolution(self, fitness):
        parents_list = self.selection(fitness)
        self.population = self.reproduction(parents_list).copy()

def main():
    solução = GeneticSearch(1,0.2,4,[2,1])
    população = solução.getPopulation()
    for i in range(2):
        print(população[i].getNetwork())
    new_son = solução.crossOver(população[0],população[1])
    print("\n")
    for i in range(2):
        print(new_son[i].getNetwork())
    
main()
