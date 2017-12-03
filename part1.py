import math


def initialize():
    dataset_from_file = [line.rstrip('\r\n')[1:].split()
                         for line in open('kmdata1.txt', 'r')]
    k = len(clusters)
    for data in dataset_from_file:
        tmp_list = []
        for item in data:
            tmp = float(item)
            tmp_list.append(tmp)
        dataset.append(tmp_list)


def assign_cluster(cluster, dataset):
    m1_data = []
    m2_data = []
    m3_data = []
    j_clusters = []
    cafname = "iter{}_ca.txt".format(iterate + 1)
    ca_file = open(cafname, 'w')

    for data in dataset:
        d1 = data[0]
        d2 = data[1]
        c1x = cluster[0][0]
        c1y = cluster[0][1]
        c2x = cluster[1][0]
        c2y = cluster[1][1]
        c3x = cluster[2][0]
        c3y = cluster[2][1]

        m1 = math.sqrt(((d1 - c1x) ** 2) + ((d2 - c1y) ** 2))
        m2 = math.sqrt(((d1 - c2x) ** 2) + ((d2 - c2y) ** 2))
        m3 = math.sqrt(((d1 - c3x) ** 2) + ((d2 - c3y) ** 2))
        tmp = [m1, m2, m3]
        assigned = min(m1, m2, m3)
        ca_file.write(str(assigned) + "\n")
        j_clusters.append(tmp[assigned - 1])
        tmp = [d1, d2]
        if assigned == 1:
            m1_data.append(tmp)
        elif assigned == 2:
            m2_data.append(tmp)
        elif assigned == 3:
            m3_data.append(tmp)

    ca_file.close()
    return m1_data, m2_data, m3_data, j_clusters


def move_centroid(m1_data, m2_data, m3_data):
    cmfname = "iter{}_cm.txt".format(iterate + 1)
    cm_file = open(cmfname, 'w')
    m1x = total(m1_data, 0) / len(m1_data)
    m1y = total(m1_data, 1) / len(m1_data)
    m2x = total(m2_data, 0) / len(m2_data)
    m2y = total(m2_data, 1) / len(m2_data)
    m3x = total(m3_data, 0) / len(m3_data)
    m3y = total(m3_data, 1) / len(m3_data)
    cm_file.write("{:0.6f} {:0.6f}\n".format(m1x, m1y))
    cm_file.write("{:0.6f} {:0.6f}\n".format(m2x, m2y))
    cm_file.write("{:0.6f} {:0.6f}\n".format(m3x, m3y))
    cm_file.close()
    return [[m1x, m1y], [m2x, m2y], [m3x, m3y]]


def compute_j(j_clusters):
    return sum(j_clusters) / len(j_clusters)


def total(data, pos):
    sum = 0
    for item in data:
        sum += item[pos]
    return sum


def min(m1, m2, m3):
    small = 3
    if m1 < m2 and m1 < m3:
        small = 1
    elif m2 < m3:
        small = 2

    return small


def main():
    global iterate, clusters, dataset
    iterate = 0
    clusters = [[3, 3], [6, 2], [8, 5]]
    dataset = []
    cost_j = 0
    initialize()

    prev_j = 0
    tmp_c = clusters
    while iterate < 10:
        print(tmp_c)
        m1, m2, m3, jc = assign_cluster(tmp_c, dataset)
        tmp_c = move_centroid(m1, m2, m3)
        cm_file = open("iter{}_cm.txt".format(iterate + 1), 'a')
        cost_j = compute_j(jc)
        diff_j = cost_j - prev_j
        cm_file.write('J = {:0.6f}\n'.format(cost_j))
        cm_file.write('dJ = {:0.6f}\n'.format(diff_j))
        cm_file.close()
        prev_j = cost_j
        iterate += 1


if __name__ == "__main__":
    main()
