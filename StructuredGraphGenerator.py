import numpy as np
import SimpleGraph
from SpringNodeData import *

class StrucutredGraphGenerator:
    def __init__(self, nbRows, nbCols, positionFun):
        self.nbRows = nbRows
        self.nbCols = nbCols
        self.positionFun = positionFun

    def getNodeType(self, row, col):
        maxRow = self.nbRows-1
        maxCol = self.nbCols-1
        if row in [0, maxRow] or col in [0, maxCol]: 
            if (row, col) in [(0,0), (0,maxCol), (maxRow,0), (maxRow,maxCol)]:
                return NodeType.Locked
            elif row in [0 , maxRow] or col in [0, maxCol]:
                return NodeType.Boundary
            else:
                return NodeType.Locked
        else:
            return NodeType.Inner
     
    def getNodeID(self, row, col):
        return row * self.nbCols + col 

    def generateStrucutredGraph(self):
        nbNodes = self.nbRows * self.nbCols
        myGraph = SimpleGraph.Graph(2)

        for rowID in range(self.nbRows):
            for colID in range(self.nbCols):
                nodeID = self.getNodeID(rowID,colID)
                nodeType = self.getNodeType(rowID,colID)
                nodePos = np.array(self.positionFun(colID,rowID))
                nodeGrad = 0.
                myGraph.addNode(SpringNode(nodePos, nodeGrad, nodeType))
                if colID-1 >= 0:
                    myGraph.addEdge(nodeID, self.getNodeID(rowID,colID-1))
                if rowID-1 >= 0:
                    myGraph.addEdge(nodeID, self.getNodeID(rowID-1,colID))
        return myGraph
