import csv
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import os
import statistics as s_tats
import time
from scipy.special import expit
import warnings
import pickle
import math
import pandas as pd
from scipy.stats.distributions import t


def linear_fit(x, a, b):
    return a*x + b

def post_analysis_qc(model, data, voltage_array, warning, wellID, endo_removed):
    include_summary = 1

    model_len = np.shape(model)
    data_len = np.shape(data)
    #print(model_midpoint)
    #print(data_midpoint)

    if model_len[0] % 2 == 0:
        model_midpoint = model_len[0] / 2
        data_midpoint = data_len[0] / 2
    else:
        model_midpoint = np.floor(model_len[0] / 2)
        data_midpoint = np.floor(data_len[0] / 2)

    discrepancy = 0.1*data[int(data_midpoint)]
    #if model[int(model_midpoint)] != data[int(data_midpoint)]:
    warning_addition = 0
    if not (discrepancy+data[int(data_midpoint)]) >= model[int(model_midpoint)] >= (data[int(data_midpoint)]-discrepancy):
        warning_addition = 0
        include_summary = 0
        if warning:
            warning = warning + ' and model midpoint varies too far from the data'
        else:
            #print(wellID + ' midpoint warn')
            warning = 'model midpoint varies too far from the data'

    #if warning_addition == 0:
        # Check that plateau was reached
        '''
        if model_len[0] < 2:
            return warning_addition
        final_model_point = model[model_len[0]-1]
        seclast_model_point = model[model_len[0]-2]
        lin_y_data = np.array([seclast_model_point, final_model_point])

        final_volt_point = voltage_array[model_len[0]-1]
        seclast_volt_point = voltage_array[model_len[0]-2]
        lin_x_data = np.array([seclast_volt_point, final_volt_point])

        warnings.filterwarnings('ignore')
        params, cov = optimize.curve_fit(linear_fit, lin_x_data, lin_y_data)
        lin_model = linear_fit(lin_x_data, params[0], params[1])
        '''
        '''
        plt.figure()
        plt.plot(lin_x_data, lin_y_data)
        plt.plot(lin_x_data, lin_model)
        plt.show()
        '''
        '''
        #print(params[0])
        if not 0.0025 >= params[0] >= -0.0025:
            include_summary = 0
            if not warning:
                warning = 'plateau not reached in model prediction'
            else:
                warning += ' and plateau not reached in model prediction'
        #print(warning)
        '''
        #Check for endogenous current
    if warning_addition == 0 and model_len[0] >= 4 and endo_removed == 'no':
        final_model_point = data[model_len[0] - 1]
        seclast_model_point = data[model_len[0] - 2]
        thridlast_model_point = data[model_len[0] - 3]
        fourthlast_model_point = data[model_len[0] - 4]

        #fifthlast_model_point = model[model_len[0] - 5]
        #sixthlast_model_point = model[model_len[0] - 6]

        last_lin_y_data = np.array([seclast_model_point, final_model_point])
        seclast_lin_y_data = np.array([thridlast_model_point, seclast_model_point])
        thirdlast_lin_y_data = np.array([fourthlast_model_point, thridlast_model_point])

        final_volt_point = voltage_array[model_len[0] - 1]
        seclast_volt_point = voltage_array[model_len[0] - 2]
        thirdlast_volt_point = voltage_array[model_len[0] - 3]
        fourthlast_volt_point = voltage_array[model_len[0] - 4]

        last_lin_x_data = np.array([seclast_volt_point, final_volt_point])
        seclast_lin_x_data = np.array([thirdlast_volt_point, seclast_volt_point])
        thirdlast_lin_x_data = np.array([fourthlast_volt_point, thirdlast_volt_point])

        warnings.filterwarnings('ignore')
        last_params, cov = optimize.curve_fit(linear_fit, last_lin_x_data, last_lin_y_data)
        last_lin_model = linear_fit(last_lin_x_data, last_params[0], last_params[1])

        warnings.filterwarnings('ignore')
        seclast_params, cov = optimize.curve_fit(linear_fit, seclast_lin_x_data, seclast_lin_y_data)
        seclast_lin_model = linear_fit(seclast_lin_x_data, seclast_params[0], seclast_params[1])

        warnings.filterwarnings('ignore')
        thirdlast_params, cov = optimize.curve_fit(linear_fit, thirdlast_lin_x_data, thirdlast_lin_y_data)
        thirdlast_lin_model = linear_fit(thirdlast_lin_x_data, thirdlast_params[0], thirdlast_params[1])

        if last_params[0] > 0.006:
            if last_params[0] > seclast_params[0]:
                if 0 <= seclast_params[0] <= 0.003:
                    if seclast_params[0] < thirdlast_params[0]:
                        if thirdlast_params[0] > 0.005:
                            warning_addition = 1
                            include_summary = 2
                            #print(wellID + ' endo current')
                            #print('final slope = ' + str(last_params[0]))
                            #print('mid slope = ' + str(seclast_params[0]))
                            #print('start slop = ' + str(thirdlast_params[0]))
                            if not warning:
                                warning = 'Endogenous Current exhibited'
                            else:
                                warning += ' and Endogenous Current Exhibited'

    elif warning_addition == 0 and model_len[0] < 4:
        if model_len[0] < 2:
            return [warning, include_summary]
        final_model_point = model[model_len[0] - 1]
        seclast_model_point = model[model_len[0] - 2]
        lin_y_data = np.array([seclast_model_point, final_model_point])

        final_volt_point = voltage_array[model_len[0] - 1]
        seclast_volt_point = voltage_array[model_len[0] - 2]
        lin_x_data = np.array([seclast_volt_point, final_volt_point])

        warnings.filterwarnings('ignore')
        params, cov = optimize.curve_fit(linear_fit, lin_x_data, lin_y_data)
        lin_model = linear_fit(lin_x_data, params[0], params[1])
        '''
        plt.figure()
        plt.plot(lin_x_data, lin_y_data)
        plt.plot(lin_x_data, lin_model)
        plt.show()
        '''
        # print(params[0])
        #if wellID == 'P02' or wellID == 'L01' or wellID == 'E02':
            #print(wellID)
            #print(params[0])


        if not 0.005 >= params[0] >= 0:
            include_summary = 0
            warning_addition = 1
            #print(wellID + ' plat')
            if not warning:
                warning = 'plateau not reached in model prediction'
            else:
                warning += ' and plateau not reached in model prediction'
        # print(warning)

    if warning_addition == 0:
        if model_len[0] < 2:
            return [warning, include_summary]
        final_model_point = model[model_len[0] - 1]
        seclast_model_point = model[model_len[0] - 2]
        lin_y_data = np.array([seclast_model_point, final_model_point])

        final_volt_point = voltage_array[model_len[0] - 1]
        seclast_volt_point = voltage_array[model_len[0] - 2]
        lin_x_data = np.array([seclast_volt_point, final_volt_point])

        warnings.filterwarnings('ignore')
        params, cov = optimize.curve_fit(linear_fit, lin_x_data, lin_y_data)
        lin_model = linear_fit(lin_x_data, params[0], params[1])
        '''
        plt.figure()
        plt.plot(lin_x_data, lin_y_data)
        plt.plot(lin_x_data, lin_model)
        plt.show()
        '''
        # print(params[0])


        if not 0.005 >= params[0] >= 0:
            include_summary = 0
            warning_addition = 1
            #print(wellID + ' plat'+ str(params[0]))
            if not warning:
                warning = 'plateau not reached in model prediction'
            else:
                warning += ' and plateau not reached in model prediction'
        # print(warning)
    return [warning, include_summary]

#def boltzmann_v05(x, V05, k):
def boltzmann_v05(x, V05, k, top, bottom):
    #return 1/(1+np.exp((V05-x)/k))
    return bottom + ((top-bottom)/(1+np.exp((V05-x)/k)))
    #return expit(-((V05-x)/k))

#def boltzmann_therm(x, G0, z):
def boltzmann_therm(x, G0, z, top, bottom):
    '''
    num = G0 - (z * 96485 / 1000*x)
    dom = 8.3145 * 298
    return expit(-(num / dom))
    '''
    #Y=1/(1+exp((deltaG0-z*F/1000*X)/(R*T)))
    return bottom + ((top-bottom)/(1 + np.exp((G0 - (z * 96485 / 1000*x))/(8.3145 * 298))))

def V05_analysis(voltage_array, norm_currs, rsq_thresh, returnV05, returnK, pos40mVCD, wellID):
    fit_parameters = np.array(['V05', 'k', 'top', 'bottom', 'RSquared', 'Warning'])
    # fit_parameters = np.append(fit_parameters)

    # print(wellID)
    # print(norm_currs[0])
    # print(norm_currs[-1])

    p0 = [20, 20, 1, 0]
    try:
        #params, cov = optimize.curve_fit(boltzmann_v05, voltage_array, norm_currs, p0, maxfev=50000)
        params, cov = optimize.curve_fit(boltzmann_v05, voltage_array, norm_currs, p0, maxfev=50000, bounds=([-np.inf, -np.inf, 0, -np.inf], [np.inf, np.inf, 4, np.inf]))

    except:
        print(voltage_array)
        print(norm_currs)

    V05 = params[0]
    k = params[1]
    top = params[2]
    bottom = params[3]

    sigma_params = np.sqrt(np.diagonal(cov))
    V05_sigma = sigma_params[0]
    k_sigma = sigma_params[1]
    top_sigma = sigma_params[2]
    bottom_sigma = sigma_params[3]

    if V05_sigma == 0:
        V05_sigma = math.inf
    if k_sigma == 0:
        k_sigma = math.inf
    if top_sigma == 0:
        top_sigma = math.inf
    if bottom_sigma == 0:
        bottom_sigma = math.inf

    alpha = 0.05

    tval = t.ppf(1 - alpha / 2.0, (len(voltage_array)-len(params)))
    '''
    V05_lower_ci = V05 - (1.96 * (V05_sigma / np.sqrt(len(voltage_array))))
    V05_upper_ci = V05 + (1.96 * (V05_sigma / np.sqrt(len(voltage_array))))
    k_lower_ci = k - (1.96 * (k_sigma / np.sqrt(len(voltage_array))))
    k_upper_ci = k + (1.96 * (k_sigma / np.sqrt(len(voltage_array))))
    top_lower_ci = top - (1.96 * (top_sigma / np.sqrt(len(voltage_array))))
    top_upper_ci = top + (1.96 * (top_sigma / np.sqrt(len(voltage_array))))
    bottom_lower_ci = bottom - (1.96 * (bottom_sigma / np.sqrt(len(voltage_array))))
    bottom_upper_ci = bottom + (1.96 * (bottom_sigma / np.sqrt(len(voltage_array))))
    '''
    V05_lower_ci = V05 - (tval * (V05_sigma))
    V05_upper_ci = V05 + (tval * (V05_sigma))
    k_lower_ci = k - (tval * (k_sigma))
    k_upper_ci = k + (tval * (k_sigma))
    top_lower_ci = top - (tval * (top_sigma))
    top_upper_ci = top + (tval * (top_sigma))
    bottom_lower_ci = bottom - (tval * (bottom_sigma))
    bottom_upper_ci = bottom + (tval * (bottom_sigma))

    V05_lower_ci = "{:.5f}".format(V05_lower_ci)
    V05_upper_ci = "{:.5f}".format(V05_upper_ci)
    k_lower_ci = "{:.5f}".format(k_lower_ci)
    k_upper_ci = "{:.5f}".format(k_upper_ci)
    top_lower_ci = "{:.5f}".format(top_lower_ci)
    top_upper_ci = "{:.5f}".format(top_upper_ci)
    bottom_lower_ci = "{:.5f}".format(bottom_lower_ci)
    bottom_upper_ci = "{:.5f}".format(bottom_upper_ci)

    V05_ci = str('(' + str(V05_lower_ci) + ' ,' + str(V05_upper_ci) + ')')
    k_ci = str('(' + str(k_lower_ci) + ' ,' + str(k_upper_ci) + ')')
    top_ci = str('(' + str(top_lower_ci) + ' ,' + str(top_upper_ci) + ')')
    bottom_ci = str('(' + str(bottom_lower_ci) + ' ,' + str(bottom_upper_ci) + ')')

    # model = boltzmann_v05(voltage_array, V05, k)
    model = boltzmann_v05(voltage_array, V05, k, top, bottom)
    warning = ''
    rsquare = 1 - sum((norm_currs - model) ** 2) / sum((norm_currs - s_tats.mean(norm_currs)) ** 2)

    # Check the Rsquared of the voltage region from -50 to -30mV
    volt_list = list(voltage_array)
    lower_volt_indx = [i for i in range(len(volt_list)) if -30 >= volt_list[i] >= -50]
    lower_rsquare = 'N/A'
    if len(lower_volt_indx) >= 2:
        lower_rsquare = 1 - sum((norm_currs[lower_volt_indx] - model[lower_volt_indx]) ** 2) / sum(
            (norm_currs[lower_volt_indx] - s_tats.mean(norm_currs[lower_volt_indx])) ** 2)

    fit_params_results = np.array([V05, V05_ci, k, k_ci, top, top_ci, bottom, bottom_ci, rsquare])

    V05_ok = 1
    if rsquare < rsq_thresh:
        warning = 'Fit of Whole Data-set Poor'
        #pos40mVCD = 'N/A'
        returnV05 = 'N/A'
        returnK = 'N/A'
        if not -50 <= V05 <= 50:
            V05_ok = 0
            #pos40mVCD = 'N/A'
            warning = 'Fit of Whole Data-set Poor and V05 outside of possible range of values'

    else:
        '''
        if lower_rsquare != 'N/A':
            if lower_rsquare < 0.1:
                warning = 'Fit of region from -50mV to -30mV Poor with RSquared = ' + str(lower_rsquare)

                returnV05 = V05
                returnK = k
                if not -50 <= V05 <= 50:
                    V05_ok = 0
                    returnV05 = 'V05'
                    returnK = 'V05'
                    warning = 'Fit of region from -50mV to -30mV Poor with RSquared = ' + str(
                        lower_rsquare) + ' and V05 outside of possible range of values'
            else:
                if not -50 <= V05 <= 50:
                    V05_ok = 0
                    warning = 'V05 outside of possible range of values'
                    returnV05 = 'V05'
                    returnK = 'V05'
                    #pos40mVCD = 'N/A'
                else:
                    returnV05 = V05
                    returnK = k
        else:
        '''
        if not -50 <= V05 <= 50:
            V05_ok = 0
            warning = 'V05 outside of possible range of values'
            returnV05 = 'V05'
            returnK = 'V05'
            #pos40mVCD = 'N/A'
        else:
            returnV05 = V05
            returnK = k


    return [returnV05, returnK, model, rsquare, V05_ok, fit_params_results, warning, V05, k, top, bottom, lower_volt_indx, pos40mVCD]

def therm_analysis(V05, k, top, bottom, returnDG, returnz):
    therm_fit_parameters = np.array(['G0', 'z', 'top', 'bottom'])
    G0 = (V05 / k) * (8.3145 * 298)
    z = (1 / k) / (96485 / (1000 * 8.3145 * 298))
    therm_top = top
    therm_bottom = bottom

    therm_param_results = np.array([G0, z, therm_top, therm_bottom])

    returnDG = G0
    returnz = z
    return [returnDG, returnz, therm_param_results, G0, z, therm_top, therm_bottom]

def therm_fit_analysis(voltage_array, norm_currs, rsq_thresh, returnDG, returnz, lower_volt_indx, pos40mVCD):

    therm_fit_parameters = np.array(['G0', 'G0 95% CI', 'z', 'z 95% CI', 'top', 'top 95% CI', 'bottom', 'bottom 95% CI', 'RSquared', 'Warning'])

    #therm_p0 = [2500, 155, 1, 0]
    v_list = list(voltage_array)
    therm_v_list = [i for i in range(len(v_list)) if v_list[i] != 0]
    therm_voltage_array = voltage_array[therm_v_list]
    therm_norm_currs = norm_currs[therm_v_list]

    if np.shape(therm_norm_currs)[0] < 4:
        return [returnDG, returnz, np.array([]), therm_norm_currs, therm_voltage_array,'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', pos40mVCD]


    therm_params, therm_cov = optimize.curve_fit(boltzmann_therm, therm_voltage_array, therm_norm_currs,
                                                 maxfev=5000000, bounds=([-np.inf, -np.inf, 0, -np.inf], [np.inf, np.inf, 4, np.inf]))


    G0 = therm_params[0]
    z = therm_params[1]
    therm_top = therm_params[2]
    therm_bottom = therm_params[3]

    sigma_params = np.sqrt(np.diagonal(therm_cov))
    G0_sigma = sigma_params[0]
    z_sigma = sigma_params[1]
    top_sigma = sigma_params[2]
    bottom_sigma = sigma_params[3]

    alpha = 0.05

    tval = t.ppf(1 - alpha / 2.0, (len(voltage_array) - len(therm_params)))

    if G0_sigma == 0:
        G0_sigma = math.inf
    if z_sigma == 0:
        z_sigma = math.inf
    if top_sigma == 0:
        top_sigma = math.inf
    if bottom_sigma == 0:
        bottom_sigma = math.inf


    G0_lower_ci = G0 - (tval * (G0_sigma))
    G0_upper_ci = G0 + (tval * (G0_sigma))
    z_lower_ci = z - (tval * (z_sigma))
    z_upper_ci = z + (tval * (z_sigma))
    top_lower_ci = therm_top - (tval * (top_sigma))
    top_upper_ci = therm_top + (tval * (top_sigma))
    bottom_lower_ci = therm_bottom - (tval * (bottom_sigma))
    bottom_upper_ci = therm_bottom + (tval * (bottom_sigma))

    G0_lower_ci = "{:.5f}".format(G0_lower_ci)
    G0_upper_ci = "{:.5f}".format(G0_upper_ci)
    z_lower_ci = "{:.5f}".format(z_lower_ci)
    z_upper_ci = "{:.5f}".format(z_upper_ci)
    top_lower_ci = "{:.5f}".format(top_lower_ci)
    top_upper_ci = "{:.5f}".format(top_upper_ci)
    bottom_lower_ci = "{:.5f}".format(bottom_lower_ci)
    bottom_upper_ci = "{:.5f}".format(bottom_upper_ci)

    G0_ci = str('(' + str(G0_lower_ci) + ' ,' + str(G0_upper_ci) + ')')
    z_ci = str('(' + str(z_lower_ci) + ' ,' + str(z_upper_ci) + ')')
    top_ci = str('(' + str(top_lower_ci) + ' ,' + str(top_upper_ci) + ')')
    bottom_ci = str('(' + str(bottom_lower_ci) + ' ,' + str(bottom_upper_ci) + ')')

    # therm_model = boltzmann_therm(therm_voltage_array, G0, z)
    therm_model = boltzmann_therm(therm_voltage_array, G0, z, therm_top, therm_bottom)
    therm_rsquare = 1 - sum((therm_norm_currs - therm_model) ** 2) / sum(
        (therm_norm_currs - s_tats.mean(therm_norm_currs)) ** 2)

    therm_lower_rsquare = 'N/A'
    if len(lower_volt_indx) >= 2:
        therm_lower_rsquare = 1 - sum((therm_norm_currs[lower_volt_indx] - therm_model[lower_volt_indx]) ** 2) / sum(
            (therm_norm_currs[lower_volt_indx] - s_tats.mean(therm_norm_currs[lower_volt_indx])) ** 2)

    therm_param_results = np.array([G0, G0_ci, z, z_ci, therm_top, top_ci, therm_bottom, bottom_ci, therm_rsquare])
    therm_warning = ''

    if therm_rsquare < rsq_thresh:
        #pos40mVCD = 'N/A'
        returnDG = 'N/A'
        returnz = 'N/A'
        therm_warning = 'poor fit'
    else:
        '''
        if therm_lower_rsquare != 'N/A':
            
            if therm_lower_rsquare < 0.1:
                therm_warning = 'Fit of region from -50mV to -30mV Poor with RSquared = ' + str(therm_lower_rsquare)
                #pos40mVCD = 'N/A'
                #returnDG = 'N/A'
                returnDG = G0
                returnz = z
            else:
                returnDG = G0
                returnz = z
            
        else:
        '''
        returnDG = G0
        returnz = z

    return [returnDG, returnz, therm_model, therm_norm_currs, therm_voltage_array, therm_rsquare, therm_param_results, therm_warning, G0, z, therm_top, therm_bottom, pos40mVCD]



def ssAct_fit_py(input_file, output_dir, wellID, result_plots, num_sweeps, variant, rsq_thresh, summary_sweep_voltage, total_sweeps):
    # Initialise return value
    pos40mVCD = 'N/A'
    returnV05 = 'unset'
    returnDG = 'unset'
    returnK = 'unset'
    returnz = 'unset'

    numpy_pandas = 'pandas'

    if numpy_pandas == 'numpy':
        data = []
        with open(input_file) as csvfile:
            read = csv.reader(csvfile)
            for row in read:
                data.append(row)

        data = np.array(data)

        # Filtering the time data and removing noisy time regions
        time_us = data[1:, 0]
        #print(time_us)
        time_us = time_us.astype(np.float)
        # time_us = list(time_us)

        time_secs = time_us * 1e-6
        time_secs = list(time_secs)

        tot_range_time_indx_list = [i for i in range(len(time_secs)) if 1.3 >= time_secs[i] >= 1.205]
        #print('USING OLD PROTOCOL TIME RANGE')
        #tot_range_time_indx_list = [i for i in range(len(time_secs)) if 1.13 >= time_secs[i] >= 1.09]
        tot_range_time_indx_list = np.array(tot_range_time_indx_list)
        tot_range_time_indx_list = tot_range_time_indx_list.astype(int)

        time_secs = np.array(time_secs)
        time_secs = time_secs[tot_range_time_indx_list]

        time_secs = time_secs - 1.205

        time_ms = time_secs * 1e3

        # Extract the names of the actual sweeps
        sweepNumArray = data[0, 1:]
        voltage_array = data[2, 1:]
        voltage_array = voltage_array[1::2]
        voltage_array = voltage_array.astype(float)
        # Convert to mV units
        voltage_array = voltage_array * 1e3


        try:
            summary_sweep_index = list(voltage_array).index(summary_sweep_voltage)
            summary_sweep = sweepNumArray[2*summary_sweep_index]
            summary_sweep = summary_sweep.split('_')
            summary_sweep = int(summary_sweep[1])
        except:
            summary_sweep = 'N/A'


        dataArray = data[1:, 1:]
        #print(dataArray)
        #dataArray = dataArray.astype(np.float)
    else:
        data = pd.read_csv(input_file, sep=',', low_memory=False, header=None)

        # Filtering the time data and removing noisy time regions
        time_us = data.iloc[3:, 0].astype(float)

        time_secs = time_us * 1e-6

        tot_range_time_indx_list = [i for i in range(len(time_secs)) if 1.3 >= time_secs.iloc[i] >= 1.205]
        # print('USING OLD PROTOCOL TIME RANGE')
        # tot_range_time_indx_list = [i for i in range(len(time_secs)) if 1.13 >= time_secs[i] >= 1.09]
        #tot_range_time_indx_list = np.array(tot_range_time_indx_list)
        #tot_range_time_indx_list = tot_range_time_indx_list.astype(int)

        time_secs = time_secs.iloc[tot_range_time_indx_list]

        time_secs = time_secs - 1.205

        time_ms = time_secs * 1e3

        # Extract the names of the actual sweeps
        sweepNumArray = data.iloc[0, 1:]
        voltage_array = data.iloc[2, 1:]
        voltage_array = voltage_array.iloc[1::2]
        voltage_array = np.array(voltage_array).astype(float)
        # Convert to mV units
        voltage_array = voltage_array * 1e3

        try:
            summary_sweep_index = list(voltage_array).index(summary_sweep_voltage)
            summary_sweep = sweepNumArray.iloc[2 * summary_sweep_index]
            summary_sweep = summary_sweep.split('_')
            summary_sweep = int(summary_sweep[1])
        except:
            summary_sweep = 'N/A'

        dataArray = data.iloc[1:, 1:]
        # print(dataArray)
        # dataArray = dataArray.astype(np.float)

    # A matrix storing the results of the current densities for all the sweeps in the well
    current_dens_data = []
    current_dens_data.append([])
    #current_dens_data[0].append('SweepNum')
    current_dens_data[0].append('Voltage (mV)')
    current_dens_data[0].append('Current Density (pA/pF)')


    # create an 13 row result list

    for i in range(1, total_sweeps + 1):
        current_dens_data.append([])
        '''
        sw = i
        current_dens_data[i].append('Sweep' + str(sw))
        '''


    os.mkdir(os.path.join(result_plots, wellID))
    norm_currs = np.array([])     #array that stores the current densities which is then normalised using the minimum current dens
    #print((2*num_sweeps)-1)
    #print(np.shape(dataArray))
    for sweep in range(1, (2*num_sweeps), 2):
        #print(sweep)

        if numpy_pandas == 'numpy':
            actual_sweep = sweepNumArray[sweep]
            actual_sweep = actual_sweep.split('_')
            actual_sweep = int(actual_sweep[1])

            sweepData = dataArray[tot_range_time_indx_list, sweep]
            sweepData = np.array(sweepData).astype(float)

            capacitance = np.array(dataArray[0, sweep]).astype(float)
        else:
            actual_sweep = sweepNumArray.iloc[sweep]
            actual_sweep = actual_sweep.split('_')
            actual_sweep = int(actual_sweep[1])

            capacitance = float(dataArray.iloc[0, sweep])

            sweepData = dataArray.iloc[2:, sweep]
            sweepData = sweepData.iloc[tot_range_time_indx_list].astype(float)



        '''
        plt.figure()
        plt.plot(time_secs, sweepData)
        plt.title(wellID + ' ' + str(actual_sweep))
        plt.show()
        '''

        #print(sweepData)
        #time.sleep(4)

        #print(capacitance)

        min_curr_amp = min(sweepData)
        # Current density = minimum current amplitude / capacitance
        current_density = min_curr_amp / capacitance
        #current_density = min_curr_amp
        current_dens_data[actual_sweep].append(voltage_array[int(sweep/2)])
        current_dens_data[actual_sweep].append(current_density)

        #print(actual_sweep)
        #print(summary_sweep)
        if actual_sweep == summary_sweep:
            #pos40mVCD = 'current_density = ' + str(current_density) + ' min current =  ' + str(min_curr_amp) + ' capacitance = ' + str(capacitance)
            pos40mVCD = current_density

        norm_currs = np.append(norm_currs, min_curr_amp)

        fig = plt.figure()
        plt.plot(time_secs, sweepData)
        plt.xlabel('Time(s)')
        plt.ylabel('Current (pA)')
        plt.title('Raw Current Data Sweep' + str(actual_sweep) + ' ' + str(min_curr_amp))
        plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '_image')
        with open(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '.pickle', 'wb') as fig_file:
            pickle.dump(fig, fig_file)
        fig_file.close()
        plt.close(fig)



    #print(pos40mVCD)
    # Now fit the minimum current data to the boltzmann curves
    if len(norm_currs) < 8:
        if returnV05 == 'unset':
            returnV05 = 'N/A'
        if returnK == 'unset':
            returnK = 'N/A'
        if returnDG == 'unset':
            returnDG = 'N/A'
        if returnz == 'unset':
            returnz = 'N/A'

        return [pos40mVCD, returnV05, returnDG, returnK, returnz]


    #norm_currs = norm_currs[::-1]
    #voltage_array = voltage_array[::-1]
    #print(wellID)
    #print(norm_currs)
    #print(voltage_array)
    orig_norm_currs = norm_currs
    #print(norm_currs)
    #norm_currs = abs(norm_currs)
    max_normcurr = max(norm_currs)
    max_normcurr = min(norm_currs)
    #print()
    # norm_currs = norm_currs / max_normcurr
    norm_currs = np.divide(norm_currs, [max_normcurr])
    #print(norm_currs)

    fit_parameters = np.array(['V05', 'V05 95% CI', 'k', 'k 95% CI', 'top', 'top 95% CI', 'bottom', 'bottom 95% CI', 'RSquared', 'Warning'])

    [returnV05, returnK, model, rsquare, V05_ok, fit_params_results, warning, V05, k, top, bottom, lower_volt_indx, pos40mVCD] = V05_analysis(voltage_array, norm_currs, rsq_thresh, returnV05, returnK, pos40mVCD, wellID)

    [warning, include_summary] = post_analysis_qc(model, norm_currs, voltage_array, warning, wellID, 'no')

    if include_summary == 0:
        returnV05 = 'N/A'
        returnK = 'N/A'
    if include_summary == 2:
        norm_currs = orig_norm_currs[0:-1]
        # norm_currs = abs(norm_currs)
        # max_curr = max(norm_currs)
        max_curr = min(norm_currs)
        norm_currs = np.divide(norm_currs, [max_curr])
        voltage_array = voltage_array[0:-1]

        [returnV05, returnK, model, rsquare, V05_ok, fit_params_results, warning, V05, k, top, bottom, lower_volt_indx,
         pos40mVCD] = V05_analysis(voltage_array, norm_currs, rsq_thresh, returnV05, returnK, pos40mVCD, wellID)
        if warning:
            warning += ' and Endogenous Current Exhibited'
        else:
            warning = 'Endogenous Current Exhibited'
        [warning, include_summary] = post_analysis_qc(model, norm_currs, voltage_array, warning, wellID, 'yes')
        if include_summary == 0:
            returnV05 = 'N/A'
            returnK = 'N/A'
        include_summary = 2


    if rsquare > rsq_thresh and V05_ok == 1:
        therm_fit_parameters = np.array(['G0', 'z', 'top', 'bottom'])
        #therm_fit_parameters = np.array(['G0', 'G0 95% CI', 'z', 'z 95% CI', 'top', 'top 95% CI', 'bottom', 'bottom 95% CI', 'RSquared', 'Warning'])
        #[returnDG, returnz, therm_model, therm_norm_currs, therm_voltage_array, therm_rsquare, therm_param_results, therm_warning, G0, z, therm_top, therm_bottom, pos40mVCD] = therm_fit_analysis(voltage_array, norm_currs, rsq_thresh, returnDG, returnz, lower_volt_indx, pos40mVCD)
        [returnDG, returnz, therm_param_results, G0, z, therm_top, therm_bottom] = therm_analysis(V05, k, top, bottom, returnDG, returnz)

        '''
        if therm_model.any():
            if include_summary == 2:
                [therm_warning, include_therm_summary] = post_analysis_qc(therm_model, therm_norm_currs, therm_voltage_array, therm_warning, wellID, 'yes')
                if therm_warning:
                    therm_warning += ' and Endogenous Current Exhibited'
                else:
                    therm_warning = 'Endogenous Current Exhibited'
            else:
                [therm_warning, include_therm_summary] = post_analysis_qc(therm_model, therm_norm_currs, therm_voltage_array, therm_warning, wellID, 'no')
            if include_therm_summary == 0:
                returnDG = 'N/A'
                returnz = 'N/A'

            #IGNORE FROM HERE 
            if include_therm_summary == 2:
            # Endogenous current observed in post-qc analysis, remove last element and re-analyse without endogenous current
                if np.shape(voltage_array)[0] >= 6:
                    therm_cds = orig_norm_currs[0:-1]
                    #therm_cds = abs(therm_cds)
                    therm_vs = voltage_array[0:-1]
                    #max_cd = max(therm_cds)
                    max_cd = min(therm_cds)
                    therm_cds = np.divide(therm_cds, [max_cd])
                    if therm_warning:
                        therm_warning += ' and Endogenous Current Exhibited'
                    else:
                        therm_warning += 'Endogenous Current Exhibited'
                    [returnDG, returnz, therm_model, therm_norm_currs, therm_voltage_array, therm_rsquare, therm_param_results, therm_warning, G0, z, therm_top, therm_bottom, pos40mVCD] = therm_analysis(therm_vs, therm_cds, rsq_thresh, returnDG, returnz, lower_volt_indx, pos40mVCD)
                    [therm_warning, include_therm_summary] = post_analysis_qc(therm_model, therm_norm_currs, therm_voltage_array, therm_warning, wellID)
                    if include_therm_summary == 0:
                        returnDG = 'N/A'
                        returnz = 'N/A'
            #IGNORE TO HERE
            
            
            fig = plt.figure()
            plt.plot(therm_voltage_array, therm_norm_currs, 'o')
            plt.plot(therm_voltage_array, therm_model)
            plt.title(wellID + ' Thermodynamic Boltzmann Curve')
            plt.xlabel('Voltages (mV)')
            plt.ylabel('Normalised Currrent')
            plt.savefig(os.path.join(result_plots, wellID, 'Thermodynamic_' + wellID)+'_image')
            with open(os.path.join(result_plots, wellID, 'Thermodynamic_' + wellID)+'.pickle', 'wb') as fig_file:
                pickle.dump(fig, fig_file)
            fig_file.close()
            '''

        #therm_param_results = np.append(therm_param_results, warning)
        therm_fit_parameters = np.vstack((therm_fit_parameters, therm_param_results))

        therm_file = os.path.join(output_dir, wellID + '_thermodynamic_parameters.csv')
        with open(therm_file, mode='w') as therm_output:
            result_writer = csv.writer(therm_output, delimiter=',', lineterminator='\n')
            for row in range(0, 2):
                result_writer.writerow(therm_fit_parameters[row])


    #if returnDG == 'N/A' or returnK == 'N/A' or returnV05 == 'N/A':
    #    pos40mVCD = 'N/A'

    if returnV05 == 'V05' or returnK == 'V05':
        returnV05 = 'N/A'
        returnK = 'N/A'

    if returnK == 'unset':
        returnK = 'N/A'

    if returnV05 == 'unset':
        returnV05 = 'N/A'

    if returnDG == 'unset':
        returnDG = 'N/A'

    if returnz == 'unset':
        returnz = 'N/A'

    if variant == 'neg_ctrl':
        returnK = 'N/A'
        returnV05 = 'N/A'
        returnDG = 'N/A'
        returnz = 'N/A'


    fit_params_results = np.append(fit_params_results, warning)
    fit_parameters = np.vstack((fit_parameters, fit_params_results))

    fig = plt.figure()
    plt.plot(voltage_array, norm_currs, 'o')
    plt.plot(voltage_array, model)
    plt.title(wellID + ' V05 Boltzmann Curve')
    plt.xlabel('Voltages (mV)')
    plt.ylabel('Normalised Currrent')
    plt.savefig(os.path.join(result_plots, wellID, 'V05_' + wellID)+'_image')
    with open(os.path.join(result_plots, wellID, 'V05_' + wellID)+ '.pickle', 'wb') as fig_file:
        pickle.dump(fig, fig_file)
    fig_file.close()
    plt.close(fig)

    V05_file = os.path.join(output_dir, wellID + '_V05_parameters.csv')
    with open(V05_file, mode='w') as V05_output:
        res_writer = csv.writer(V05_output, delimiter=',', lineterminator='\n')
        for row in range(0, 2):
            res_writer.writerow(fit_parameters[row])

    cd_file = os.path.join(output_dir, wellID + '_current_densities.csv')
    with open(cd_file, mode='w') as cd_output:
        res_cd_writer = csv.writer(cd_output, delimiter=',', lineterminator='\n')
        for row in range(0, total_sweeps + 1):
            res_cd_writer.writerow(current_dens_data[row])

    plt.close('all')
    #print(pos40mVCD)
    return [pos40mVCD, returnV05, returnDG, returnK, returnz]
