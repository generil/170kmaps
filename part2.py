import imageio
import math
import numpy as np
from random import randint


def initialize():
    array = imageio.imread('kmimg1.png')
    dataset = []
    cluster = []

    for item in array:
        for i in item:
            dataset.append(list(i))

    i = 0
    while i < get_k():
        index = randint(0, len(dataset))
        cluster.append(dataset[index])
        i += 1

    return dataset, cluster


def get_k():
    return 16


def assign_cluster(dataset, cluster):
    assigned = []
    compressed = []

    i = 0
    while i < get_k():
        assigned.append([])
        i += 1

    for item in dataset:
        ass = nearest_color(item, cluster)
        compressed.append(ass)
        index = cluster.index(ass)
        assigned[index].append(item)

    return assigned, compressed


def distance(color1, color2):
    return math.sqrt(sum([(e1 - e2)**2 for e1, e2 in zip(color1, color2)]))


def nearest_color(sample, colors):
    by_distance = sorted(colors, key=lambda c: distance(c, sample))
    return by_distance[0]


def change_clusters(assigned):
    new_cluster = []
    for item in assigned:
        i = 0
        sum0, sum1, sum2 = 0, 0, 0
        while i < len(item):
            sum0 += item[i][0]
            sum1 += item[i][1]
            sum2 += item[i][2]
            i += 1
        ave0 = int(round(sum0 / len(item)))
        ave1 = int(round(sum1 / len(item)))
        ave2 = int(round(sum2 / len(item)))
        new_cluster.append([ave0, ave1, ave2])

    return new_cluster


def generate_image(dataset):
    tmp_array = []
    i = 1
    tmp = []
    for item in dataset:
        if i % 128 != 0:
            tmp.append(item)
            i += 1
        else:
            tmp.append(item)
            tmp_array.append(tmp)
            tmp = []
            i = 1

    imgarray = np.array(tmp_array)
    imageio.imwrite('compressed.png', imgarray, 'PNG-PIL')


def main():
    data = initialize()
    d, c = data
    q = []
    i = 0
    while i < 10:
        a, q = assign_cluster(d, c)
        c = change_clusters(a)
        i += 1
    generate_image(q)


if __name__ == '__main__':
    main()
