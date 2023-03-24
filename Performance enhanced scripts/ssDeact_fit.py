import itertools

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
import itertools
import multiprocessing

from ssDeact_warnings import generate_warnings
from ssDeact_warnings_neg_summary import generate_neg_summary_warnings


def exp_curve(x, A, B, tau, C):
    # def exp_curve(x, A, tau, C):
    return A * np.exp((x + B) / tau) + C
    # return A*np.exp(x/tau) + C


def fit_taus(tau_array, voltage_array, sweep_array, parameter_data, slow_fast, wellID):
    # p0 = [10, 1, 0]
    try:
        voltage_array_fit = (voltage_array - min(voltage_array)) / (max(voltage_array) - min(voltage_array))
        tau_array_fit = (tau_array - min(tau_array)) / (max(tau_array) - min(tau_array))
        # p0 = [tau_array_fit[0], 40, tau_array_fit[-1]]
        p0 = [tau_array_fit[0], -1 * voltage_array_fit[-1], 40, tau_array_fit[-1]]
        params, cov = optimize.curve_fit(exp_curve, voltage_array_fit, tau_array_fit, p0, maxfev=500000, loss='soft_l1', f_scale=0.1, method='trf')


    except:

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

            sweep_data = sweep_data.astype((str, 300))
            sweep_data[-1] = warning

            parameter_data[sweep] = list(sweep_data)

        return [parameter_data, 'N/A', 'N/A']


    non_lin_model = np.array(exp_curve(voltage_array_fit, params[0], params[1], params[2], params[3]).astype(float))
    non_lin_model = non_lin_model * (max(tau_array) - min(tau_array)) + min(tau_array)


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

            sweep_data = sweep_data.astype((str, 300))
            sweep_data[-1] = warning

            parameter_data[sweep] = list(sweep_data)


    return [parameter_data, non_lin_model, qc_fig_name]

def post_analysis_qc(voltage_array, parameter_data, wellID, slow_fast, summary_voltage):
    # Plot the current densities against their voltages and then extract outliers and flag these sweeps
    #print('hi')
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
                continue
            if 'Rsquare' in sweep_data[-1] or 'current' in sweep_data[-1] or 'negative' in sweep_data[-1] or 'duration' in sweep_data[-1] or 'amplitude' in sweep_data[-1]:
                continue

            if slow_fast == 'fast':

                if float(sweep_data[5]) < float(sweep_data[6]):
                    tau_array = np.append(tau_array, sweep_data[5])
                else:
                    tau_array = np.append(tau_array, sweep_data[6])
                # print('appended '+tau_array[-1])
            elif slow_fast == 'slow':

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
    # print(voltage_array)

    if np.shape(tau_array)[0] <= 4:
        #print(wellID + ' return 1 cos not enough data')

        return [parameter_data, include_summary]

    # Now ensure there is an increasing trend in taus
    prev_tau = tau_array[0]
    success_taus = np.array([tau_array[0]])
    success_v = np.array([voltage_array[0]])
    new_sw_array = np.array([sweep_array[0]])
    fail_tau_indx = np.array([])

    # print(tau_array)
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

    # print(parameter_data)
    # time.sleep(10)
    if np.shape(tau_array)[0] <= 4:
        #print(wellID + ' return 2 cos not enough data')
        include_summary = 1
        return [parameter_data, include_summary]

    # Invert the arrays so that they exhibit order of cartesian plane for fitting purposes
    tau_array = success_taus[::-1]
    voltage_array = success_v[::-1]
    sweep_array = new_sw_array

    # tau_array = 1 / tau_array
    if slow_fast == 'slow':
        tit = 'slow ' + wellID
    elif slow_fast == 'fast':
        tit = 'fast ' + wellID
    elif slow_fast == 'weighted':
        tit = 'weighted ' + wellID


    # Outlier analysis for non-normally distributed data:
    # Fit the data, obtain model. Go through each point and determine how far it deviates from the model. Get the model? or data? stdev and if the point more than 3 stdevs from model then is outlier

    [parameter_data, non_lin_model, qc_fig_name] = fit_taus(tau_array, voltage_array, sweep_array, parameter_data, slow_fast, wellID)
    #if non_lin_model == 'N/A':
        #print('return')
    return [parameter_data, include_summary]



def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m / sd)


def double_exponential(x, A, B, C, tau1, tau2):
    return A * np.exp(-x / tau1) + B * np.exp(-x / tau2) + C


def peak_current_greater_threshold(times, currents, peak_current_parameter, start_time=0.002, end_time=3.0):
    print(peak_current_parameter)
    min_current = min([float(c) for t, c in zip(times, currents) if start_time <= float(t) <= end_time])
    print(min_current)
    return (min_current > peak_current_parameter)


def peak_current_smaller_threshold(times, currents, peak_current_parameter, start_time=0.002, end_time=3.0):
    # print(peak_current_parameter)
    max_current = max([float(c) for t, c in zip(times, currents) if start_time <= float(t) <= end_time])
    # print(max_current)
    return (max_current < peak_current_parameter)



'''
def work(sweep_pass_qc, sweep_voltage, summary_sweep, actual_sweep, sweep_length, sweepData, orig_time_secs, start_time, end_time, summary_sweep_voltage, amp_thresh, rsq_thresh):


    orig_time_ms = orig_time_secs* 1e-3
    #if sweep_pass_qc_array[sweep] == 0:
    if sweep_pass_qc == 0:
        #continue
        return
    #actual_sweep = sweep + 1

    #sweep_voltage = voltage_array[sweep]

    if sweep_voltage == -80 or sweep_voltage == -90:
        # if actual_sweep == 11 or actual_sweep == 12:
        #continue
        return

    global analyse_neg
    # Variables that indicates whether to use previous fit parameters as start point inputs for this fit iteration
    # Dynamic start point initialisation
    # if actual_sweep >= 11:
    if sweep_voltage <= -80:
        # When equal to 0, set to 2 so program knows to seed with initial p0 parameters
        if analyse_neg == 0:
            analyse_neg = 2
        else:
            # When equal to 1 program knows to use previous iterations of params for seeds
            analyse_neg = 1

    #sweepData = data[sweep, :]

    sweepData = sweepData[start_time:end_time]
    orig_sweepData = sweepData

    sweepData = sweepData * 1e12

    if summary_sweep_voltage > -80:
        if sweep_voltage == summary_sweep_voltage:
            if max(sweepData) < amp_thresh:
                #continue
                return
    else:
        if sweep_voltage == summary_sweep_voltage:
            if min(sweepData) > amp_thresh:
                #continue
                return

    # Now check if there is a capacitive spike. If yes then trim time and current data again

    # Use the minimum or maximum, depending on the curve shape, to trim the best

    # if actual_sweep < 11:
    if sweep_voltage > -80:
        max_current = max(sweepData)
        indx_max_current = 2 * (list(sweepData).index(max_current))
        sweepData = sweepData[indx_max_current:]
        time_secs = orig_time_secs[indx_max_current:]
        time_ms = orig_time_ms[indx_max_current:]

        # Early sweeps aren't as receptive to the max point trimming
        # Compare standard deviations of start portion and all data to determine if noise is still present at the start

        if np.shape(time_secs)[0] >= 200:
            overall_std = s_tats.stdev(sweepData)
            start_std = s_tats.stdev(sweepData[0:200])

            if start_std > overall_std:
                trim_extra_time = 200
                sweepData = sweepData[trim_extra_time:]
                time_secs = time_secs[trim_extra_time:]
                time_ms = time_ms[trim_extra_time:]



    else:
        min_current = min(sweepData)
        indx_min_current = 2 * (list(sweepData).index(min_current))

        if sweep_voltage <= -140:
            indx_last_time = [i for i in range(len(orig_time_secs)) if orig_time_secs[i] >= 1]
            indx_last_time = indx_last_time[0]
        else:
            indx_last_time = [i for i in range(len(orig_time_secs)) if orig_time_secs[i] >= 1.5]
            indx_last_time = indx_last_time[0]

        sweepData = sweepData[indx_min_current:indx_last_time]
        time_secs = orig_time_secs[indx_min_current:indx_last_time]
        time_ms = orig_time_ms[indx_min_current:indx_last_time]

    # Doing informed fitting now
    global rsquare
    global params
    if sweep_voltage > -80:
        # First Time data been fit, start initial seed
        if rsquare == -1:
            p0 = [500, 200, 200, 1000, 300]
        else:
            #if not warning:
                #p0 = params
            #else:
            p0 = [500, 200, 200, 1000, 300]
    else:
        if analyse_neg == 2:
            p0 = [-500, -1000, -20, 20, 300]
        else:
            #if not warning:
                #p0 = params
            #else:
            p0 = [-500, -1000, -20, 20, 300]

    try:
        warnings.filterwarnings('ignore')
        params, cov = optimize.curve_fit(double_exponential, time_ms, sweepData, p0, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')
    except:
        #continue
        return

    model = double_exponential(time_ms, params[0], params[1], params[2], params[3], params[4])
    # print('model variable computed')
    A = params[0]
    B = params[1]
    C = params[2]
    tau1 = params[3]
    tau2 = params[4]

    rsquare = 1 - sum((sweepData - model) ** 2) / sum((sweepData - s_tats.mean(sweepData)) ** 2)

    # Produce warnings or refit data if necessary
    fix_rsq = 0
    # if actual_sweep > 12:
    if sweep_voltage < -90:
        if rsquare < rsq_thresh:

            end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.9 * (time_secs[-1])]

            new_time_secs = time_secs[0:end_time_indx_list[0]]
            sweepData = sweepData[0:end_time_indx_list[0]]
            unnorm_sweepData = sweepData[0:end_time_indx_list[0]]
            new_time_ms = new_time_secs * 1e3

            # Refit the data
            try:
                params, cov = optimize.curve_fit(double_exponential, new_time_ms, sweepData, params, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')
            except:
                # print('fit failed')
                #continue
                return

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
        if rsq_thresh > rsquare >= 0.5 * rsq_thresh:

            ###########  NOTE  ########## This done for non-extrap method
            end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.9 * (time_secs[-1])]

            new_time_secs = time_secs[0:end_time_indx_list[0]]
            sweepData = sweepData[0:end_time_indx_list[0]]
            unnorm_sweepData = sweepData[0:end_time_indx_list[0]]
            new_time_ms = new_time_secs * 1e3

            # Refit the data
            try:
                params, cov = optimize.curve_fit(double_exponential, new_time_ms, sweepData, params, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')
            except:
                # print('fit failed')
                #continue
                return

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
        tval = t.ppf(1 - alpha / 2.0, (len(time_secs) - len(params)))
    else:
        tval = t.ppf(1 - alpha / 2.0, (len(new_time_secs) - len(params)))

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

    if tau1 > tau2:
        tau_slow = tau1
        tau_fast = tau2
        A_slow = A
        A_fast = B

        tau_slow_ci = str('(' + str(tau1_lower_ci) + ' ,' + str(tau1_upper_ci) + ')')
        tau_fast_ci = str('(' + str(tau2_lower_ci) + ' ,' + str(tau2_upper_ci) + ')')
        A_fast_ci = str('(' + str(B_lower_ci) + ' ,' + str(B_upper_ci) + ')')
        A_slow_ci = str('(' + str(A_lower_ci) + ' ,' + str(A_upper_ci) + ')')
        C_ci = str('(' + str(C_lower_ci) + ' ,' + str(C_upper_ci) + ')')

        Af_percent = A_fast / (A_fast + A_slow)
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
        warning = generate_neg_summary_warnings(A_fast, A_slow, tau_fast, tau_slow, actual_sweep, summary_sweep, summary_sweep_voltage, sweep_voltage)

    t_weighted = None
    if abs(A + B) > 0.0:
        t_weighted = (A * tau1 + B * tau2) / (A + B)
    if not warning and (actual_sweep == summary_sweep):
        neg50mVTW = t_weighted
    return [params, warning, rsquare, t_weighted]

'''
#def ssDeact_fit(well_widget, control_widget):
def ssDeact_fit(time_secs, data, sweep_pass_qc_array, num_sweeps, wellID, rsq_thresh, summary_sweep_voltage, amp_thresh, cursor_start, cursor_end):
    # Initialise return value

    #print(well_widget.wellID)

    #print(cursor_start)
    neg50mVTW = 'N/A'



    #total_sweeps = num_sweeps
    '''
    data = well_widget.sweep_currents
    time_secs = well_widget.sweep_times
    num_sweeps = well_widget.num_sweeps
    total_sweeps = num_sweeps
    wellID = well_widget.wellID

    rsq_thresh = control_widget.rsq_thresh
    summary_sweep_voltage = control_widget.summary_sweep_voltage
    amp_thresh = control_widget.amp_thresh
    cursor_start = control_widget.cursor_start
    cursor_end = control_widget.cursor_end
    '''
    sweep_length = cursor_end-cursor_start

    start_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= cursor_start]
    start_time = start_time_indx_list[0]
    end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= cursor_end]
    end_time = end_time_indx_list[0]

    time_secs = time_secs[start_time:end_time]
    time_secs = np.subtract(np.array(time_secs), time_secs[0])
    orig_time_secs = time_secs
    orig_time_ms = orig_time_secs * 1 * (10 ** 3)

    # Extract the names of the actual sweeps

    voltage_array = np.arange(20, -160, -10)
    sweepNumArray = np.arange(1, num_sweeps+1, 1)

    try:
        summary_sweep_index = list(voltage_array).index(summary_sweep_voltage)
        summary_sweep = 'N/A'
        if summary_sweep_index:
            summary_sweep = sweepNumArray[summary_sweep_index]
    except:
        summary_sweep = 'N/A'

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

    # create an 18 row result list
    for i in range(1, num_sweeps + 1):
        parameter_data.append([])
        sw = i
        parameter_data[i].append('Sweep' + str(sw))

    # Start at index 1 and iterate every second column so not to analyse voltage columns
    #global rsquare
    rsquare = -1
    #analyse_neg = 0
    warning = 'N/A'

    #global analyse_neg
    analyse_neg = 0


    '''
    num_cpus = int(multiprocessing.cpu_count())
    pool = multiprocessing.Pool(20)

    #sweep_pass_qc, sweep_voltage, summary_sweep, actual_sweep, sweep_length, sweepData, orig_time_secs, start_time, end_time, summary_sweep_voltage, amp_thresh, rsq_thresh

    all_data = pool.starmap(work, zip(well_widget.sweep_pass_qc_array, voltage_array, itertools.repeat(summary_sweep), sweepNumArray,itertools.repeat(sweep_length), data, itertools.repeat(orig_time_secs), itertools.repeat(start_time), itertools.repeat(end_time), itertools.repeat(summary_sweep_voltage), itertools.repeat(amp_thresh), itertools.repeat(rsq_thresh)))

    pool.close()
    pool.join()
    '''

    #print('pool done')


    for sweep in range(0, num_sweeps):
        if sweep_pass_qc_array[sweep] == 0:
            continue
        actual_sweep = sweep+1

        sweep_voltage = voltage_array[sweep]

        if sweep_voltage == -80 or sweep_voltage == -90:
            # if actual_sweep == 11 or actual_sweep == 12:
            continue

        # Variables that indicates whether to use previous fit parameters as start point inputs for this fit iteration
        # Dynamic start point initialisation
        # if actual_sweep >= 11:
        if sweep_voltage <= -80:
            # When equal to 0, set to 2 so program knows to seed with initial p0 parameters
            if analyse_neg == 0:
                analyse_neg = 2
            else:
                # When equal to 1 program knows to use previous iterations of params for seeds
                analyse_neg = 1


        sweepData = data[sweep, :]

        sweepData = sweepData[start_time:end_time]
        orig_sweepData = sweepData

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
        
        #Use the minimum or maximum, depending on the curve shape, to trim the best
        
        # if actual_sweep < 11:
        if sweep_voltage > -80:
            max_current = max(sweepData)
            indx_max_current = 2 * (list(sweepData).index(max_current))
            sweepData = sweepData[indx_max_current:]
            time_secs = orig_time_secs[indx_max_current:]
            time_ms = orig_time_ms[indx_max_current:]

            # Early sweeps aren't as receptive to the max point trimming
            # Compare standard deviations of start portion and all data to determine if noise is still present at the start

            if np.shape(time_secs)[0] >= 200:
                overall_std = s_tats.stdev(sweepData)
                start_std = s_tats.stdev(sweepData[0:200])

                if start_std > overall_std:
                    trim_extra_time = 200
                    sweepData = sweepData[trim_extra_time:]
                    time_secs = time_secs[trim_extra_time:]
                    time_ms = time_ms[trim_extra_time:]



        else:
            min_current = min(sweepData)
            indx_min_current = 2 * (list(sweepData).index(min_current))

            if sweep_voltage <= -140:
                indx_last_time = [i for i in range(len(orig_time_secs)) if orig_time_secs[i] >= 1]
                indx_last_time = indx_last_time[0]
            else:
                indx_last_time = [i for i in range(len(orig_time_secs)) if orig_time_secs[i] >= 1.5]
                indx_last_time = indx_last_time[0]

            sweepData = sweepData[indx_min_current:indx_last_time]
            time_secs = orig_time_secs[indx_min_current:indx_last_time]
            time_ms = orig_time_ms[indx_min_current:indx_last_time]


        # Doing informed fitting now
        if sweep_voltage > -80:
            # First Time data been fit, start initial seed
            if rsquare == -1:
                p0 = [500, 200, 200, 1000, 300]
            else:
                if not warning:
                    p0 = params
                else:
                    p0 = [500, 200, 200, 1000, 300]
        else:
            if analyse_neg == 2:
                p0 = [-500, -1000, -20, 20, 300]
            else:
                if not warning:
                    p0 = params
                else:
                    p0 = [-500, -1000, -20, 20, 300]

        try:
            warnings.filterwarnings('ignore')
            params, cov = optimize.curve_fit(double_exponential, time_ms, sweepData, p0, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')
        except:
            continue


        model = double_exponential(time_ms, params[0], params[1], params[2], params[3], params[4])
        # print('model variable computed')
        A = params[0]
        B = params[1]
        C = params[2]
        tau1 = params[3]
        tau2 = params[4]

        rsquare = 1 - sum((sweepData - model) ** 2) / sum((sweepData - s_tats.mean(sweepData)) ** 2)

        # Produce warnings or refit data if necessary
        fix_rsq = 0
        # if actual_sweep > 12:
        if sweep_voltage < -90:
            if rsquare < rsq_thresh:

                end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.9 * (time_secs[-1])]

                new_time_secs = time_secs[0:end_time_indx_list[0]]
                sweepData = sweepData[0:end_time_indx_list[0]]
                unnorm_sweepData = sweepData[0:end_time_indx_list[0]]
                new_time_ms = new_time_secs * 1e3

                # Refit the data
                try:
                    params, cov = optimize.curve_fit(double_exponential, new_time_ms, sweepData, params, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')
                except:
                    # print('fit failed')
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
            if rsq_thresh > rsquare >= 0.5 * rsq_thresh:

                ###########  NOTE  ########## This done for non-extrap method
                end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.9 * (time_secs[-1])]

                new_time_secs = time_secs[0:end_time_indx_list[0]]
                sweepData = sweepData[0:end_time_indx_list[0]]
                unnorm_sweepData = sweepData[0:end_time_indx_list[0]]
                new_time_ms = new_time_secs * 1e3

                # Refit the data
                try:
                    params, cov = optimize.curve_fit(double_exponential, new_time_ms, sweepData, params, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')
                except:
                    # print('fit failed')
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
            tval = t.ppf(1 - alpha / 2.0, (len(time_secs) - len(params)))
        else:
            tval = t.ppf(1 - alpha / 2.0, (len(new_time_secs) - len(params)))

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

        if tau1 > tau2:
            tau_slow = tau1
            tau_fast = tau2
            A_slow = A
            A_fast = B

            tau_slow_ci = str('(' + str(tau1_lower_ci) + ' ,' + str(tau1_upper_ci) + ')')
            tau_fast_ci = str('(' + str(tau2_lower_ci) + ' ,' + str(tau2_upper_ci) + ')')
            A_fast_ci = str('(' + str(B_lower_ci) + ' ,' + str(B_upper_ci) + ')')
            A_slow_ci = str('(' + str(A_lower_ci) + ' ,' + str(A_upper_ci) + ')')
            C_ci = str('(' + str(C_lower_ci) + ' ,' + str(C_upper_ci) + ')')

            Af_percent = A_fast / (A_fast + A_slow)
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

        print('wellID =', wellID, 'sweep = ', sweep, 'process =', os.getpid())

    # Post quality control analysis now being performed on slow/fast tau trends and idenitfying outliers
    [parameter_data, include_summary] = post_analysis_qc(voltage_array, parameter_data, wellID, 'weighted', summary_sweep_voltage)

    if include_summary == 0:
        neg50mVTW = 'N/A'

    return neg50mVTW
