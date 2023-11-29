import math
import heapq

def distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def total_distance(points):
    return sum([distance(point, points[index + 1]) for index, point in enumerate(points[:-1])]) + distance(points[-1], points[0])

def run_AStar(points, start=None):
    if start is None:
        start = points[0]
    must_visit = points
    heap = [(0, [start], must_visit)]
    while heap:
        (cost, path, remaining) = heapq.heappop(heap)
        if not remaining:
            return path
        for point in remaining:
            if point not in path:
                new_path = path + [point]
                new_remaining = list(set(remaining) - set(new_path))
                new_cost = total_distance(new_path)
                heapq.heappush(heap, (new_cost, new_path, new_remaining))
