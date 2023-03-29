



import numpy as np
from scipy import optimize


def straight_line(x, m, b):
    y = x*m+b
    print(y)
    return y


def work(time, data):
    params = optimize.curve_fit(straight_line, time, data)
    return 1


def toy_plate_script(num_rows, num_cols):
    data = []
    time_secs = []


    for row in range(0, num_rows):
        for col in range(0, num_cols):
            y_data = np.arange(0, 10000, 10000)

            x_data = np.arange(0, 10000, 10000)
            data.append(y_data)
            time_secs.append(x_data)

    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(max_workers=20) as executor:
        # with multiprocessing.pool.ThreadPool(20) as pool:
        # call a function on each item in a list and process results
        for result in executor.map(work, time_secs, data):
            print(result)

def main():
    toy_plate_script(16, 24)

if __name__ == '__main__':
    main()



