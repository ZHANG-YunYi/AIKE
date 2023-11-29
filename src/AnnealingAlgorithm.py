import numpy as np
import matplotlib.pyplot as plt
import math
from tqdm import tqdm


def calculate_total_length(city_data, path):
    total_length = 0
    for i in range(len(path) - 1):
        x1 = city_data[path[i]][0]
        y1 = city_data[path[i]][1]
        x2 = city_data[path[i+1]][0]
        y2 = city_data[path[i+1]][1]
        total_length += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return total_length


def generate_new_path(current_path):
    new_path = current_path[:]  # 复制当前路径
    # 在当前路径中随机选择两个城市，交换它们的位置
    i = np.random.randint(len(new_path))
    j = np.random.randint(len(new_path))
    new_path[i], new_path[j] = new_path[j], new_path[i]
    return new_path


def run_Anneal(city_data):
    # 定义TSP问题的距离矩阵
    # distances = np.array([[0, 2, 9, 10],
    #                       [1, 0, 6, 4],
    #                       [15, 7, 0, 8],
    #                       [6, 3, 12, 0]])

    # 初始化当前解（初始路径）
    current_path = [i for i in range(0, city_data.shape[0])]
    np.random.shuffle(current_path)
    current_length = calculate_total_length(city_data, current_path)
    best_path = current_path
    best_length = current_length

    # 设置模拟退火算法的参数
    T = 100.0  # 初始温度
    T_min = 0.00001  # 温度下限，当T小于此值时，停止迭代
    alpha = 0.99  # 温度衰减系数，用于控制温度下降的速度
    k = 10000  # 迭代次数
    new_length_list = []
    iter_list = []
    # 开始模拟退火算法的迭代过程
    for i in range(k):
        # 生成新的解（新的路径）
        new_path = generate_new_path(current_path)
        new_length = calculate_total_length(city_data, new_path)
        new_length_list.append(new_length)
        iter_list.append(i)
        # 计算当前解与新解的差异（即目标函数的变化量）
        delta = new_length - current_length

        # 如果新解比当前解更优，则更新当前解和最优解
        if delta < 0 or np.random.rand() < np.exp(-delta / T):
            current_path = new_path
            current_length = new_length
            if current_length < best_length:
                best_path = current_path
                best_length = current_length

                # 降低温度
        T *= alpha
        if T < T_min:
            break

            # 输出最优解和对应的路径长度
    # print("最优路径：", best_path)
    # print("路径长度：", best_length)
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(1,1,1)
    ax2.plot(iter_list, new_length_list)
    ax2.set_xlabel('iteration')
    ax2.set_ylabel('The length of current path')
    ax2.set_title('The curve of Annealing iteration')
    return best_path, best_length


if __name__ == '__main__':
    pass
