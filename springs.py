import numpy as np
import math
import sys
from matplotlib import pyplot as plt
from matplotlib import animation

from StructuredGraphGenerator import *
from GraphPlotter import *
from SpringSystemSolver import *
from SimpleGraph import Graph
from SpringCalculator import SpringCalculator

class SpringSolver:
    def __init__(self): 
        def rotate2D(pos2d, angle):
            rotationMatrix = np.array([[np.cos(angle), -np.sin(angle)], \
                                       [np.sin(angle),  np.cos(angle)] ])
            return np.dot(rotationMatrix, pos2d)
        def meshTransformation(col, row):
            pos2d = np.array([col/4., row/4.])
#            pos2d = rotate2D(pos2d, np.pi/4.)
            return 2*pos2d[0]+5, pos2d[1]

        generator = StrucutredGraphGenerator(10, 25, meshTransformation)
        self.graph =  generator.generateStrucutredGraph()
        
#        self.graph = Graph(2)
#        self.graph.addNode(SpringNode(np.array([0.,0.]), 0, NodeType.Boundary))
#        self.graph.addNode(SpringNode(np.array([1.8,2.]),0, NodeType.Inner   ))
#        self.graph.addNode(SpringNode(np.array([2.,0.]), 0, NodeType.Boundary))
#        self.graph.addNode(SpringNode(np.array([2.,2.]), 0, NodeType.Locked  ))
#        self.graph.addEdge(0,1)
#        self.graph.addEdge(1,2)
#        self.graph.addEdge(3,1)

        self.springCalculator = SpringCalculator(self.graph)
        self.systemSolver = SpringSystemSolver(self.graph, self.springCalculator)
        self.graphPlotter = GraphPlotter(self.graph)

    def update(self, frame):
        self.systemSolver.iterate()
        self.graphPlotter.plot()

    def solveSystem(self):
        self.animation = animation.FuncAnimation(self.graphPlotter.fig, self.update, interval=1)
        plt.show()
