import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time
import GeneticAlgorithm
import AStarAlgorithm
import AnnealingAlgorithm


def read_city_data(file_path):
    data = np.loadtxt(file_path, dtype=np.float32)
    data = np.array(data)
    return data


def draw_path(city_data, path):
    # 每次画图之前先把图初始化
    city_num = city_data.shape[0]
    city_graph = nx.DiGraph()
    pos = {}
    for i in range(0, city_data.shape[0]):
        # 用一部字典存储各个城市的位置
        pos[i] = city_data[i]
        # 这里加上节点的序号和坐标属性，访问属性用nx.get_node_attributes(city_graph, 'position')
        city_graph.add_node(i, idx=i, position=city_data[i])
    k = 0
    for k in range(0, len(path) - 1):
        city_graph.add_edge(path[k], path[k + 1])
    city_graph.add_edge(path[-1], path[0])
    nx.draw(city_graph, pos=pos, with_labels=True)
    # plt.show()


if __name__ == '__main__':
    city_data = read_city_data('../data/CityData10.txt')
    city_num = city_data.shape[0]
    city_graph = nx.DiGraph()
    pos = {}
    for i in range(0, city_data.shape[0]):
        pos[i] = city_data[i]
    points = []
    for k in range(0, city_num):
        points.append((city_data[k][0], city_data[k][1]))
    path = []

    print('======================================')
    print('          begin calculating           ')
    print('======================================')
    start = time.time()
    point_path = AStarAlgorithm.run_AStar(points)
    for point in point_path:
        for key, value in pos.items():
            if point == tuple(value):
                path.append(key)
    time_cost = time.time() - start
    print('path calculated by AStar:\n', path)
    print('runtime of AStar:', time_cost)
    start = time.time()
    fig1 = plt.figure(figsize=(5, 4))
    plt.title('Result of A*')
    draw_path(city_data, path)
    print('======================================')
    start = time.time()
    path = GeneticAlgorithm.run_GA(city_data)
    print('path calculated by GA:\n', path)
    time_cost = time.time() - start
    print('runtime of GA:', time_cost)
    fig2 = plt.figure(figsize=(5, 4))
    plt.title('Result of Genetic')
    draw_path(city_data, path)
    # plt.show()
    print('======================================')
    start = time.time()
    path = AnnealingAlgorithm.run_Anneal(city_data)
    time_cost = time.time() - start
    print('path calculated by Anneal:\n', path)
    fig3 = plt.figure(figsize=(5, 4))
    plt.title('Result of Annealing')
    draw_path(city_data, path)
    print('runtime of Annealing:', time_cost)
    plt.show()