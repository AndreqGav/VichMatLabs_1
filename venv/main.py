import math
import pylab
from matplotlib import mlab
import numpy as np

xmin = 0 #левая граница отрезка
xmax = 1 #правая граница отрезка
n = 1 #степень многочлена

dx = 0.1 #частота разбиения графика(точность)

# сама функция
def func(x):
    if x == 0:
        return 1.0
    return math.cos(x) * x**.5

# чтение данных из файла, успешно -> True, иначе -> False
def GetData(filepath)->bool:

    global xmin
    global  xmax
    global  n

    with open(filepath, 'r') as f:
        nums = f.read().splitlines()

        if len(nums) == 3:
            xmin = int(nums[0])
            xmax = int(nums[1])
            n = int(nums[2])
        else:
            return False
        return  True

# (X-X_0)*(X-X_1)*...*(X-X_n)
def Product(x, k, grid):
    mul = 1
    for i in range(k):
        if i: mul *= x - grid[i - 1]
        yield mul

# Нахождение разделенной разности
def SplitDifference(grid)->[]:
    C = []  # разделенная разность
    for k in range(len(grid)):
        p = Product(grid[k], k + 1, grid)
        C.append((func(grid[k]) - sum(C[i] * next(p) for i in range(k))) / next(p))
    return  C

# Значение многочлена в точке x
def PolynomialValue(x, grid):
    C = SplitDifference(grid)
    return sum(C[k] * p for k, p in enumerate(Product(x, len(C),grid)))

def ChebyshevNode(x,i)->float:
    return  (xmin + xmax)/2 + (xmax - xmin)*(math.cos((2*i+1)*math.pi/(2*n+2)))/2

def GetChebyshevGrid(grid)->[]:
    ChebyshevGrid = []
    for i in range(len(grid)):
        ChebyshevGrid.append(ChebyshevNode(grid[i],i))
    return  ChebyshevGrid

def main():
    global  dx

    result = GetData('input.txt')
    if result == False:
        return -1

    # мн-во точек построения для графика
    xlist = list(np.arange(xmin, xmax, dx))
    # график самой функции
    pylab.plot(xlist, [func(x) for x in xlist])

    # равномерная сетка
    uniformGrid = list(np.arange(xmin, xmax, float((xmin + xmax)/n)))
    # график многочлена по равномерной сетке
    pylab.plot(xlist,list(PolynomialValue(x,uniformGrid) for x in xlist))

    # Чебышевская сетка
    ChebyshevGrid = GetChebyshevGrid(uniformGrid)
    # график многочлена по Чебышевской сетке
    pylab.plot(xlist, list(PolynomialValue(x, ChebyshevGrid) for x in xlist))

    pylab.xlim(xmin, xmax)
    pylab.ylim(-3.8,3.5)

    pylab.show()

if __name__ == '__main__':
    main()