from heapq import heappop, heappush
from math import log, exp

def dijkstra(graph, weight, source=0, target=None):
    """single source shortest paths by Dijkstra

       :param graph: directed graph in listlist or listdict format
       :param weight: in matrix format or same listdict graph
       :assumes: weights are non-negative
       :param source: source vertex
       :type source: int
       :param target: if given, stops once distance to target found
       :type target: int

       :returns: distance table, precedence table
       :complexity: `O(|V| + |E|log|V|)`
    """
    n = len(graph)
    assert all(weight[u][v] >= 0 for u in range(n) for v in graph[u])
    prec = [None] * n
    black = [False] * n
    dist = [float('inf')] * n
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        dist_node, node = heappop(heap)       # Le sommet le plus proche
        if not black[node]:
            black[node] = True
            if node == target:
                break
            for neighbor in graph[node]:
                dist_neighbor = dist_node + weight[node][neighbor]
                if dist_neighbor < dist[neighbor]:
                    dist[neighbor] = dist_neighbor
                    prec[neighbor] = node
                    heappush(heap, (dist_neighbor, neighbor))
    return dist, prec



try:
    N = int(input("Please enter a number: "))
except ValueError:
    print("Oops!  That was no valid number.  Try again...")
    exit(32)
source, target = map(int, input().split())
weight = []
graph = [[] for _ in range(N)]
for i in range(N):
    p = map(float, input().split())
    weight.append(list(map(lambda p_i: -log(1 - p_i), p)))
    for j in range(N):
        if i != j:
            graph[i].append(j)
dist, _ = dijkstra(graph, weight, source, target)
"""node = target
path = []
while prec[node] is not None:
    path.append(node)
    node = prec[node]
path.append(source)"""
# print(' '.join(map(str, path[::-1])))
print(round(1 - exp(-dist[target]), 3))


