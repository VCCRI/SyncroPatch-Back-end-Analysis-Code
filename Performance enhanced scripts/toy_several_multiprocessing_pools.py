

import multiprocessing
import itertools

def work2(array, length):
    for i in range(0, length+1):
        print(array[i])
        
    return


def work1(array, length):
    for i in range(0, length+1):
        print(array[i])
    return


def process2():
    pool = multiprocessing.Pool(25)
    pool.starmap(work2, zip(range(20, 46), itertools.repeat(25)))

    pool.close()
    pool.join()

def process1():
    pool = multiprocessing.Pool(20)
    pool.starmap(work1, zip(range(20), itertools.repeat(20)))

    pool.close()
    pool.join()



def main():
    process1()
    process2()

if __name__ == '__main__':
    main()