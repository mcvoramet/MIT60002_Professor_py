# Graph represented as adjacency matrix
# 1 - if there is a connection
# 0 - if there is no connection

class Node(object):
    def __init__(self, name):
        """Assume name is a string"""
        self.name = name
    def getName(self):
        return self.name
    def __str__(self):
        return self.name

class Edge(object):
    def __init__(self, src, dest):
        """Assumes src and dest are nodes"""
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return self.src.getName() + '->' + self.dest.getName()

class Digraph(object): # Directed Graph
    """edges is a dict mapping each node to a list of its children"""

    def __init__(self):
        self.edges = {} #{nodes:[edges]}

    def addNode(self, node):   # check to make sure that it's not already in the dictionary
        if node in self.edges:
            raise ValueError("Duplicate node")
        else:
            self.edges[node] = []
        
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not (src in self.edges and dest in self.edges): # make sure they're both in the dictionary
            raise ValueError("Node not in graph")
        self.edges[src].append(dest)

    def childrenOf(self, node): # want to get all the children of a particular node
        return self.edges[node]

    def hasNode(self, node): # want to know if the node is in the graph
        return node in self.edges
    
    def getNode(self, name): # want to get a node by its name
        for n in self.edges:
            if n.getName() == name:
                return n
        raise NameError(name) # this will raise only when it couldn't find the node

    def __str__(self): # print out all of the link in the graph
        result = ''
        for src in self.edges:
            for dest in self.edges[src]:
                result = result + src.getName() + '->' + dest.getName() + '\n'
        return result[:-1] # omit final newline (\n)

class Graph(Digraph): # Undirected Graph
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)

def buildCityGraph(graphType):
    g = graphType()
    for name in ('Boston', 'Providence', 'New York', 'Chicago',
                'Denver', 'Phoenix', 'Los Angeles'): #Creaet 7 nodes
                g.addNode(Node(name))

    g.addEdge(Edge(g.getNode('Boston'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('Providence')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('Boston')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('New York'), g.getNode('Chicago')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Denver')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Los Angeles'), g.getNode('Boston')))
    
    return g

g = buildCityGraph(Digraph)
print(g)

def printPath(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result

# Build the Depth First Search function
def DFS(graph, start, end, path, shortest, toPrint=False):
    path = path + [start] # path is initially an empty list
    if toPrint:
        print('Current DFS path:', printPath(path))
    if start == end:
        return path
    for node in graph.childrenOf(start): # loop over teh children of the start node
        if node not in path: # avoid cycles
            if shortest == None or len(path) < len(shortest): # if no solution yet...
                newPath = DFS(graph, node, end, path, shortest, toPrint) # Recursively do DFS (`node` track how will explore all paths through first node before...)
                if newPath != None:
                    shortest = newPath
                
        elif toPrint:
            print('Already visited', node) # get out of the loop

    return shortest

def DFSshortestPath(graph, start, end, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return DFS(graph, start, end, [], None, toPrint)


# Build a Breadth First Search function
def BFS(graph, start, end, toPrint = False):
    initPath = [start]
    pathQueue = [initPath] # list of path
    while len(pathQueue) != 0:
        #Get and remove oldest element in pathQueue
        tmpPath = pathQueue.pop(0) # if didn't found the solution
        if toPrint:
            print('Current BFS path:', printPath(tmpPath))
        lastNode = tmpPath[-1] # grab last point in that path and then explore
        if lastNode == end:
            return tmpPath # found solution -> stop!
        for nextNode in graph.childrenOf(lastNode): # keep looping until find the solution
            if nextNode not in tmpPath:
                newPath = tmpPath + [nextNode]
                pathQueue.append(newPath)

    return None # If no solution return None

def BFSshortestPath(graph, start, end, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return BFS(graph, start, end, toPrint)

# test shortest path 
def testSP(source, destination):
    g = buildCityGraph(Digraph)
    # Choose one (DFS or BFS)
    #sp = DFSshortestPath(g, g.getNode(source), g.getNode(destination), toPrint=True)
    sp = BFSshortestPath(g, g.getNode(source), g.getNode(destination), toPrint=True)
   
    if sp!= None:
        print('Shortest path from', source, 'to', destination, 'is', printPath(sp))
    
    else:
        print('There is no path from', source, 'to', destination) 

testSP('Boston', 'Phoenix')
        
# DFS: Always following the next available edge until stuck then it will do the backtrack.
#      It's easily modified to solve shortest path prblem (have weight).

# BFS: Always exploring the next equal length option and keep track in that queue
#      of the things left to do as walking way through.
#      It's can't easily be modified because the short weithgted path may have many more
#      than the minimum numbers of loops.