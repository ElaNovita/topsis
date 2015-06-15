from math import sqrt

# bobot  C1 C2 C3 C4 C5
w = [5, 3, 4, 4, 2]

D = [  # matriks alternatif dg solusi
    [0.75, 2000, 18, 50, 500],
    [0.5, 1500, 20, 40, 450],
    [0.9, 2050, 35, 35, 800]
]

rules = [0, 1, 0, 1, 0]  # 0/1 => kriteria cost/benefit kriteria


def find_r(matriks_D, n):  # mencari nilai r pd saat mentarnsform ke matriks R
    total = 0
    for i in range(len(matriks_D)):
        total += (matriks_D[i][n] ** 2)
    return sqrt(total)


def transform_to_r(matriks_D):  # transformasikan matriks D ke matriks R
    R = []
    for i in range(len(matriks_D)):
        r_list = []
        for j in range(len(matriks_D[i])):
            r = matriks_D[i][j] / find_r(matriks_D, j)
            r_list.append(r)
        R.append(r_list)
    return R


def transform_to_v(matriks_R, w):
    Y = []
    for i in range(len(matriks_R)):
        y_list = []
        for j in range(len(matriks_R[i])):
            y = matriks_R[i][j] * w[j]
            y_list.append(y)
        Y.append(y_list)
    return Y


def A(matriks_V, rules):  # solusi ideal positif/negatif
    data = {
        'positive': [],
        'negative': []
    }

    zipped = zip(*matriks_V)
    for i in range(len(matriks_V[0])):
        if rules[i] == 1:
            data['positive'].append(min(zipped[i]))
            data['negative'].append(max(zipped[i]))
        else:
            data['positive'].append(max(zipped[i]))
            data['negative'].append(min(zipped[i]))

    return data


def S(matriks_V, A):  # jarak terhadap solusi negatif/positif
    data = {
        'positive': [],
        'negative': []
    }

    for i in range(len(matriks_V)):
        p_total = 0
        n_total = 0

        for j in range(len(matriks_V[i])):
            p_total += (matriks_V[i][j] - A['positive'][j]) ** 2
            n_total += (matriks_V[i][j] - A['negative'][j]) ** 2

        data['positive'].append(sqrt(p_total))
        data['negative'].append(sqrt(n_total))

    return data


def C(S):
    data = []
    for i in range(len(S['positive'])):
        d = S['negative'][i] / (S['positive'][i] + S['negative'][i])
        data.append(d)
    return data


def best_alternatives(matriks_D, w, rules):
    matriks_R = transform_to_r(matriks_D)
    matriks_V = transform_to_v(matriks_R, w)
    solusi_A = A(matriks_V, rules)
    jarak = S(matriks_V, solusi_A)
    cs = C(jarak)

    return cs


alternatif = best_alternatives(D, w, rules)
print alternatif
print

best_of_all = sorted(alternatif, reverse=True)
for i in best_of_all:
    print "Alternatif %s: dengan nilai %s" % (alternatif.index(i) + 1, i)
