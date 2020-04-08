from matrix import Matrix

if __name__ == '__main__':
    a = Matrix(3)
    for i in range(0, a.dim):
        for j in range(0, a.dim):
            a[i, j] = j + i*3
    a[0, 0] = 7

    print(a)
    print(a.transpose())
    b = a.inverse()
    print(b)
    print((a @ b) * 2)
