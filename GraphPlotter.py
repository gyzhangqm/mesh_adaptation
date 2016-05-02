from matplotlib import pyplot as plt
from SpringNodeData import *
import numpy as np
from scipy.interpolate import griddata

class GraphPlotter:
    def __init__ (self, graph):
        self.graph = graph

        self.xlim = (3.5, 18.)
        self.ylim = (-.5, 3.)

        self.fig = plt.figure()
        self.figAxis = plt.axes(xlim=self.xlim, ylim=self.ylim)
        self.figAxis.set_axis_bgcolor('#263944')
        self.figAxis.get_xaxis().set_visible(False)
        self.figAxis.get_yaxis().set_visible(False)

        self.frameCount = 0
    
        edgePlotData = self.getEdgesLineData()
        self.edgesPlot, = self.figAxis.plot(edgePlotData[0], edgePlotData[1], '0.5', color='#c2d0cf')
        
        # nodePlotData = self.getNodalPointsData()
        # self.nodesPlot, = self.figAxis.plot(nodePlotData[0], nodePlotData[1], 'ro', color='#c2d0cf')
        
        #gradSurfData = self.getGradientSurfData()
        #xi = np.linspace(self.posMin[0], self.posMax[0], 100)
        #yi = np.linspace(self.posMin[1], self.posMax[1], 100)
        #zi = griddata((gradSurfData[0], gradSurfData[1]), gradSurfData[2], (xi[None,:], yi[:,None]), method='cubic')
        #print zi
        #self.gradientSurf = self.figAxis.contourf(xi,yi,zi, cmap='bone')
     
    def getNodalPointsData(self):
        xdata = []
        ydata = []
        for iNodeID, iNode in self.graph.getNodes():
            xdata.append(iNode.position[0])
            ydata.append(iNode.position[1])
        return  [xdata, ydata]

    def getEdgesLineData(self):
        xdata = []
        ydata = []
        for iNodeID, iNode in self.graph.getNodes():
            for (neigborNodeID, neigborNode) in self.graph.getConnectedToID(iNodeID):
                xdata.append(iNode.position[0])
                xdata.append(neigborNode.position[0])
                xdata.append(np.nan)
                ydata.append(iNode.position[1])
                ydata.append(neigborNode.position[1])
                ydata.append(np.nan)
        return [xdata, ydata]
    
    def getGradientSurfData(self):
        xdata = []
        ydata = []
        zdata = []
        for iNodeID, iNode in self.graph.getNodes():
            xdata.append(iNode.position[0])
            ydata.append(iNode.position[1])
            zdata.append(iNode.gradient)
        return [xdata, ydata, zdata]

    def plot(self):
        edgePlotData = self.getEdgesLineData()
        self.edgesPlot.set_data(edgePlotData[0], edgePlotData[1])
        
        #nodePlotData = self.getNodalPointsData()
        #self.nodesPlot.set_data(nodePlotData[0], nodePlotData[1])
        
        #self.frameCount += 1
