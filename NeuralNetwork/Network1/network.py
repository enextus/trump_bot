"""

network.py Модуль создания и обучения нейронной сети для распознавания рукописных цифр
с использованием метода градиентного спуска.
Python Kurs; Eduard;

"""
#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, sys
import random
import numpy as np

""" Описание класса Network """

# используется для описания нейронной сети
class Network(object):
    def __init__(self, sizes): # конструктор класса; # self – указатель на объект класса;
    
    # sizes – список размеров слоев нейронной сети
    self.num_layers = len(sizes) # задаем количество слоев нейронной сети
    self.sizes = sizes # задаем список размеров слоев нейронной сети
    self.biases = [np.random.randn(y, 1) for y in sizes[1:]] # задаем случайные начальные смещения
    self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])] # задаем случайные начальные веса связей

    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
            return a


# определение сигмоидальной функции активации
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

""" --Конец описания класса Network--"""

""" ---Тело программы--- """

net = Network([2, 3, 1]) # создаем нейронную сеть из трех слоев

""" ---Конец тела программы--- """

""" Вывод результата на экран: """

print('Сеть net:')
print('Количетво слоев:', net.num_layers)
for i in range(net.num_layers):
    print('Количество нейронов в слое', i,':',net.sizes[i])
for i in range(net.num_layers-1):
    print('W_',i+1,':')
    print(np.round(net.weights[i],2))
    print('b_',i+1,':')
    print(np.round(net.biases[i],2))
