import math
from pprint import pprint

from first_lecture import printmat


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

def get_paths(mat):
    for k in mat:
        for i in mat:
            for j in mat:
                if mat[i][j] > mat[i][k] + mat[k][j]:
                    mat[i][j] = mat[i][k] + mat[k][j]

def get_suma(dic):
    suma = 0
    for j in mat:
        suma += dic[j]
    return suma

def get_average(mat):
    m = 0
    for i in mat:
        for j in mat:
            if m < mat[i][j]:
                m = mat[i][j]
    return m

def get_mean_average_distance(mat):
    n = len(mat)
    suma = 0
    for i in mat:
        suma += get_suma(mat[i])
    return suma / (n**2 - n)

#(n/suma(délek všech nejkratších cest z vrcholu i do všech dostupných)).
def get_closenest(mat):
    closenest = {}
    n = len(mat)
    for i in mat:
        suma = get_suma(mat[i])
        closenest[i] = n / suma
    return closenest

if __name__ == '__main__':
    filepath = './KarateClub.csv'
    mat = create_mat_from_file(filepath)
    #printmat(mat)
    get_paths(mat)
    printmat(mat)
    mean_average_distance = get_mean_average_distance(mat)
    print(f'mean average distances: {mean_average_distance}')
    average = get_average(mat)
    print(f'average: {average}')
    closenest = get_closenest(mat)
    print('closenest:')
    pprint(closenest)
