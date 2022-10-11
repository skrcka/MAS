import os
import pprint
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

def create_list_from_file(filepath):
    paths = {}
    with open(filepath) as f:
        for line in f:
            n1, n2 = line.strip().split(';')
            n1 = int(n1)
            n2 = int(n2)
            if not paths.get(n1):
                paths[n1] = []
            if not paths.get(n2):
                paths[n2] = []
            paths[n1].append(n2)
            paths[n2].append(n1)
        for key in paths:
            paths[key] = set(paths[key])
    return paths

def printlist(paths):
    for key in paths:
        print(f'{key}: ', end='')
        print(paths[key])

def create_mat_from_file(filepath):
    mat = {}
    with open(filepath) as f:
        n1s = []
        n2s = []
        for line in f:
            n1, n2 = line.strip().split(';')
            n1s.append(int(n1))
            n2s.append(int(n2))
        nset = set(n1s + n2s)
        for n in nset:
            mat[n] = {}
            for m in nset:
                mat[n][m] = 0 if n == m else math.inf
        for i in range(len(n1s)):
            n1 = n1s[i]
            n2 = n2s[i]
            mat[n1][n2] = 1
            mat[n2][n1] = 1
    return mat

def printmat(mat):
    print('   ', end='')
    for key in mat:
        print(key, end=' ')
    print()
    
    for key in mat:
        print(f'{key}:', end=' ')
        for key2 in mat[key]:
            print(mat[key][key2], end=' ')
        print()

def get_min_stupen(mat):
    min_stupen = 1_000_000_000
    min_stupen_node = -1
    for key in mat:
        stupen = 0
        for key2 in mat[key]:
            stupen += mat[key][key2]
        if stupen < min_stupen:
            min_stupen = stupen
            min_stupen_node = key
    return (min_stupen_node, min_stupen)

def get_max_stupen(mat):
    max_stupen = 0
    max_stupen_node = -1
    for key in mat:
        stupen = 0
        for key2 in mat[key]:
            stupen += mat[key][key2]
        if stupen > min_stupen:
            max_stupen = stupen
            max_stupen_node = key
    return (max_stupen_node, max_stupen)

def get_average_stupen(mat):
    nodes = 0
    stupen = 0
    for key in mat:
        nodes += 1
        for key2 in mat[key]:
            stupen += mat[key][key2]
    return stupen/nodes

def get_nodes_list_with_stupen(mat):
    nodes_with_stupen = []
    for key in mat:
        stupen = 0
        for key2 in mat[key]:
            stupen += mat[key][key2]
        nodes_with_stupen.append((key, stupen))
    return nodes_with_stupen

def get_node_count_for_stupen(nodes_with_stupen):
    node_count_for_stupen = {}
    for node, stupen in nodes_with_stupen:
        if not node_count_for_stupen.get(stupen):
            node_count_for_stupen[stupen] = 0
        node_count_for_stupen[stupen] += 1
    return node_count_for_stupen

def nodes_with_stupen_to_arr(node_count_for_stupen):
    arr = []
    for node in node_count_for_stupen:
        for _ in range(node_count_for_stupen[node]):
            arr.append(node)
    return arr

def output_node_count_per_stupen_tocsv(node_count_for_stupen):
    with open('./output.csv', 'w+') as f:
        for key in node_count_for_stupen:
            for i in range(node_count_for_stupen[key]):
                f.write(f'{key}\n')

def show_barplot(df, x, y):
    sns.barplot(df, x=df[x], y=df[y])
    plt.show()

def show_histplot(df, avg_degree, x="degrees", bins=19):
    sns.histplot(data=df, x=x, bins=bins)
    plt.axvline(avg_degree, color="red")
    plt.text(avg_degree, 10, f'Average degree: {avg_degree}', rotation=0)
    plt.show()

if __name__ == '__main__':
    filepath = './KarateClub.csv'
    mat = create_mat_from_file(filepath)
    printmat(mat)
    min_stupen_node, min_stupen = get_min_stupen(mat)
    print(f'min_stupen_node: {min_stupen_node}, stupen: {min_stupen}')
    max_stupen_node, max_stupen = get_max_stupen(mat)
    print(f'max_stupen_node: {max_stupen_node}, stupen: {max_stupen}')
    avg_stupen = get_average_stupen(mat)
    print(f'avg_stupen: {avg_stupen}')
    nodes_with_stupen = get_nodes_list_with_stupen(mat)
    node_count_for_stupen = get_node_count_for_stupen(nodes_with_stupen)
    print(node_count_for_stupen)
    for key in node_count_for_stupen:
       print(f'{key}: {node_count_for_stupen[key]}')
    output_node_count_per_stupen_tocsv(node_count_for_stupen)

    #df = pd.DataFrame(node_count_for_stupen, index=[0]).transpose().reset_index()
    #df.columns = ['node', 'pocet']

    paths = create_list_from_file(filepath)
    printlist(paths)
    
    #show_barplot(df, 'node', 'pocet')
    print(node_count_for_stupen)
    arr = nodes_with_stupen_to_arr(node_count_for_stupen)
    print(arr)
    df = pd.DataFrame(arr, columns=["degrees"])
    show_histplot(df, avg_stupen)
