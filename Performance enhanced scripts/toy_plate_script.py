



import numpy as np
from scipy import optimize
import time
import random
import warnings
import statistics as s_tats
import matplotlib.pyplot as plt


def straight_line(x, m, b):
    y = x*m+b
    return y


def work(time, data):
    warnings.filterwarnings('ignore')
    #params = optimize.curve_fit(double_exponential, time, data, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')
    try:
        params, cov = optimize.curve_fit(double_exponential, time, data, method='trf') #BAD!!
    except:
        return np.nan
    #params, cov = optimize.curve_fit(double_exponential, time, data,  maxfev=50000) #1.88 seconds, 1.671149492263794
    #print(len(params))
    model = double_exponential(time, params[0], params[1], params[2], params[3], params[4])
    rsquare = 1 - sum((data - model) ** 2) / sum((data - s_tats.mean(data)) ** 2)
    '''
    plt.figure()
    plt.plot(time, data)
    plt.plot(time, model)
    '''
    plt.show()

    return rsquare


def double_exponential(x, A, B, C, tau1, tau2):
    return A * np.exp(-x / tau1) + B * np.exp(-x / tau2) + C


def toy_plate_script(num_rows, num_cols, well_widgets):
    tic = time.time()

    data = []
    time_secs = []


    for row in range(0, num_rows):
        for col in range(0, num_cols):
            #y_data = np.linspace(0, 10000, 10000)
            x_data = np.linspace(0, 1000, 10000)
            y_data = double_exponential(x_data, -500, -1000, -20, 20, 300)
            y_data = np.add(y_data, np.random.randint(1, 10, 10000))

            data.append(y_data)
            time_secs.append(x_data)

    print(len(time_secs))
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(max_workers=20) as executor:
        # with multiprocessing.pool.ThreadPool(20) as pool:
        # call a function on each item in a list and process results
        results = []
        for result in executor.map(work, time_secs, data):
            #print(result)
            results.append(result)


    print(results)
    print(time.time()-tic)

def main():
    toy_plate_script(16, 24)

if __name__ == '__main__':
    main()



