from NeuralNetwork import NeuralNetwork
import random

class GeneticSearch:
    def __init__(self, populationSize, crossoverRate, mutationRate, architecture):
        self.populationSize = populationSize
        self.crossoverRate = crossoverRate
        self.mutationRate = mutationRate
        self.architecture = architecture
        self.population = []

        for i in range(populationSize):
            self.population.append(NeuralNetwork(architecture))

    def getPopulation(self):
        return self.population

    def mutation(self,population):
            for individual in population:
                network = individual.getNetwork()
                for layer in network:
                    for neuron in layer:
                        for i in range(len(neuron)):
                            if random.random() < self.mutationRate:
                                neuron[i] += random.gauss(0,1)

    def crossOver(self,p1,p2):
        alpha = random.random()
        f1 = NeuralNetwork(self.architecture)
        f2 = NeuralNetwork(self.architecture)
        if random.random() < self.crossoverRate:
            for i in range(len(f1.getNetwork())):
                for j in range(len(f1.getNetwork()[i])):
                    for k in range(len(f1.getNetwork()[i][j])):
                        f1.getNetwork()[i][j][k] = alpha * p1.getNetwork()[i][j][k] + (1-alpha) * p2.getNetwork()[i][j][k]
                        f2.getNetwork()[i][j][k] = alpha * p2.getNetwork()[i][j][k] + (1-alpha) * p1.getNetwork()[i][j][k]
            return (f1,f2)
        else:
            return(p1,p2)
                        
    def selection(self,fitness):
        parents_list = []
        F = sum(fitness)
        acum_prob = [fitness[0]/F]
        for i in range(1,len(fitness)):
            acum_prob.append(fitness[i]/F + acum_prob[i-1])
        for i in range(len(fitness)):
            index = 0
            num = random.random()
            while(acum_prob[index] < num):
                index+=1
            parents_list.append(self.population[index])
        return parents_list

    def reproduction(self,parents_list):
        newPopulation = []

        for i in range(1,len(parents_list),2):
            childrens = self.crossOver(parents_list[i],parents_list[i-1])
            for children in childrens:
                newPopulation.append(children)
        self.mutation(newPopulation)
        
        return newPopulation

    def evolution(self,fitness):
        parents_list = self.selection(fitness)
        self.population = self.reproduction(parents_list)
