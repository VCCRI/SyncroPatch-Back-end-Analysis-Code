

import multiprocessing
import itertools
import time

def work2(array, length):
    print(array)
    print(length)
    return


def work1(array, length):
    print(array)
    print(length)
    return


def process2():
    print('process2')
    pool = multiprocessing.Pool(25)
    pool.starmap(work2, zip(itertools.repeat(range(20, 46)), itertools.repeat(25)))

    pool.close()
    pool.join()

def process1():
    print('process1')
    pool = multiprocessing.Pool(20)
    pool.starmap(work1, zip(itertools.repeat(range(20)), itertools.repeat(20)))

    pool.close()
    pool.join()



def main():
    process1()
    process2()

if __name__ == '__main__':
    main()