import random
import math

class NeuralNetwork:
    def __init__(self, layers):
        self.Network = []
        for i in range(1, len(layers)):
            self.Network.append([])
            for j in range(layers[i]):
                self.Network[i-1].append([])
                for k in range(layers[i-1]):
                    self.Network[i-1][j].append(random.random())

    def getNetwork(self):
        return self.Network.copy()

    def setNetwork(self, network):
        self.Network = network.copy()

    def sigmoid_logistic(self, x):
        return 1/(1 + math.e**(-x))

    def activateNeuron(self, weights, inputs):
        signal = weights[0]*(-1)
        for i in range(1,len(weights)):
            signal += weights[i]*inputs[i-1]
        return self.sigmoid_logistic(signal)

    def feedForward(self, inputs):
        for layer in self.Network:
            inputs_aux = []
            for neuron in layer:
                inputs_aux.append(self.activateNeuron(neuron,inputs))
            inputs = inputs_aux.copy()
        return inputs.copy()
