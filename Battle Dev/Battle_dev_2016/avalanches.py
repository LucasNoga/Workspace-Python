Objectif

Le but de ce challenge est de trouver le chemin le moins risqué entre deux sommets. Chaque piste relie deux sommets et le risque d'avalanche de la piste est P. Chaque sommet est relié à tous les autres sommets par une piste. Par ailleurs, les probabilités d'avalanche sont indépendantes.

Petit rappel statistique

Si on note P(A), P(B) et P(C) les risques d'avalanche des pistes A, B et C, alors la probabilité qu'il n'y ait pas d'avalanche sur les pistes A, B et C sont respectivement 1-P(A), 1-P(B), 1-P(C). Comme les probabilités sont indépendantes, la probabilité qu'il n'y ait pas d'avalanche sur un parcours où le skieur emprunterait successivement les pistes A, B et C est :
(1-p(a)) * (1-p(b)) * (1-p(c))

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

N = int(input())
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