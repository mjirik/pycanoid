__author__ = 'Patrik'

import numpy as np

if __name__ == '__main__':
    matrix = np.random.randint(2, size=(10,10))
    np.save('blockmap', matrix)
    n = np.load('blockmap.npy')
    print n

    #for r in range(matrix.shape[0]):
    #    for s in range(matrix.shape[1]):
    #        x = matrix[r,s]