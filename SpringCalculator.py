import numpy as np

class SpringCalculator:
    def __init__(self, graph):
        self.graph = graph
        self.maxSpringK = 1e9
        self.minSpringK = -1e9
        self.meanSpringK = 1.

    def recomputeNodalGradients(self):
        self.recomputeTruncationData() 

    def recomputeTruncationData(self):
        #return
        springKs = np.empty(shape=(0,0))
        for edge in self.graph.getEdges():
            candidateSpringK = self.getUntruncatedSpringStiffness(edge[0], edge[1])
            if candidateSpringK > 1e-6:
                springKs = np.append(springKs, candidateSpringK)

        self.maxSpringK = np.percentile(springKs, 80.)
        self.minSpringK = np.percentile(springKs, 20.)
        self.meanSpringK = np.mean(springKs)

    def getUntruncatedSpringStiffness(self, firstNode, secondNode):
        deltaGradient = np.linalg.norm(self.gradientField(firstNode.position) - self.gradientField(secondNode.position)) 
        return deltaGradient
    
    def getSpringStiffness(self, firstNode, secondNode):
        springStiff = self.getUntruncatedSpringStiffness(firstNode, secondNode)
        return self.truncateSpringStiffness(springStiff)

    def truncateSpringStiffness(self, springForce):
        avgK    = springForce/ self.meanSpringK
        avgMaxK = self.maxSpringK/self.meanSpringK 
        avgMinK = self.minSpringK/self.meanSpringK 
        return max(min(avgMaxK,avgK), avgMinK);

    def gradientField(self, nodePos):
        return self.intGaussian(nodePos[0], 11, 1)

    def gaussian(self, x, center, stdDeviation):
        return np.exp(-np.power(x-center,2.)/(2.*stdDeviation**2)) / (np.sqrt(2.*np.pi)*stdDeviation)

    def diffGaussian(self, x, center, stdDeviation):
        return (center-x)/(np.sqrt(2.*np.pi)*stdDeviation**3) * np.exp(-np.power(x-center,2.)/(2.*stdDeviation**2))

    def intGaussian(self, x, center, stdDeviation):
        import scipy.special
        return 0.5 * scipy.special.erfc((center-x)/(np.sqrt(2)*stdDeviation))
