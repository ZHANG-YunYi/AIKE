import numpy as np
import sys
import time
from tqdm import tqdm
class GA:

    def __init__(self, citys, maxgen=500,
                 size_pop=200, cross_rate=0.8,
                 muta_rate=0.005
                 ):
        self.maxgen = maxgen  # 最大进化次数
        self.size_pop = size_pop  # 种群大小（染色体个数）
        self.cross_rate = cross_rate  # 交叉概率
        self.muta_rate = muta_rate  # 变异概率
        self.citys = citys  # 城市的坐标数据
        self.num = citys.shape[0]  # 城市的个数(染色体长度)

    # 获得距离矩阵
    def matrix_distance(self):
        self.distance_m = np.zeros((self.num, self.num))
        for i in range(self.num):
            for j in range(self.num):
                self.distance_m[i][j] = np.sqrt(
                    (self.citys[i][0] - self.citys[j][0]) ** 2 + (self.citys[i][1] - self.citys[j][1]) ** 2)

    # 计算某条路径的距离
    def get_total_distance(self, one_path):
        distance = 0
        for i in range(self.num - 1):
            distance += self.distance_m[one_path[i]][one_path[i + 1]]
        distance += self.distance_m[one_path[-1]][one_path[0]]
        return distance

    # 初始化种群
    def generate_population(self):
        path = np.array(range(self.num))
        self.pop = []
        for i in range(self.size_pop):
            x = path.copy()
            np.random.shuffle(x)  # 随机洗牌
            self.pop.append(x)

    # 交叉互换
    def crossover(self):
        self.new_pop = []
        for father in self.pop:
            child = father  # 初步让子代获得父本染色体
            if np.random.rand() < self.cross_rate:
                # 随机选择一个染色体作为母本
                mother_index = np.random.randint(0, self.size_pop)
                mother = self.pop[mother_index]
                # 确定切割点
                left = np.random.randint(0, self.num - 2)
                right = np.random.randint(left + 1, self.num - 1)
                mother = mother.tolist()
                father = father.tolist()
                # 切割片段
                gene = mother[left:right]
                child1_c = father[right:] + father[:right]
                child1 = child1_c.copy()
                # 去除重复基因
                for o in gene:
                    child1_c.remove(o)
                child1[left:right] = gene
                child1[right:] = child1_c[0:len(child1) - right]
                child1[:left] = child1_c[(len(child1) - right):]
                child = np.array(child1)

            self.new_pop.append(child)
        self.pop = self.new_pop

    # 变异
    def mutation(self):
        for i in range(self.size_pop):
            if np.random.rand() < self.muta_rate:
                child = self.pop[i]
                u = np.random.randint(0, self.num - 2)
                v = np.random.randint(u + 1, self.num - 1)
                child_x = child[u + 1:v]
                child_x = child_x[::-1]
                child = np.concatenate((child[0:u + 1], child_x, child[v:]))
                self.pop[i] = child

    # 自然选择，种群根据适应度进行更新
    def select(self):
        # 计算每条路径的长度，放入列表
        self.dis = []
        for i in range(self.size_pop):
            self.dis.append(self.get_total_distance(one_path=self.pop[i]))
        # 根据路径长度计算每个个体的适应度
        self.fitness = []
        for i in range(self.size_pop):
            self.fitness.append(1 / (self.dis[i] ** 15))
        # 适应度总和
        fitness_sum = 0
        for i in range(self.size_pop):
            fitness_sum += self.fitness[i]
        # 根据适应度进行选择，适应度大的被选择概率大
        idx = np.random.choice(np.arange(self.size_pop), size=self.size_pop, replace=True,
                               p=(self.fitness) / (fitness_sum))
        self.new_pop = []
        for i in idx:
            self.new_pop.append(self.pop[i])
        self.pop = self.new_pop

    # 输出当前种群中最优路径
    def result_path(self):
        idx_path=[]
        self.index = np.argmax(self.fitness)
        a = "the shortest path is:"
        for i in range(self.num - 1):
            a += str(self.pop[self.index][i])
            a += "-->"
            idx_path.append(self.pop[self.index][i])
        a += str(self.pop[self.index][-1])
        idx_path.append(self.pop[self.index][-1])
        # print(a)
        # print("the total distance is", self.dis[self.index])
        return idx_path

# 主函数进行迭代
def run_GA(citys):
    SL = GA(citys)
    SL.matrix_distance()
    SL.generate_population()
    print('Iteration progress of Genetic algorithm...')
    for i in tqdm(range(SL.maxgen)):
        SL.crossover()
        SL.mutation()
        SL.select()
    path=SL.result_path()
    return path

# if __name__ == '__main__':
#     citys = np.array([[16.47, 96.10], [16.47, 94.44], [20.09, 92.54],
#                       [22.39, 93.37], [25.23, 97.24], [22.00, 96.05], [20.47, 97.02],
#                       [17.20, 96.29], [16.30, 97.38], [14.05, 98.12], [16.53, 97.38],
#                       [21.52, 95.59], [19.41, 97.13], [20.09, 92.55]])
#     main(citys)