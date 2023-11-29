import math
import heapq
import time
def distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def total_distance(points):
    return sum([distance(point, points[index + 1]) for index, point in enumerate(points[:-1])]) + distance(points[-1], points[0])


def run_AStar(points, start=None):
    print('Start to run A* and the procedure will be killed if it does not finish in 60s...')
    iter = 1
    if start is None:
        start = points[0]
    must_visit = points
    heap = [(0, [start], must_visit)]
    start = time.time()
    while heap:
        # print('---------------------------')
        # print('iter', iter)
        # print('the length of open list:', len(heap))
        now = time.time()
        if now-start > 60*1:
            break
        (cost, path, remaining) = heapq.heappop(heap)
        if not remaining:
            print('the length of open list:', len(heap))
            return path, total_distance(path)
        for point in remaining:
            if point not in path:
                new_path = path + [point]
                new_remaining = list(set(remaining) - set(new_path))
                new_cost = total_distance(new_path)
                heapq.heappush(heap, (new_cost, new_path, new_remaining))
        iter += 1
    print('failed to get path by A* in 60s')
    print('the length of open list:', len(heap))
    return [], None