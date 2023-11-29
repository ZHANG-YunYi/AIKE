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
    if path == []:
        nx.draw(city_graph, pos=pos, with_labels=True)
        return
    for k in range(0, len(path) - 1):
        city_graph.add_edge(path[k], path[k + 1])
    city_graph.add_edge(path[-1], path[0])
    nx.draw(city_graph, pos=pos, with_labels=True)
    return
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
    path_Astar = []
    path_GA = []
    path_Anne = []
    print('======================================')
    print('          begin calculating           ')
    print('======================================')
    start = time.time()
    point_path, total_distance_Astar = AStarAlgorithm.run_AStar(points)
    for point in point_path:
        for key, value in pos.items():
            if point == tuple(value):
                path_Astar.append(key)
    time_cost = time.time() - start
    print('path calculated by AStar:', path_Astar)
    print('total distance :', total_distance_Astar)
    print('runtime of AStar:', time_cost)
    print('======================================')
    start = time.time()
    path_GA, total_distance_GA = GeneticAlgorithm.run_GA(city_data)
    print('path calculated by GA:', path_GA)
    print('total distance :', total_distance_GA)
    time_cost = time.time() - start
    print('runtime of GA:', time_cost)
    print('======================================')
    start = time.time()
    path_Anne, total_distance_Anne = AnnealingAlgorithm.run_Anneal(city_data)
    time_cost = time.time() - start
    print('path calculated by Anneal:', path_Anne)
    print('total distance:', total_distance_Anne)
    print('runtime of Annealing:', time_cost)

    # 画图
    fig3 = plt.figure(figsize=(10,4))
    plt.title('result of A*')
    draw_path(city_data, path_Astar)
    fig4 = plt.figure(figsize=(10, 4))
    # plt.subplot(1,3,2)
    plt.title('result of GA')
    draw_path(city_data, path_GA)
    # plt.subplot(1,3,3)
    fig5 = plt.figure(figsize=(10, 4))
    plt.title('result of Annealing')
    draw_path(city_data, path_Anne)
    plt.show()