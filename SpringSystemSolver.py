import numpy as np
from SpringNodeData import *
from NodeNormalCalculator import NodeNormalCalculator

class SpringSystemSolver:
    def __init__(self, nodeGraph, springCalculator):
        self.nodeGraph = nodeGraph
        self.springCalculator = springCalculator
        self.nodeNormalCalulator = NodeNormalCalculator(nodeGraph)
        self.nodeNormalCalulator.recomputeNormals()

        self.coeffMatrix = np.zeros(0) 
        self.rightHandSide = np.zeros(0)
        self.solution = np.zeros(0)
        self.nbNodes = 0
        self.nbDim = 0

        self.resizeSystemData()
        self.acceleration = 0.01

    def assembleLockedNode(self, nodeID, node):
        for iDim in range(self.nbDim): 
            self.coeffMatrix[iDim, nodeID, iDim, nodeID] = 1.
            self.rightHandSide[iDim, nodeID] = node.position[iDim]
    
    def assembleBoundaryNode(self, nodeID, node):
        normalDirection = self.nodeNormalCalulator.getBoundaryNodeNormal(nodeID)
        tangentDirection = np.array([normalDirection[1], -normalDirection[0]])
        dependentDim = np.argmin(abs(tangentDirection))
        freeDim = (1 if dependentDim == 0 else 0)
       
        #Dependent Dim, following the line equation 1*y - m*x = b, where y is the dep dim and x is the free dim)
        slope = tangentDirection[dependentDim]/tangentDirection[freeDim]
        y_intersect = node.position[dependentDim] - slope * node.position[freeDim]
        self.coeffMatrix[dependentDim, nodeID, dependentDim, nodeID] = 1.
        self.coeffMatrix[dependentDim, nodeID, freeDim, nodeID] = -slope
        self.rightHandSide[dependentDim, nodeID] = y_intersect
 
        #Free Dimension, acting like an inner node
        totalSpring = 0.
        for connectedNodeID, connectedNode in self.nodeGraph.getConnectedToID(nodeID):
            springK = self.springCalculator.getSpringStiffness(node, connectedNode)
            edgeDirection = connectedNode.position - node.position
            dotProduct = np.dot(edgeDirection, tangentDirection) /  np.linalg.norm(edgeDirection)
            projectedSpringK = springK * dotProduct
            totalSpring += springK
            self.coeffMatrix[freeDim, nodeID, freeDim, connectedNodeID] = abs(projectedSpringK)
        self.coeffMatrix[freeDim, nodeID, freeDim, nodeID] = -np.sum(self.coeffMatrix[freeDim, nodeID, freeDim, :]) 
        self.rightHandSide[freeDim, nodeID] = np.sum(self.coeffMatrix[freeDim, nodeID, freeDim, :]) * 1.
 
    def assembleInnerNode(self, nodeID, node):
        for iDim in range(self.nbDim):
            for connectedNodeID, connectedNode in self.nodeGraph.getConnectedToID(nodeID):
                springK = self.springCalculator.getSpringStiffness(node, connectedNode)
                self.coeffMatrix[iDim, nodeID, iDim, connectedNodeID] = springK
            self.coeffMatrix[iDim, nodeID, iDim, nodeID] = -np.sum(self.coeffMatrix[iDim, nodeID, iDim, :])
            self.rightHandSide[iDim, nodeID] = np.sum(self.coeffMatrix[iDim, nodeID, iDim, :]) * 1.

    def iterate(self):
        self.springCalculator.recomputeNodalGradients()
        self.resizeSystemData()
        self.assembleSystem()
        self.solveSystem()
        self.updateNodes()

    def assembleSystem(self):
        for iNodeID, iNode in self.nodeGraph.getNodes():
            if iNode.boundaryCond == NodeType.Locked:
                self.assembleLockedNode(iNodeID, iNode)
            elif iNode.boundaryCond == NodeType.Boundary:
                self.assembleBoundaryNode(iNodeID, iNode)
            else:
                self.assembleInnerNode(iNodeID, iNode)

    def resizeSystemData(self):
        self.nbNodes = max(enumerate(self.nodeGraph.getNodes()))[0] + 1
        self.nbDim = np.shape(self.nodeGraph.getNode(0).position)[0]
        
        self.coeffMatrix[:] = 0.
        self.rightHandSide[:] = 0.
        self.solution[:] = 0.
        
        self.coeffMatrix.resize(self.nbDim, self.nbNodes, self.nbDim, self.nbNodes)
        self.rightHandSide.resize(self.nbDim, self.nbNodes)
        self.solution.resize(self.nbDim, self.nbNodes)

    def solveSystem(self):
        nbDofs = self.nbNodes * self.nbDim
        #np.set_printoptions(edgeitems=100, infstr='inf', linewidth=2000, nanstr='nan', \
        #        precision=8,  suppress=False, threshold=1000, formatter=None)
        #print self.coeffMatrix.reshape(nbDofs, nbDofs)
        #print self.rightHandSide.reshape(nbDofs, 1)

        self.solution = np.linalg.solve(self.coeffMatrix.reshape(nbDofs,nbDofs), \
                self.rightHandSide.reshape(nbDofs)).reshape(self.nbNodes,self.nbDim,order='F')

    def updateNodes(self):
        for nodeID, node in self.nodeGraph.getNodes():
            newNodePos = self.solution[nodeID,:]
            #print 'nodes: ', newNodePos
            updatedNodePos = self.acceleration * newNodePos + (1.-self.acceleration) * node.position
            node.position = updatedNodePos
