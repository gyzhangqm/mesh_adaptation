class Graph:
    def __init__(self, dim):
        self.connectivityTable = list() 
        self.nodes = list()
        
    def addNode(self, node):
        self.nodes.append(node)
        self.connectivityTable.append([])
    
    def addEdge(self, nodeID1, nodeID2):
        if not nodeID1 in self.connectivityTable[nodeID2] or nodeID1 != nodeID2:
            self.connectivityTable[nodeID1] = self.connectivityTable[nodeID1] + [nodeID2]
            self.connectivityTable[nodeID2] = self.connectivityTable[nodeID2] + [nodeID1]

    def getConnectedToID(self, nodeID):
        for neigborNodeID in self.connectivityTable[nodeID]:
            yield (neigborNodeID, self.nodes[neigborNodeID])

    def getNodes(self):
        for nodeID in range(len(self.nodes)):
            yield nodeID, self.nodes[nodeID]

    def getNode(self, nodeID):
        return self.nodes[nodeID]

    def getEdges(self):
        for nodeID1, node1 in self.getNodes():
            for nodeID2, node2 in self.getConnectedToID(nodeID1):
                yield (node1, node2)

#class Graph2:
#    class GraphVertex:
#        def __init__(self, vertexID, vertexData)
#            self.vertexID = vertexID
#            self.vertexData = vertexData
#    class GraphEdge:
#        def __init__(self, edgeID, vertex1, vertex2, edgeData)
#            self.edgeID = edgeID
#            self.vertex1 = vertex1
#            self.vertex2 = vertex2
#            self.edgeData = edgeData
#
#    def __init__(self, dim):
#        self.connectivityTable = list() 
#        self.nodesData = list()
#        self.edgesData = list()
#        
#    def addNode(self, nodeData):
#        self.nodeData.append(nodeData)
#        self.connectivityTable.append([])
#    
#    def addEdge(self, nodeID1, nodeID2, edgesData):
#        if not nodeID1 in self.connectivityTable[nodeID2] or nodeID1 != nodeID2:
#            edgeID = len(self.edgesData)
#            self.edgesData.append( (nodeID1, nodeID2, edgesData) )
#            self.connectivityTable[nodeID1].append( (nodeID2, edgeID) )
#            self.connectivityTable[nodeID2].append( (nodeID1, edgeID) )
#
#    def getNode(self, nodeID):
#        return GraphVertex(nodeID, self.nodesData[nodeID])
#
#    def getEdge(self, edgeID):
#        firstNodeID = self.edgesData[edgeID][0]
#        secondNodeID = self.edgesData[edgeID][1]
#        edgeData = self.edgesData[edgeID][2]
#        return GraphVertex(edgeID, firstNodeID, secondNodeID, edgeData)
#
#    def getNodes(self):
#        for nodeID in range(len(self.nodesData)):
#            yield self.getNode(nodeID)
#
#    def getEdges(self):
#        for edgeID in range(len(self.edgesData)): 
#            yield self.getEdge(edgeID)
#    
#    def getNodesConnectedToNodeID(self, nodeID):
#        for neigborNodeID, edgeID in self.connectivityTable[nodeID]:
#            yield self.getNode(neigborNodeID)
#
#    def getEdgesConnectedToNodeID(self, nodeID):
#        for neigborNodeID, edgeID in self.connectivityTable[nodeID]:
#            yield self.getEdge(edgeID)
#
#
