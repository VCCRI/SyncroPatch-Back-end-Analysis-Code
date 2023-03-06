import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import stats
import os
import statistics as s_tats
import warnings
import time
import pickle
from scipy.stats.distributions import t
import math
import pandas as pd

from ssDeact_warnings import generate_warnings
from ssDeact_warnings_neg_summary import generate_neg_summary_warnings

def exp_curve(x, A, B, tau, C):
#def exp_curve(x, A, tau, C):
    return A*np.exp((x+B)/tau) + C
    #return A*np.exp(x/tau) + C


def fit_taus(tau_array, voltage_array, sweep_array, parameter_data, slow_fast, wellID):
    # p0 = [10, 1, 0]
    try:
        voltage_array_fit = (voltage_array - min(voltage_array))/(max(voltage_array) - min(voltage_array))
        tau_array_fit = (tau_array - min(tau_array))/(max(tau_array)-min(tau_array))
        #p0 = [tau_array_fit[0], 40, tau_array_fit[-1]]
        p0 = [tau_array_fit[0], -1 * voltage_array_fit[-1], 40, tau_array_fit[-1]]
        params, cov = optimize.curve_fit(exp_curve, voltage_array_fit, tau_array_fit, p0, maxfev=500000, loss='soft_l1', f_scale=0.1, method='trf')


    except:
        # print(wellID)
        '''
        plt.figure()
        plt.plot(voltage_array, tau_array, 'o')
        plt.title(wellID)
        plt.show()
        '''

        for i in range(0, len(sweep_array)):
            sweep = int(sweep_array[i])
            sweep_data = np.array(parameter_data[sweep])
            warning = sweep_data[-1]
            if warning:
                if slow_fast == 'slow':
                    warning += ' and exponential trend unable to be modelled for slow tau values'
                elif slow_fast == 'fast':
                    warning += ' and exponential trend unable to be modelled for fast tau values'
                elif slow_fast == 'weighted':
                    warning += ' and exponential trend unable to be modelled for weighted tau values'
            else:
                if slow_fast == 'slow':
                    warning = 'exponential trend unable to be modelled for slow tau values'
                elif slow_fast == 'fast':
                    warning = 'exponential trend unable to be modelled for fast tau values'
                elif slow_fast == 'weighted':
                    warning = 'exponential trend unable to be modelled for weighted tau values'
            # print('fail fit')
            sweep_data = sweep_data.astype((str, 300))
            sweep_data[-1] = warning
            # print(sweep_data)
            parameter_data[sweep] = list(sweep_data)
            # print(parameter_data[sweep])
        # print(wellID + ' return cos fit fail')
        return [parameter_data, 'N/A', 'N/A']

    # print(str(params[0]) + ' ' + str(params[1]) + ' ' + str(params[2]) + ' ' + str(params[3]))
    #voltage_array = voltage_array * 1000
    #non_lin_model = np.array(exp_curve(voltage_array, params[0], params[1], params[2]).astype(float))
    non_lin_model = np.array(exp_curve(voltage_array_fit, params[0], params[1], params[2], params[3]).astype(float))
    non_lin_model = non_lin_model * (max(tau_array) - min(tau_array)) + min(tau_array)
    #voltage_array = voltage_array*1000

    #non_lin_model = np.array(exp_curve(voltage_array, params[0] * (max(tau_array) - min(tau_array)) + min(tau_array), params[1]*(max(voltage_array)-min(voltage_array))+min(voltage_array), params[2]*(max(tau_array) - min(tau_array))+min(tau_array)).astype(float))
    # print(str(params[0]) + ' ' + str(params[1]) + ' ' + str(params[2]))

    '''
    non_lin_model = np.poly1d(np.polyfit(voltage_array, tau_array, 5))
    non_lin_model = non_lin_model(voltage_array)
    '''

    rsquare = 1 - sum((tau_array.astype(float) - non_lin_model) ** 2) / sum(
        (tau_array.astype(float) - s_tats.mean(tau_array.astype(float))) ** 2)
    rsq_str = '%.4f' % rsquare
    if slow_fast == 'slow':
        qc_fig_name = wellID + '_slow_tau_postQC_exponential_fit_RSquared_' + str(rsq_str) + '.png'
    elif slow_fast == 'fast':
        qc_fig_name = wellID + '_fast_tau_postQC_exponential_fit_RSquared_' + str(rsq_str) + '.png'
    elif slow_fast == 'weighted':
        qc_fig_name = wellID + '_weighted_tau_postQC_exponential_fit_RSquared_' + str(rsq_str) + '.png'

    tau_outliers = np.array([])
    volt_outliers = np.array([])
    if rsquare < .85:
        # print(str(rsquare) + ' failed')
        # Now go through and tag each warning with 'exponential trend unable to be modelled for tau values'
        for i in range(0, len(sweep_array)):
            sweep = int(sweep_array[i])
            sweep_data = np.array(parameter_data[sweep])
            warning = sweep_data[-1]
            if warning:
                if slow_fast == 'slow':
                    warning += ' and exponential fit poor for slow tau values'
                elif slow_fast == 'fast':
                    warning += ' and exponential fit poor for fast tau values'
                elif slow_fast == 'weighted':
                    warning += ' and exponential fit poor for weighted tau values'
            else:
                if slow_fast == 'slow':
                    warning = 'exponential fit poor for slow tau values'
                elif slow_fast == 'fast':
                    warning = 'exponential fit poor for fast tau values'
                elif slow_fast == 'weighted':
                    warning = 'exponential fit poor for weighted tau values'
            # print(warning)
            # print('rsq')
            sweep_data = sweep_data.astype((str, 300))
            sweep_data[-1] = warning
            # print(sweep_data)
            parameter_data[sweep] = list(sweep_data)
            # print(parameter_data[sweep])
            # time.sleep(4)
            #non_lin_model = non_lin_model[::-1]
    '''
    else:
        tau_stdev = s_tats.stdev(tau_array)
        tau_array = tau_array[::-1]
        voltage_array = voltage_array[::-1]
        non_lin_model = non_lin_model[::-1]
        # tau_outliers = np.array([])
        # volt_outliers = np.array([])
        for i in range(0, len(tau_array)):
            if abs(tau_array[i] - non_lin_model[i]) > 1 * tau_stdev:
                sweep = int(sweep_array[i])
                sweep_data = np.array(parameter_data[sweep])
                warning = sweep_data[-1]
                if not warning:
                    if slow_fast == 'slow':
                        warning = 'Slow tau value a possible outlier'
                    else:
                        warning = 'Fast tau value a possible outlier'
                else:
                    if slow_fast == 'slow':
                        warning += ' and slow tau value a possible outlier'
                    else:
                        warning += ' and fast tau value a possible outlier'

                sweep_data = sweep_data.astype((str, 300))
                sweep_data[-1] = warning
                parameter_data[sweep] = list(sweep_data)
                tau_outliers = np.append(tau_outliers, tau_array[i])
                volt_outliers = np.append(volt_outliers, voltage_array[i])
                print(wellID + ' outlier')
                print(tau_array[i])
                print(parameter_data[sweep])
    
        non_lin_model = non_lin_model[::-1]
    '''

    return [parameter_data, non_lin_model, qc_fig_name]

def post_analysis_qc(voltage_array, parameter_data, result_plots, wellID, slow_fast, summary_voltage):
# Plot the current densities against their voltages and then extract outliers and flag these sweeps

    #print(len(parameter_data))
    #print(type(parameter_data))

    voltage_array = voltage_array / 1000
    summary_voltage = summary_voltage / 1000
    tau_array = np.array([])
    sweep_array = np.array([])
    fit_voltages = np.array([])
    volt_indx = 0
    include_summary = 1
    for i in range(1, len(parameter_data)):
        if len(parameter_data[i]) > 1:
            volt_indx += 1
            sweep_data = np.array(parameter_data[i])
            if sweep_data[1] == -80 or sweep_data[1] == -90:
                #print('skip reversal potential in postqc')
                continue
            if 'Rsquare' in sweep_data[-1] or 'current' in sweep_data[-1] or 'negative' in sweep_data[-1] or 'duration' in sweep_data[-1] or 'amplitude' in sweep_data[-1]:
                #print(sweep_data[-1])
                continue
            #print(sweep_data)
            #print(parameter_data)
            if slow_fast == 'fast':
                '''
                print('fast')
                print(sweep_data)
                print('tau1='+sweep_data[4])
                print('tau2='+sweep_data[5])
                print(type(sweep_data[5]))
                '''
                if float(sweep_data[5]) < float(sweep_data[6]):
                    tau_array = np.append(tau_array, sweep_data[5])
                else:
                    tau_array = np.append(tau_array, sweep_data[6])
                #print('appended '+tau_array[-1])
            elif slow_fast == 'slow':
                '''
                print('slow')
                print(sweep_data)
                print('tau1=' + sweep_data[4])
                print('tau2=' + sweep_data[5])
                print(type(sweep_data[4]))
                '''
                if float(sweep_data[5]) < float(sweep_data[6]):
                    tau_array = np.append(tau_array, sweep_data[6])
                else:
                    tau_array = np.append(tau_array, sweep_data[5])
            elif slow_fast == 'weighted':
                tau_array = np.append(tau_array, sweep_data[12])

            sweep_array = np.append(sweep_array, i)
            fit_voltages = np.append(fit_voltages, sweep_data[1])

    voltage_array = fit_voltages.astype(float)
    tau_array = tau_array.astype(float)
    #print(voltage_array)


    if np.shape(tau_array)[0] <= 4:
        # print(wellID + ' return cos not enough data')
        return [parameter_data, include_summary]

    # Now ensure there is an increasing trend in taus
    prev_tau = tau_array[0]
    success_taus = np.array([tau_array[0]])
    success_v = np.array([voltage_array[0]])
    new_sw_array = np.array([sweep_array[0]])
    fail_tau_indx = np.array([])

    #print(tau_array)
    for t in range(1, np.shape(tau_array)[0]):
        if tau_array[t] < prev_tau:
            success_taus = np.append(success_taus, tau_array[t])
            success_v = np.append(success_v, voltage_array[t])
            new_sw_array = np.append(new_sw_array, sweep_array[t])
            prev_tau = tau_array[t]
        else:

            sweep = int(sweep_array[t])
            sweep_data = np.array(parameter_data[sweep])
            warning = sweep_data[-1]
            if voltage_array[t] == summary_voltage:
                '''
                
                print('no summary')
                print(wellID)
                print(voltage_array[t])
                print(summary_voltage)
                '''
                include_summary = 0
            if not warning:
                if slow_fast == 'slow':
                    warning = 'Slow tau value not following increasing trend'
                elif slow_fast == 'fast':
                    warning = 'Fast tau value not following increasing trend'
                elif slow_fast == 'weighted':
                    warning = 'Weighted tau value not following increasing trend'
            else:
                if slow_fast == 'slow':
                    warning += ' and slow tau value not following increasing trend'
                elif slow_fast == 'fast':
                    warning += ' and fast tau value not following increasing trend'
                elif slow_fast == 'weighted':
                    warning += ' and weighted tau value not following increasing trend'

            sweep_data = sweep_data.astype((str, 300))
            sweep_data[-1] = warning
            parameter_data[sweep] = list(sweep_data)

    #print(parameter_data)
    #time.sleep(10)
    if np.shape(tau_array)[0] <= 4:
        #print(wellID + ' return cos not enough data')
        include_summary = 1
        return [parameter_data, include_summary]

    # Invert the arrays so that they exhibit order of cartesian plane for fitting purposes
    tau_array = success_taus[::-1]
    voltage_array = success_v[::-1]
    sweep_array = new_sw_array

    #tau_array = 1 / tau_array
    if slow_fast == 'slow':
        tit = 'slow ' + wellID
    elif slow_fast == 'fast':
        tit = 'fast ' + wellID
    elif slow_fast == 'weighted':
        tit = 'weighted ' + wellID

    '''
    plt.figure()
    plt.plot(voltage_array, tau_array)
    plt.title(tit)
    plt.show()
    '''


    # Outlier analysis for non-normally distributed data:
    # Fit the data, obtain model. Go through each point and determine how far it deviates from the model. Get the model? or data? stdev and if the point more than 3 stdevs from model then is outlier

    #params, cov = optimize.curve_fit(linear_fit, voltage_array, tau_array)
    #lin_model = np.array(linear_fit(voltage_array, params[0], params[1])).astype(float)
    #print(str(params[0]) + ' ' + str(params[1]))
    [parameter_data, non_lin_model, qc_fig_name] = fit_taus(tau_array, voltage_array, sweep_array, parameter_data, slow_fast, wellID)
    if non_lin_model == 'N/A':
        return [parameter_data, include_summary]

    '''
    if np.shape(tau_outliers)[0] > 0:
        indx_outliers = np.array([])
        for o in range(0, np.shape(tau_outliers)[0]):
            indx_outlier = [i for i in range(0, len(tau_array)) if tau_array[i] == tau_outliers[o]]
            indx_outliers = np.append(indx_outliers, indx_outlier)
        new_taus = np.array([])
        new_vs = np.array([])
        new_sws = np.array([])
        sweep_array = sweep_array[::-1]
        for i in range(0, np.shape(tau_array)[0]):
            if i not in indx_outliers:
                new_taus = np.append(new_taus, tau_array[i])
                new_vs = np.append(new_vs, voltage_array[i])
                new_sws = np.append(new_sws, sweep_array[i])

        tau_array = new_taus
        voltage_array = new_vs
        sweep_array = new_sws[::-1]
        [parameter_data, non_lin_model, tau_outliers, volt_outliers, qc_fig_name] = fit_taus(tau_array, voltage_array, sweep_array, parameter_data, slow_fast, wellID)
        if non_lin_model == 'N/A':
            return parameter_data
    '''

    fig = plt.figure()
    #voltage_array = voltage_array*1000
    #volt_outliers = volt_outliers*1000
    plt.plot(voltage_array, tau_array, 'o')
    plt.plot(voltage_array, non_lin_model)
    #plt.plot(volt_outliers, tau_outliers, 'ro')
    #plt.xticks(np.arange(min(voltage_array), max(voltage_array)+1, 10))
    plt.title(tit + ' fit')
    plt.xlabel('Voltage (mV)')
    plt.ylabel('Tau ' + slow_fast + ' (ms)')
    plt.savefig(os.path.join(result_plots, wellID, qc_fig_name))
    plt.close(fig)
    return [parameter_data, include_summary]


def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)


def double_exponential(x, A, B, C, tau1, tau2):
    return A*np.exp(-x/tau1) + B*np.exp(-x/tau2) + C

def peak_current_greater_threshold(times, currents, peak_current_parameter, start_time=0.002, end_time=3.0):
    print(peak_current_parameter)
    min_current = min([float(c) for t,c in zip(times, currents) if start_time <= float(t) <= end_time])
    print(min_current)
    return (min_current > peak_current_parameter)

def peak_current_smaller_threshold(times, currents, peak_current_parameter, start_time=0.002, end_time=3.0):
    #print(peak_current_parameter)
    max_current = max([float(c) for t,c in zip(times, currents) if start_time <= float(t) <= end_time])
    #print(max_current)
    return (max_current < peak_current_parameter)


def ssDeact_fit_py(input_file, output_file, wellID, result_plots, num_sweeps, variant, sweep_length, rsq_thresh, summary_sweep_voltage, total_sweeps, amp_thresh):

    # Initialise return value
    neg50mVTW = 'N/A'

    numpy_pandas = 'pandas'

    if numpy_pandas == 'numpy':
        data = []
        with open(input_file) as csvfile:
            read = csv.reader(csvfile)
            for row in read:
                data.append(row)


        # Filtering the time data and removing noisy time regions
        #time_us = data[1:, 0]  #np array implementation
        time_us = [row[0] for row in data]
        time_us = time_us[1:]
        #print(time_us)
        #return neg50mVTW
        time_us = np.array(time_us)
    else:
        data = pd.read_csv(input_file, sep=',', low_memory=False, header=None)
        time_us = data.iloc[3:, 0]

    time_us = np.array(time_us).astype(np.float)
    #time_us = list(time_us)


    time_secs = time_us * 1e-6
    full_time_secs = time_secs
    time_secs = list(time_secs)
    #start_time = time_secs.index(1.215)
    if summary_sweep_voltage == 50:
        start_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 1.20]
        start_time = start_time_indx_list[0]
        end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= (sweep_length + 1.2)]
        end_time = end_time_indx_list[0]
    else:
        start_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 1.10]
        start_time = start_time_indx_list[0]
        end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= (sweep_length + 1.10)]
        end_time = end_time_indx_list[0]


    #end_time = time_secs.index(sweep_length + 1.2)
    time_secs = time_secs[start_time:end_time]
    time_secs = np.array(time_secs)
    orig_time_secs = time_secs

    orig_time_ms = time_secs * 1e3


    #T=1.2s is when the voltage pulse was applied to the well, and the amplitudes need to be extracted back to this point. i.e. treat this as t=0
    orig_time_secs = orig_time_secs - orig_time_secs[0]
    orig_time_ms = orig_time_ms - orig_time_ms[0]


    # Extract the names of the actual sweeps
    #sweepNumArray = data[0, 1:]    #np array implementation
    #voltage_array = data[1, 1:]    #np array implementation
    if numpy_pandas == 'numpy':
        sweepNumArray = data[0]
        sweepNumArray = sweepNumArray[1:]
        voltage_array = data[2]
        voltage_array = voltage_array[1:]
        voltage_array = np.array(voltage_array)
        #if summary_sweep_voltage != 52:
        voltage_array = voltage_array[1::2].astype(float)

        # Convert to mV units
        voltage_array = voltage_array * 1e3
    else:
        sweepNumArray = data.iloc[0]
        sweepNumArray = sweepNumArray.iloc[1:]
        sweepNumArray = np.array(sweepNumArray)
        voltage_array = data.iloc[2]
        voltage_array = voltage_array.iloc[1:]
        voltage_array = np.array(voltage_array)
        # if summary_sweep_voltage != 52:
        voltage_array = voltage_array[1::2].astype(float)

        # Convert to mV units
        voltage_array = voltage_array * 1e3

    # Now iterate through the voltage array to extract the summary sweep
    try:
        summary_sweep_index = list(voltage_array).index(summary_sweep_voltage)
        #print(summary_sweep_index)
        summary_sweep = 'N/A'
        if summary_sweep_index:
            #multiply by 2
            summary_sweep = sweepNumArray[2*summary_sweep_index]
            summary_sweep = summary_sweep.split('_')
            summary_sweep = int(summary_sweep[1])
    except:
        summary_sweep = 'N/A'

    #dataArray = [data[1:, 2:]
    #dataArray = dataArray[1:]
    #dataArray = dataArray.astype(np.float)

    parameter_data = []
    parameter_data.append([])
    parameter_data[0].append('SweepNum')
    parameter_data[0].append('Voltage (mV)')
    parameter_data[0].append('Amplitude Slow Component (pA)')
    parameter_data[0].append('Amplitude Slow Component 95% CI')
    parameter_data[0].append('Amplitude Fast Component (pA)')
    parameter_data[0].append('Amplitude Fast Component 95% CI')
    parameter_data[0].append('Vertical Offset (pA)')
    parameter_data[0].append('Vertical Offset 95% CI')
    parameter_data[0].append('tau Slow (ms)')
    parameter_data[0].append('tau Slow 95% CI')
    parameter_data[0].append('tau Fast (ms)')
    parameter_data[0].append('tau Fast 95% CI')
    parameter_data[0].append('t_weighted (ms)')
    parameter_data[0].append('Af/(Af+As) (%)')
    parameter_data[0].append('Start Trim Time (secs)')
    parameter_data[0].append('End Trim Time (secs)')
    parameter_data[0].append('RSquared')
    parameter_data[0].append('Fit Warnings')

    #create an 18 row result list
    for i in range(1, total_sweeps+1):
        parameter_data.append([])
        sw = i
        parameter_data[i].append('Sweep'+str(sw))


    os.mkdir(os.path.join(result_plots, wellID))
    # Start at index 1 and iterate every second column so not to analyse voltage columns
    rsquare = -1
    analyse_neg = 0
    warning = 'N/A'
    orig_sweep_length = sweep_length
    current_density_neg_50mV = 'N/A'
    current_density_neg_120mV = 'N/A'
    peak_neg_50mV = 'N/A'
    peak_neg_120mV = 'N/A'
    cap_neg_50mV = 'N/A'
    cap_neg_120mV = 'N/A'

    for sweep in range(1, (2*num_sweeps), 2):
        actual_sweep = sweepNumArray[sweep]
        actual_sweep = actual_sweep.split('_')
        actual_sweep = int(actual_sweep[1])

        sweep_voltage = voltage_array[int(sweep / 2)]

        if sweep_voltage == -80 or sweep_voltage == -90:
        #if actual_sweep == 11 or actual_sweep == 12:
            continue

        #Variables that indicates whether to use previous fit parameters as start point inputs for this fit iteration
        #Dynamic start point initialisation
        #if actual_sweep >= 11:
        if sweep_voltage <= -80:
            #When equal to 0, set to 2 so program knows to seed with initial p0 parameters
            if analyse_neg == 0:
                analyse_neg = 2
            else:
                #When equal to 1 program knows to use previous iterations of params for seeds
                analyse_neg = 1

        #sweepData = dataArray[:, sweep]
        if numpy_pandas == 'numpy':
            sweepData = [row[sweep+1] for row in data]
            sweepData = np.array(sweepData[1:]).astype(np.float)

            full_sweepData = sweepData
            capacitance = sweepData[0]
            sweepData = sweepData[start_time:end_time]
            orig_sweepData = sweepData
        else:
            sweepData = data.iloc[1:, sweep+1].astype(float)
            full_sweepData = sweepData
            capacitance = sweepData.iloc[0]
            sweepData = sweepData.iloc[2:]
            sweepData = sweepData[start_time:end_time]
            orig_sweepData = sweepData

        '''
        voltageData = [row[sweep] for row in data]
        voltageData = 1000*np.array(voltageData[1:]).astype(np.float)

        start_time = [i for i in range(len(list(voltageData)) if voltageData[i] != -40)
        start_time = start_time[0]
        '''
        #sweep_voltage = voltage_array[sweep]



        time_secs = orig_time_secs


        time_ms = orig_time_ms
        sweepData = sweepData * 1e12

        if summary_sweep_voltage > -80:
            if sweep_voltage == summary_sweep_voltage:
                if max(sweepData) < amp_thresh:
                    continue
        else:
            if sweep_voltage == summary_sweep_voltage:
                if min(sweepData) > amp_thresh:
                    continue

        # Now check if there is a capacitive spike. If yes then trim time and current data again
        '''
        Use the minimum or maximum, depending on the curve shape, to trim the best
        '''
        #if actual_sweep < 11:
        if sweep_voltage > -80:
            max_current = max(sweepData)
            indx_max_current = 2*(list(sweepData).index(max_current))
            #indx_max_current = math.floor(1.5 * (list(sweepData).index(max_current)))
            sweepData = sweepData[indx_max_current:]
            time_secs = orig_time_secs[indx_max_current:]
            time_ms = orig_time_ms[indx_max_current:]
            #time_secs = time_secs - time_secs[0]
            #time_ms = time_ms - time_ms[0]


            #Early sweeps aren't as receptive to the max point trimmin
            #Compare standard deviations of start portion and all data to determine if noise is still present at the start

            if np.shape(time_secs)[0] >= 200:
                overall_std = s_tats.stdev(sweepData)
                start_std = s_tats.stdev(sweepData[0:200])

                if start_std > overall_std:
                    #trim_extra_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.01]
                    #trim_extra_time = trim_extra_time_indx_list[0]
                    trim_extra_time = 200
                    sweepData = sweepData[trim_extra_time:]
                    time_secs = time_secs[trim_extra_time:]
                    time_ms = time_ms[trim_extra_time:]
                    #time_secs = time_secs - time_secs[0]
                    #time_ms = time_ms - time_ms[0]



            #Check the time scale is acceptable. If it appears that too much has been trimmed then hardcode the time value trimmed
            '''
            if (time_secs[-1] - time_secs[0]) < 2.75:
                #This equivalent to 1.215 s but since whole time scale subtracted by 1.2 then test 0.015
                start_time_indx_list = [i for i in range(len(orig_time_secs)) if orig_time_secs[i] >= 1.215]
                start_time = start_time_indx_list[0]
                time_secs = orig_time_secs[start_time:]
                sweepData = orig_sweepData[start_time:]
            '''

            '''
            else:
                time_secs = orig_time_secs
                time_ms = orig_time_ms
            '''
        else:
            min_current = min(sweepData)
            indx_min_current = 2*(list(sweepData).index(min_current))
            #indx_min_current = math.floor(1.5 * (list(sweepData).index(min_current)))

            #if actual_sweep >= 17:
            if sweep_voltage <= -140:
                indx_last_time = [i for i in range(len(orig_time_secs)) if orig_time_secs[i] >= 1]
                indx_last_time = indx_last_time[0]
            else:
                indx_last_time = [i for i in range(len(orig_time_secs)) if orig_time_secs[i] >= 1.5]
                indx_last_time = indx_last_time[0]


            sweepData = sweepData[indx_min_current:indx_last_time]
            time_secs = orig_time_secs[indx_min_current:indx_last_time]
            time_ms = orig_time_ms[indx_min_current:indx_last_time]
            #time_secs = time_secs - time_secs[0]
            #time_ms = time_ms - time_ms[0]

            #sweepData = sweepData[indx_min_current:-1]
            #time_secs = orig_time_secs[indx_min_current:-1]
            #time_ms = orig_time_ms[indx_min_current:-1]

            '''
            #if actual_sweep >=14:
            if actual_sweep >= 14:
                try:
                    max_peak = max(sweepData)
                    if max_peak > 0:
                        max_peak_0_95= 0.95*max_peak
                    else:
                        # Fix peak trimming
                        peak_0_05 = 0.05 * abs(max_peak)
                        max_peak_0_95 = max_peak - peak_0_05

                    #print(max(sweepData))
                    #print(max_peak_0_95)
                    indx_max_095_peak = [i for i in range(len(list(sweepData))) if sweepData[i] >= max_peak_0_95]
                    indx_max_095_peak = indx_max_095_peak [0]
                    sweepData = sweepData[0:indx_max_095_peak]
                    time_secs = time_secs[0:indx_max_095_peak]
                    time_ms = time_ms[0:indx_max_095_peak]
                except:

                    print('no peak')
            '''
            '''
            plt.figure()
            plt.plot(time_secs, sweepData)
            plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep) + '_Unfitted'))
            plt.close('all')
            '''
            '''
            if (time_secs[-1] - time_secs[0]) < 2.5:
                #This equivalent to 1.215 s but since whole time scale subtracted by 1.2 then test 0.015
                start_time_indx_list = [i for i in range(len(orig_time_secs)) if orig_time_secs[i] >= 1.215]
                start_time = start_time_indx_list[0]
                time_secs = orig_time_secs[start_time:]
                sweepData = orig_sweepData[start_time:]
            '''

            '''
            else:
                time_secs = orig_time_secs
                time_ms = orig_time_ms
            '''

        #print(sweepData)
        # Fit the data
        '''
        if actual_sweep < 11:
            p0 = [500, 1000, 200, 1000, 400]
            #p0 = ([500, 1000, 200, 1000, 400] - min_sw)/ (max_sw - min_sw)
        else:
            p0 = [-500000, -10000000, -20, 200, 5000] #For no extra[ method
            #p0 = ([10000000, 40000, 100, 500, 2000] - min_sw) / (max_sw - min_sw)
            #p0 = ([-10000000, -40000-00, -100, 500, 2000] - min_sw)/ (max_sw - min_sw)
            #print(p0)
        '''



        # Doing informed fitting now
        #if actual_sweep < 11:
        if sweep_voltage > -80:
            # First Time data been fit, start initial seed
            if rsquare == -1:
                p0 = [500, 200, 200, 1000, 300]
            else:
                if not warning:
                    p0 = params
                else:
                    p0 = [500, 200, 200, 1000, 300]
            # p0 = ([500, 1000, 200, 1000, 400] - min_sw)/ (max_sw - min_sw)
        else:
            if analyse_neg == 2:
                p0 = [-500, -1000, -20, 20, 300]
            else:
                if not warning:
                    p0 = params
                else:
                    p0 = [-500, -1000, -20, 20, 300]

                    #print('modelling data')
        try:
            warnings.filterwarnings('ignore')
            # params, cov = optimize.curve_fit(double_exponential, time_ms, sweepData, maxfev=50000)
            params, cov = optimize.curve_fit(double_exponential, time_ms, sweepData, p0, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')
        except:
      #      print('fit failed')
            continue

        # Extract the parameter estimations
        #print('computing model variable')

        # From when not normalising data

        model = double_exponential(time_ms, params[0], params[1], params[2], params[3], params[4])
        #print('model variable computed')
        A = params[0]
        B = params[1]
        C = params[2]
        tau1 = params[3]
        tau2 = params[4]

        rsquare = 1 - sum((sweepData - model) ** 2) / sum((sweepData - s_tats.mean(sweepData)) ** 2)


        # Produce warnings or refit data if necessary
        fix_rsq = 0
        #if actual_sweep > 12:
        if sweep_voltage < -90:
            if rsquare < rsq_thresh:

                # time_secs = list(time_secs)
                # new_end_time = time_secs.index(0.89*(sweep_length + 1.2))
                # time_secs = np.array(time_secs)
                # print(0.9*(sweep_length + 1.2))
                # print(time_secs[-1])

                ###########  NOTE  ########## This done for non-extrap method
                #end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.9 * (sweep_length + 1.2 - 1.2)]
                end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.9 * (time_secs[-1])]

                ###########  NOTE  ########## This done for extrap method
                #end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.9 * (sweep_length + 1.2)]

                ###########  NOTE  ########## This done for normalisation extrap method
                #end_time_indx_list = [i for i in range(len(unnorm_time_secs)) if unnorm_time_secs[i] >= 0.9 * (sweep_length + 1.2)]

                # print(np.shape(end_time_indx_list))
                #print(end_time_indx_list)
                new_time_secs = time_secs[0:end_time_indx_list[0]]
                sweepData = sweepData[0:end_time_indx_list[0]]
                unnorm_sweepData = sweepData[0:end_time_indx_list[0]]
                new_time_ms = new_time_secs * 1e3

                # Refit the data
                try:

                    params, cov = optimize.curve_fit(double_exponential, new_time_ms, sweepData, params, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')
                except:
                    #print('fit failed')
                    continue

                # When not using normalisation approach

                A = params[0]
                B = params[1]
                C = params[2]
                tau1 = params[3]
                tau2 = params[4]

                model = double_exponential(new_time_ms, params[0], params[1], params[2], params[3], params[4])

                rsquare = 1 - sum((sweepData - model) ** 2) / sum((sweepData - s_tats.mean(sweepData)) ** 2)
                fix_rsq = 1
        else:
            if rsq_thresh > rsquare >= 0.5*rsq_thresh:

                ###########  NOTE  ########## This done for non-extrap method
                #end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.9 * (sweep_length + 1.2 - 1.2)]
                end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.9 * (time_secs[-1])]

                ###########  NOTE  ########## This done for extrap method
                #end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.9 * (sweep_length + 1.2)]

                ###########  NOTE  ########## This done for normalisation extrap method
                #end_time_indx_list = [i for i in range(len(unnorm_time_secs)) if unnorm_time_secs[i] >= 0.9 * (sweep_length + 1.2)]

                # print(np.shape(end_time_indx_list))
                new_time_secs = time_secs[0:end_time_indx_list[0]]
                sweepData = sweepData[0:end_time_indx_list[0]]
                unnorm_sweepData = sweepData[0:end_time_indx_list[0]]
                new_time_ms = new_time_secs * 1e3

                # Refit the data
                try:

                    params, cov = optimize.curve_fit(double_exponential, new_time_ms, sweepData, params, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')
                except:
                    #print('fit failed')
                    continue


                model = double_exponential(new_time_ms, params[0], params[1], params[2], params[3], params[4])
                A = params[0]
                B = params[1]
                C = params[2]
                tau1 = params[3]
                tau2 = params[4]
                rsquare = 1 - sum((sweepData - model) ** 2) / sum((sweepData - s_tats.mean(sweepData)) ** 2)

                fix_rsq = 1

        sigma_params = np.sqrt(np.diagonal(cov))
        A_sigma = sigma_params[0]
        B_sigma = sigma_params[1]
        C_sigma = sigma_params[2]
        tau1_sigma = sigma_params[3]
        tau2_sigma = sigma_params[4]

        alpha = 0.05
        if fix_rsq == 0:
            tval = t.ppf(1-alpha / 2.0, (len(time_secs)-len(params)))
        else:
            tval = t.ppf(1-alpha / 2.0, (len(new_time_secs)-len(params)))

        A_lower_ci = A - (tval * (A_sigma))
        A_upper_ci = A + (tval * (A_sigma))
        B_lower_ci = B - (tval * (B_sigma))
        B_upper_ci = B + (tval * (B_sigma))
        C_lower_ci = C - (tval * (C_sigma))
        C_upper_ci = C + (tval * (C_sigma))
        tau1_lower_ci = tau1 - (tval * (tau1_sigma))
        tau1_upper_ci = tau1 + (tval * (tau1_sigma))
        tau2_lower_ci = tau2 - (tval * (tau2_sigma))
        tau2_upper_ci = tau2 + (tval * (tau2_sigma))


        A_lower_ci = "{:.5f}".format(A_lower_ci)
        A_upper_ci = "{:.5f}".format(A_upper_ci)
        B_lower_ci = "{:.5f}".format(B_lower_ci)
        B_upper_ci = "{:.5f}".format(B_upper_ci)
        tau1_lower_ci = "{:.5f}".format(tau1_lower_ci)
        tau1_upper_ci = "{:.5f}".format(tau1_upper_ci)
        tau2_lower_ci = "{:.5f}".format(tau2_lower_ci)
        tau2_upper_ci = "{:.5f}".format(tau2_upper_ci)
        C_lower_ci = "{:.5f}".format(C_lower_ci)
        C_upper_ci = "{:.5f}".format(C_upper_ci)


        #print('A = '+str(A)+' +/ ('+str(A_upper_ci)+','+str(A_lower_ci)+')')

        if tau1 > tau2:
            tau_slow = tau1
            tau_fast = tau2
            A_slow = A
            A_fast = B

            tau_slow_ci = str('('+str(tau1_lower_ci)+' ,'+str(tau1_upper_ci)+')')
            tau_fast_ci = str('('+str(tau2_lower_ci)+' ,'+str(tau2_upper_ci)+')')
            A_fast_ci = str('(' + str(B_lower_ci) + ' ,' + str(B_upper_ci) + ')')
            A_slow_ci = str('(' + str(A_lower_ci) + ' ,' + str(A_upper_ci) + ')')
            C_ci = str('(' + str(C_lower_ci) + ' ,' + str(C_upper_ci) + ')')

            Af_percent = A_fast/(A_fast + A_slow)
        else:
            tau_slow = tau2
            tau_fast = tau1
            A_slow = B
            A_fast = A

            tau_slow_ci = str('(' + str(tau2_lower_ci) + ' ,' + str(tau2_upper_ci) + ')')
            tau_fast_ci = str('(' + str(tau1_lower_ci) + ' ,' + str(tau1_upper_ci) + ')')
            A_fast_ci = str('(' + str(A_lower_ci) + ' ,' + str(A_upper_ci) + ')')
            A_slow_ci = str('(' + str(B_lower_ci) + ' ,' + str(B_upper_ci) + ')')
            C_ci = str('(' + str(C_lower_ci) + ' ,' + str(C_upper_ci) + ')')

            Af_percent = A_fast / (A_fast + A_slow)

        if summary_sweep_voltage > -80:
            warning = generate_warnings(A_fast, A_slow, tau_fast, tau_slow, actual_sweep, summary_sweep, sweep_length, max(model), rsquare, rsq_thresh, amp_thresh, summary_sweep_voltage, sweep_voltage)
        else:
            warning = generate_neg_summary_warnings(A_fast, A_slow, tau_fast, tau_slow, actual_sweep, summary_sweep, sweep_length, min(model), rsquare, rsq_thresh, amp_thresh, summary_sweep_voltage, sweep_voltage)

        t_weighted = None
        if abs(A + B) > 0.0:
            t_weighted = (A * tau1 + B * tau2) / (A + B)
        if not warning and (actual_sweep == summary_sweep):
            neg50mVTW = t_weighted


        parameter_data[actual_sweep].append(voltage_array[int(sweep / 2)])
        parameter_data[actual_sweep].append(A_slow)
        parameter_data[actual_sweep].append(A_slow_ci)
        parameter_data[actual_sweep].append(A_fast)
        parameter_data[actual_sweep].append(A_fast_ci)
        parameter_data[actual_sweep].append(C)
        parameter_data[actual_sweep].append(C_ci)
        parameter_data[actual_sweep].append(tau_slow)
        parameter_data[actual_sweep].append(tau_slow_ci)
        parameter_data[actual_sweep].append(tau_fast)
        parameter_data[actual_sweep].append(tau_fast_ci)
        parameter_data[actual_sweep].append(t_weighted)
        parameter_data[actual_sweep].append(Af_percent)


        if fix_rsq == 0:
            parameter_data[actual_sweep].append(time_secs[0])
            parameter_data[actual_sweep].append(time_secs[-1])
        else:
            parameter_data[actual_sweep].append(new_time_secs[0])
            parameter_data[actual_sweep].append(new_time_secs[-1])
        parameter_data[actual_sweep].append(rsquare)
        parameter_data[actual_sweep].append(warning)

        if fix_rsq == 0:
            fig1 = plt.figure()
            plt.plot(time_secs, sweepData)
            plt.plot(time_secs, model)
            plt.xlabel('Time (s)')
            plt.ylabel('Current (pA)')
            plt.title(wellID + ' Sweep ' + str(actual_sweep))
            plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '_image')
            with open(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '.pickle',
                      'wb') as fig_file:
                pickle.dump(fig1, fig_file)


            fig_file.close()
            plt.close(fig1)

            fig2 = plt.figure()
            plt.plot(orig_time_secs, orig_sweepData)
            #plt.plot(time_secs, model)
            plt.xlabel('Time (s)')
            plt.ylabel('Current (pA)')
            plt.title('Full Trace '+ wellID + ' Sweep ' + str(actual_sweep))

            plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '_full_trace_image')
            with open(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '_full_trace.pickle',
                      'wb') as fig_file:
                pickle.dump(fig2, fig_file)
            fig_file.close()
            plt.close(fig2)
        else:
            fig1 = plt.figure()
            plt.plot(new_time_secs, sweepData)
            plt.plot(new_time_secs, model)
            plt.xlabel('Time (s)')
            plt.ylabel('Current (pA)')
            plt.title(wellID + ' Sweep ' + str(actual_sweep) + ' Adjust Fit')
            #plt.ion()
            # print(result_plots)
            plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep))+'_image')
            with open(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '.pickle', 'wb') as fig_file:
                pickle.dump(fig1, fig_file)
            fig_file.close()
            plt.close(fig1)

            fig2 = plt.figure()
            plt.plot(orig_time_secs, orig_sweepData)
            # plt.plot(time_secs, model)
            plt.xlabel('Time (s)')
            plt.ylabel('Current (pA)')
            plt.title('Full Trace ' + wellID + ' Sweep ' + str(actual_sweep))

            plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '_full_trace_image')
            with open(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '_full_trace.pickle',
                      'wb') as fig_file:
                pickle.dump(fig2, fig_file)
            fig_file.close()
            plt.close(fig2)

    #print(parameter_data)
    plt.close('all')

    # Post quality control analysis now being performed on slow/fast tau trends and idenitfying outliers
    #parameter_data = post_analysis_qc(voltage_array, parameter_data, result_plots, wellID, 'slow')
    #parameter_data = post_analysis_qc(voltage_array, parameter_data, result_plots, wellID, 'fast')
    [parameter_data, include_summary] = post_analysis_qc(voltage_array, parameter_data, result_plots, wellID, 'weighted', summary_sweep_voltage)
    if include_summary == 0:
        neg50mVTW = 'N/A'


    # Now write the output
    with open(output_file, mode='w') as result_output:
        result_writer = csv.writer(result_output, delimiter=',', lineterminator='\n')
        for row in range(0, total_sweeps+1):
            result_writer.writerow(parameter_data[row])

    #del full_sweepData

    return neg50mVTW
