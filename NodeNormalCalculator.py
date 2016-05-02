import numpy as np
from SpringNodeData import NodeType

class NodeNormalCalculator:
    def __init__(self, graph):
        self.graph = graph
        self.nodeNormals = {}
    def recomputeNormals(self):
        for nodeID, node in self.graph.getNodes():
            if node.boundaryCond == NodeType.Boundary:
                #print nodeID
                normal = self.computeNodeNormal(nodeID, node)
                self.nodeNormals[nodeID] = normal
    def computeNodeNormal(self, nodeID, node):
        boundaryNodeIDs = []
        for neighborID, neighborNode in self.graph.getConnectedToID(nodeID):
            #print neighborID
            if neighborNode.boundaryCond in [NodeType.Boundary, NodeType.Locked]:
                boundaryNodeIDs.append(neighborID)
        #check if the boundary points are collinear
        #for 2D there should be only 3 neighboring nodes and thus 2 vectors
        vector1 = self.graph.getNode(boundaryNodeIDs[0]).position - self.graph.getNode(nodeID).position
        vector2 = self.graph.getNode(boundaryNodeIDs[1]).position - self.graph.getNode(nodeID).position
        
        vector1 = vector1/np.linalg.norm(vector1)
        vector2 = vector2/np.linalg.norm(vector2) 
        
        angle = np.dot(vector1, vector2)
        if abs(angle) - 1.< 1e-3:
            return np.array([vector1[1], -vector1[0]])
        else:
           import sys
           sys.exit("Error, non-collinear points in boundary nodes")
    def getBoundaryNodeNormal(self, nodeID):
        return self.nodeNormals[nodeID]
