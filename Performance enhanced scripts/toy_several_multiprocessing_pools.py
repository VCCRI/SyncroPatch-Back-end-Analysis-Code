

import multiprocessing
import itertools
import time

def work2(array, length):
    for i in range(0, length):
        print(array[i])
        time.sleep(2)
    return


def work1(array, length):
    for i in range(0, length):
        print(array[i])
        time.sleep(2)
    return


def process2():
    print('process2')
    pool = multiprocessing.Pool(25)

    data = []
    for i in range(0, 25):
        data.append(range(20, 46))

    pool.starmap(work2, zip(data, itertools.repeat(25)))

    pool.close()
    pool.join()

def process1():
    print('process1')

    data = []
    for i in range(0, 20):
        data.append(range(20))

    pool = multiprocessing.Pool(20)
    pool.starmap(work1, zip(data, itertools.repeat(20)))

    pool.close()
    pool.join()



def main():
    process1()
    process2()

if __name__ == '__main__':
    main()