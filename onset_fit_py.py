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
import math
import pandas as pd

from scipy.stats.distributions import t

def linear_fit(x, a, b):
    return a*x + b

def exponential_curve(x, A, tau, C):
    return (A-C)*np.exp(-x/tau) + C

def exp_curve(x, A, tau, C):
    return A*np.exp(-x/tau) + C

def fit_tau(voltage_array, tau_array, sweep_array, parameter_data, wellID):

    try:
        voltage_array_fit = (voltage_array - min(voltage_array)) / (max(voltage_array) - min(voltage_array))
        tau_array_fit = (tau_array - min(tau_array)) / (max(tau_array) - min(tau_array))
        # p0 = [tau_array_fit[0], 40, tau_array_fit[-1]]
        p0 = [tau_array_fit[0], 5, tau_array_fit[-1]]
        params, cov = optimize.curve_fit(exp_curve, voltage_array_fit, tau_array_fit, p0, maxfev=5000, loss='soft_l1', f_scale=0.1, method='trf')
    except:
        for i in range(0, len(sweep_array)):
            sweep = int(sweep_array[i])
            sweep_data = np.array(parameter_data[sweep])
            warning = sweep_data[-1]
            if warning:
                warning += ' and exponential trend unable to be modelled for tau values'
            else:
                warning = 'exponential trend unable to be modelled for tau values'
            #print('fail fit')
            sweep_data = sweep_data.astype((str, 140))
            sweep_data[-1] = warning
            #print(sweep_data)
            parameter_data[sweep] = list(sweep_data)
            #print(parameter_data[sweep])

        return [parameter_data, 'N/A', 'N/A', 'N/A']


    #non_lin_model = np.array(exp_curve(voltage_array, params[0], params[1], params[2], params[3])).astype(float)
    non_lin_model = np.array(exp_curve(voltage_array_fit, params[0], params[1], params[2])).astype(float)
    non_lin_model = non_lin_model * (max(tau_array) - min(tau_array)) + min(tau_array)
    #print(str(params[0]) + ' ' + str(params[1]) + ' ' + str(params[2]))

    rsquare = 1 - sum((tau_array.astype(float) - non_lin_model) ** 2) / sum((tau_array.astype(float) - s_tats.mean(tau_array.astype(float))) ** 2)

    # Warning append
    if rsquare < 0.9:
        include_summary = 0
        for i in range(0, len(sweep_array)):
            sweep = int(sweep_array[i])
            sweep_data = np.array(parameter_data[sweep])
            warning = sweep_data[-1]
            if not warning:
                warning += ' Exponential model fit poor for tau values'
            else:
                warning = 'Exponential model fit poor for tau values'
            # print(warning)
            # print('rsq')
            sweep_data = sweep_data.astype((str, 140))
            sweep_data[-1] = warning
            # print(sweep_data)
            parameter_data[sweep] = list(sweep_data)
            # print(parameter_data[sweep])
            # time.sleep(4)

    rsq_str = '%.4f' % rsquare
    qc_fig_name = wellID + '_postQC_exponential_fit_RSquared_' + str(rsq_str) + '.png'

    ''''
    tau_stdev = s_tats.stdev(tau_array)
    tau_outliers = np.array([])
    volt_outliers = np.array([])
    
    for i in range(0, len(tau_array)):
        if abs(tau_array[i] - non_lin_model[i]) > tau_stdev:
            sweep = int(sweep_array[i])
            sweep_data = np.array(parameter_data[sweep])
            warning = sweep_data[-1]
            if not warning:
                warning = 'tau value a possible outlier.'
            else:
                warning += ' and tau value a possible outlier'

            sweep_data = sweep_data.astype((str, 140))
            sweep_data[-1] = warning
            parameter_data[sweep] = list(sweep_data)
            tau_outliers = np.append(tau_outliers, tau_array[i])
            volt_outliers = np.append(volt_outliers, voltage_array[i])
            print(wellID + ' outlier')
            print(tau_array[i])
            print(parameter_data[sweep])
    '''

    #return [parameter_data, non_lin_model, rsquare, tau_outliers, volt_outliers, qc_fig_name]
    return [parameter_data, non_lin_model, rsquare, qc_fig_name]


def post_analysis_qc(voltage_array, parameter_data, result_plots, wellID, summary_voltage):
# Plot the current densities against their voltages and then extract outliers and flag these sweeps

    #print(parameter_data)
    #print(len(parameter_data))
    #print(type(parameter_data))
    tau_array = np.array([])
    sweep_array = np.array([])
    fit_voltages = np.array([])
    volt_indx = 0
    include_summary = 1

    #print(wellID)
    for i in range(1, len(parameter_data)):
        if len(parameter_data[i]) > 1:
            volt_indx += 1
            sweep_data = np.array(parameter_data[i])
            if sweep_data[-1] and sweep_data[1].astype(float) >= -20:
                #print(sweep_data[-1])
                continue
            tau_array = np.append(tau_array, sweep_data[5])
            sweep_array = np.append(sweep_array, i)
            fit_voltages = np.append(fit_voltages, voltage_array[volt_indx-1])

    voltage_array = fit_voltages

    # NEW FEATURE = ONLY FIT FROM -20 ONWARDS
    volts_of_interest_indx = [i for i in range(0, len(list(voltage_array))) if list(voltage_array)[i] >= -.020]
    volts_warn_indx = [i for i in range(0, len(list(voltage_array))) if list(voltage_array)[i] < -.020]

    voltage_array = voltage_array[volts_of_interest_indx]
    tau_array = tau_array[volts_of_interest_indx]
    tau_array = tau_array.astype(float)


    for k in range(0, len(volts_warn_indx)):
        vw = volts_warn_indx[k]
        sweep = int(sweep_array[vw])
        sweep_data = np.array(parameter_data[sweep])
        warning = sweep_data[-1]
        if not warning:
            warning = 'Voltages less than -20mV not included in post-qc tau fit'
        else:
            warning += ' and voltages less than -20mV not included in post-qc tau fit'

        sweep_data = sweep_data.astype((str, 140))
        sweep_data[-1] = warning
        parameter_data[sweep] = list(sweep_data)

    sweep_array = sweep_array[volts_of_interest_indx]
    if np.shape(tau_array)[0] <= 4:
        include_summary = 1
        #print(wellID)
        #print('too little data')
        return [parameter_data, include_summary]

    prev_tau = tau_array[0]
    success_taus = np.array([tau_array[0]])
    success_v = np.array([voltage_array[0]])
    new_sw_array = np.array([sweep_array[0]])
    fail_tau_indx = np.array([])

    #print(tau_array)
    for t in range(1, np.shape(tau_array)[0]):

        if tau_array[t] > prev_tau:
            success_taus = np.append(success_taus, tau_array[t])
            success_v = np.append(success_v, voltage_array[t])
            new_sw_array = np.append(new_sw_array, sweep_array[t])
            prev_tau = tau_array[t]
        else:
            sweep = int(sweep_array[t])
            sweep_data = np.array(parameter_data[sweep])
            warning = sweep_data[-1]
            if not warning:
                warning = 'Tau value not following increasing trend'
            else:
                warning += ' and tau value not following increasing trend'

            sweep_data = sweep_data.astype((str, 140))
            sweep_data[-1] = warning
            parameter_data[sweep] = list(sweep_data)
            if voltage_array[t] == summary_voltage:
                include_summary = 0

    #print(parameter_data)
    #time.sleep(10)


    # Invert the arrays so that they exhibit order of cartesian plane for fitting purposes
    tau_array = success_taus[::-1]
    voltage_array = success_v[::-1]
    sweep_array = new_sw_array

    if np.shape(tau_array)[0] <= 4:
        #print(wellID)
        #print('inr trend cause too little data')
        return [parameter_data, include_summary]

    ######### NOTE: TRIMMING ALL DATASETS TO ONLY FIT FROM -.02mV so ANDY CAN LOOK AT RSQUARED


    # Outlier analysis for non-normally distributed data:
    # Fit the data, obtain model. Go through each point and determine how far it deviates from the model. Get the model? or data? stdev and if the point more than 3 stdevs from model then is outlier

    #params, cov = optimize.curve_fit(linear_fit, voltage_array, tau_array)
    #lin_model = np.array(linear_fit(voltage_array, params[0], params[1])).astype(float)
    #print(str(params[0]) + ' ' + str(params[1]))

    #p0 = [10, 1, 0]

    [parameter_data, non_lin_model, rsquare, qc_fig_name] = fit_tau(voltage_array, tau_array, sweep_array, parameter_data, wellID)
    if non_lin_model == 'N/A':
        #print(wellID)
        #print('fail to fit')
        return [parameter_data, include_summary]

    # Refit the data
    '''
    if rsquare < .99:
        # trim the arrays so only to fit -20mV to 60mV and flag the other dataset
        #print(voltage_array)
        #print(tau_array)
        #print('fix '+wellID)
        #print(rsquare)

        og_rsquare = rsquare
        og_voltage_array = voltage_array
        og_tau_array = tau_array
        og_non_lin_model = non_lin_model


        fit_voltages = list(fit_voltages)
        indx_interest = [i for i in range(len(fit_voltages)) if fit_voltages[i] >= -.020]
        voltage_array = voltage_array[indx_interest]
        tau_array = tau_array[indx_interest]


        #print(voltage_array)
        #print(tau_array)

        indx_discard = [i for i in range(len(fit_voltages)) if fit_voltages[i] < -.020]
        #print('discarding at indexes:')
        #print(indx_discard)

        # we want a larger data set
        invalid_dataset = 0
        if np.shape(tau_array)[0] <= 4:
            invalid_dataset = 1

        if invalid_dataset == 0:
            fit_work = 0
            try:
                params, cov = optimize.curve_fit(exp_curve, voltage_array, tau_array, maxfev=5000)
                fit_work = 1
            except:
                fit_work = 0

            if fit_work == 1:
                non_lin_model = np.array(exp_curve(voltage_array, params[0], params[1], params[2])).astype(float)
                rsquare = 1 - sum((tau_array.astype(float) - non_lin_model) ** 2) / sum((tau_array.astype(float) - s_tats.mean(non_lin_model)) ** 2)

                if og_rsquare <= rsquare:
                    #non_lin_model = np.array(exp_curve(voltage_array, params[0], params[1], params[2], params[3])).astype(float)

                    for j in range(0, len(indx_discard)):
                        i = indx_discard[j]
                        sweep = int(sweep_array[i])
                        sweep_data = np.array(parameter_data[sweep])
                        warning = sweep_data[-1]
                        if warning:
                            warning += ' and full data-set ot taus produced poor post-QC fit. This sweep was excluded from post-QC outlier analysis'
                        else:
                            warning = 'Full data-set ot taus produced poor post-QC fit. This sweep was excluded from post-QC outlier analysis'
                        # print(warning)
                        # print('rsq')
                        sweep_data = sweep_data.astype((str, 140))
                        sweep_data[-1] = warning
                        # print(sweep_data)
                        parameter_data[sweep] = list(sweep_data)
                        # print(parameter_data[sweep])
                        # time.sleep(4)
                    #print(wellID)
                    #print(parameter_data)
                else:
                    # Use the original array
                    #print('old rsq better')
                    #print('old rsq = ' + str(rsquare))
                    tau_array = og_tau_array
                    voltage_array = og_voltage_array
                    rsquare = og_rsquare
                    non_lin_model = og_non_lin_model
            else:
                #print('fit 2 fail, revert')
                tau_array = og_tau_array
                voltage_array = og_voltage_array
                rsquare = og_rsquare
                non_lin_model = og_non_lin_model
        else:
            #print('data set too small, reverting back to full set')
            tau_array = og_tau_array
            voltage_array = og_voltage_array
            rsquare = og_rsquare
            non_lin_model = og_non_lin_model

        #print(str(rsquare) + ' failed')
        # Now go through and tag each warning with 'exponential trend unable to be modelled for tau values'
    '''

    '''
    if np.shape(tau_outliers)[0] > 0:
        indx_outliers = np.array([])

        for o in range(0, np.shape(tau_outliers)[0]-1):
            indx_outlier = [i for i in range(0, len(tau_array)) if tau_array[i] == tau_outliers[o, ]]
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
            [parameter_data, non_lin_model, rsquare, tau_outliers, volt_outliers, qc_fig_name] = fit_tau(voltage_array, tau_array, sweep_array, parameter_data, wellID)

            if non_lin_model == 'N/A':
                #print(wellID)
                #print('rem outlier fail to fit')
                return [parameter_data, 1]
    '''

    fig = plt.figure()
    plt.plot(voltage_array*1000, tau_array, 'o')
    plt.plot(voltage_array*1000, non_lin_model)
    #plt.plot(volt_outliers*1000, tau_outliers, 'ro')
    plt.xlabel('Voltage (mV)')
    plt.ylabel('Tau (ms)')
    plt.savefig(os.path.join(result_plots, wellID, qc_fig_name))
    plt.close(fig)
    return [parameter_data, include_summary]

def adjust_fit(time_secs, sweepData, p0, pr, numpy_pandas):
    if numpy_pandas == 'numpy':
        end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.75 * (time_secs[-1])]
        new_time_secs = time_secs[0:end_time_indx_list[0]]
        orig_sweepData = sweepData
        sweepData = sweepData[0:end_time_indx_list[0]]
    else:
        end_time_indx_list = [i for i in range(len(time_secs)) if time_secs.iloc[i] >= 0.75 * (time_secs.iloc[-1])]
        new_time_secs = time_secs.iloc[0:end_time_indx_list[0]]
        orig_sweepData = sweepData
        sweepData = sweepData.iloc[0:end_time_indx_list[0]]



    try:
        warnings.filterwarnings('ignore')
        params, cov = optimize.curve_fit(exponential_curve, new_time_secs * 1e3, sweepData, p0, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')

        if numpy_pandas == 'numpy':
            if new_time_secs[-1] <= (new_time_secs[0]+0.02):
                return [time_secs, orig_sweepData, 'N/A', -1, 'N/A', 'N/A']
        else:
            if new_time_secs.iloc[-1] <= (new_time_secs.iloc[0]+0.02):
                return [time_secs, orig_sweepData, 'N/A', -1, 'N/A', 'N/A']

    except:
        #if np.shape(np.array(time_secs))[0] <= 5:
        #print('except')
        #print(sweepData)
        return [time_secs, orig_sweepData, 'N/A', -1, 'N/A', 'N/A']

    model = exponential_curve(new_time_secs * 1e3, params[0], params[1], params[2])

    rsquare = 1 - sum((sweepData - model) ** 2) / sum((sweepData - s_tats.mean(sweepData)) ** 2)

    return [new_time_secs, sweepData, params, rsquare, model, cov]


def onset_fit_py(input_file, output_file, wellID, result_plots, num_sweeps, variant, rsq_thresh, summary_sweep_voltage, total_sweeps):
    # Initialise return value



    summary_tau = 'N/A'
    summary_current = 'N/A'

    numpy_pandas = 'pandas'

    #print(summary_sweep_voltage)


    if numpy_pandas == 'numpy':
        data = []
        with open(input_file) as csvfile:
            read = csv.reader(csvfile)
            for row in read:
                data.append(row)

        data = np.array(data)

        time_us = data[1:, 0]
        time_us = time_us.astype(np.float)

        origorig_time_secs = time_us *1e-6
        time_secs = time_us*1e-6
        time_secs_list = list(time_secs)
        #time_indx_list = [i for i in range(len(time_secs_list)) if 1.115 >= time_secs_list[i] >= 1.0323]
        #print('USING OLD PROTOCOL TIME REGION')
        #time_indx_list = [i for i in range(len(time_secs_list)) if 1.6165 >= time_secs_list[i] >= 1.535]
        time_indx_list = [i for i in range(len(time_secs_list)) if 1.22 >= time_secs_list[i] >= 1.175] #THIS NEW PROTOCOL TIME REGION

        #neg_time_indx_list = [i for i in range(len(time_secs_list)) if 1.20 >= time_secs_list[i] >= 1.175]
        neg_time_indx_list = [i for i in range(len(time_secs_list)) if 1.20 >= time_secs_list[i] >= 1.175] #THIS NEW PROTOCOL TIME REGION
        #neg_time_indx_list = [i for i in range(len(time_secs_list)) if 1.59 >= time_secs_list[i] >= 1.535]  # THIS OLD PROTOCOL TIME REGION

        time_secs = np.array(time_secs[time_indx_list]).astype(float)
        neg_time_secs = np.array(origorig_time_secs[neg_time_indx_list]).astype(float)
        orig_time_secs = time_secs
        neg_orig_time_secs = neg_time_secs

        sweepNumArray = data[0, 1:]

        dataArray = data[1:, 1:]
        dataArray = dataArray.astype(np.float)
        #print(time_secs)
        #print(sweepNumArray)

        # Get the median voltage for the time periods specified for each sweep and store in an array
        # Then use this array to calculate the summary sweep
        voltage_array = np.array([])
        for v in range(0, 2*num_sweeps, 2):
            v_reading = np.array(dataArray[time_indx_list, v]).astype(float)
            #print(v_reading)
            #sweep_voltage = np.round(np.mean(v_reading))
            sweep_voltage = np.median(v_reading)
            voltage_array = np.append(voltage_array, sweep_voltage)


        #voltage_array = voltage_array * 1e3
        #print(time_indx_list[0])
        #print(voltage_array)
        #print(summary_sweep_voltage)
        summary_sweep_voltage = summary_sweep_voltage*1e-3
        try:
            summary_sweep_index = list(voltage_array).index(summary_sweep_voltage)
            #print(summary_sweep_index)
            summary_sweep = 'N/A'
            if summary_sweep_index:
                summary_sweep = sweepNumArray[2*summary_sweep_index]
                summary_sweep = summary_sweep.split('_')
                summary_sweep = int(summary_sweep[1])
        except:
            summary_sweep = 'N/A'
        #print(summary_sweep)
    else:
        #pandas
        data = pd.read_csv(input_file, sep=',', low_memory=False, header=None)

        time_us = data.iloc[1:, 0].astype(float)
        origorig_time_secs = time_us * 1e-6
        time_secs = origorig_time_secs
        time_indx_list = [i for i in range(len(time_secs)) if 1.22 >= time_secs.iloc[i] >= 1.175]
        neg_time_indx_list = [i for i in range(len(time_secs)) if 1.20 >= time_secs.iloc[i] >= 1.175]

        time_secs = time_secs.iloc[time_indx_list].astype(float)
        neg_time_secs = origorig_time_secs.iloc[neg_time_indx_list].astype(float)
        orig_time_secs = time_secs
        neg_orig_time_secs = neg_time_secs

        sweepNumArray = data.iloc[0, 1:]

        dataArray = data.iloc[1:, 1:].astype(np.float)

        # print(time_secs)
        # print(sweepNumArray)

        # Get the median voltage for the time periods specified for each sweep and store in an array
        # Then use this array to calculate the summary sweep
        voltage_array = np.array([])
        for v in range(0, 2 * num_sweeps, 2):
            v_reading = np.array(dataArray.iloc[time_indx_list, v]).astype(float)
            # print(v_reading)
            # sweep_voltage = np.round(np.mean(v_reading))
            sweep_voltage = np.median(v_reading)
            voltage_array = np.append(voltage_array, sweep_voltage)

        # voltage_array = voltage_array * 1e3
        # print(time_indx_list[0])
        # print(voltage_array)
        # print(summary_sweep_voltage)
        summary_sweep_voltage = summary_sweep_voltage * 1e-3
        try:
            summary_sweep_index = list(voltage_array).index(summary_sweep_voltage)
            # print(summary_sweep_index)
            summary_sweep = 'N/A'
            if summary_sweep_index:
                summary_sweep = sweepNumArray[2 * summary_sweep_index]
                summary_sweep = summary_sweep.split('_')
                summary_sweep = int(summary_sweep[1])
        except:
            summary_sweep = 'N/A'




    parameter_data = []
    parameter_data.append([])
    parameter_data[0].append('SweepNum')
    parameter_data[0].append('Voltage (mV)')
    parameter_data[0].append('Peak Current (pA)')
    parameter_data[0].append('A (pA)')
    parameter_data[0].append('A 95% CI')
    parameter_data[0].append('tau (ms)')
    parameter_data[0].append('tau 95% CI')
    parameter_data[0].append('C (pA)')
    parameter_data[0].append('C 95% CI')
    parameter_data[0].append('RSquared')
    parameter_data[0].append('Fit Warnings')

    #create a 12 row result list
    for i in range(1, total_sweeps+1):
        parameter_data.append([])
        sw = i
        parameter_data[i].append('Sweep'+str(sw))


    os.mkdir(os.path.join(result_plots, wellID))

    rsquare = -1
    warning = 'N/A'
    final_voltage_array = np.array([])
    for sweep in range(1, (2 * num_sweeps), 2):

        if numpy_pandas == 'numpy':
            actual_sweep = sweepNumArray[sweep]
            actual_sweep = actual_sweep.split('_')
            actual_sweep = int(actual_sweep[1])

            sweepData = dataArray[:, sweep]
            # sweep_voltage = voltage_array[sweep]

            sweepData = sweepData * 1e12
        else:
            actual_sweep = sweepNumArray.iloc[sweep]
            actual_sweep = actual_sweep.split('_')
            actual_sweep = int(actual_sweep[1])

            sweepData = dataArray.iloc[:, sweep]
            # sweep_voltage = voltage_array[sweep]

            sweepData = sweepData * 1e12

        '''
        plt.plot(origorig_time_secs, sweepData)
        plt.title('full trace')
        plt.show()
        '''

        if actual_sweep < 6:
            if numpy_pandas == 'numpy':
                sweepData = sweepData[neg_time_indx_list]
            else:
                sweepData = sweepData.iloc[neg_time_indx_list]
            time_secs = neg_orig_time_secs
            plot_orig_time_secs = time_secs
            plot_orig_time_secs = plot_orig_time_secs - 1.17 #new protocol
            #print('subtracting old voltage duration for extrapolation')
            #plot_orig_time_secs = plot_orig_time_secs - 1.53
            plot_orig_sweepData = sweepData
        else:
            if numpy_pandas == 'numpy':
                sweepData = sweepData[time_indx_list]
            else:
                sweepData = sweepData.iloc[time_indx_list]
            time_secs = orig_time_secs
            plot_orig_time_secs = time_secs
            plot_orig_time_secs = plot_orig_time_secs - 1.17 #new protocol
            #print('subtracting old voltage duration for extrapolation')
            #plot_orig_time_secs = plot_orig_time_secs - 1.53
            plot_orig_sweepData = sweepData
        '''
        sweepData = sweepData[time_indx_list]
        time_secs = orig_time_secs
        '''
        '''
        plt.plot(time_secs, sweepData)
        plt.title('voltage pulse trace')
        plt.show()
        '''
        '''
        peak_current = max(sweepData)
        peak_time_indx = list(sweepData).index(peak_current)
        sweepData = sweepData[peak_time_indx:]
        time_secs = time_secs[peak_time_indx:]
        '''

        '''
        if actual_sweep == summary_sweep:
            if max(sweepData) > 4000:
                print('actual sweep fail 4n check')
                continue
        '''
        peak_current = max(sweepData)
        #Trimming current values larger than 500pA as any current readings larger than this are likely noise

        if numpy_pandas == 'numpy':
            sweep_list = list(sweepData)
            currents_of_interest_indx = [i for i in range(0, len(sweep_list)) if 0 <= sweep_list[i] <= 500]

            #currents_of_interest_indx = [i for i in range(0, len(sweep_list)) if sweep_list[i] <= (500+min(sweepData))]
            #currents_of_interest_indx = [i for i in range(0, len(sweep_list)) if sweep_list[i] <= 2000]
            #print(currents_of_interest_indx)
            if len(currents_of_interest_indx) > 20:
                sweepData = sweepData[currents_of_interest_indx]
                time_secs = time_secs[currents_of_interest_indx]
            else:
                #print(wellID + ' ' + str(actual_sweep))
                #print(len(currents_of_interest_indx))
                continue
        else:
            currents_of_interest_indx = [i for i in range(0, len(sweepData)) if 0 <= sweepData.iloc[i] <= 500]

            if len(currents_of_interest_indx) > 20:
                sweepData = sweepData.iloc[currents_of_interest_indx]
                time_secs = time_secs.iloc[currents_of_interest_indx]
            else:
                continue

        # 1.17 the time when voltage pulse starts so this is the time = 0 point
        #time0 = time_secs[0]
        time_secs = time_secs - 1.17 #new protocol
        #print('subtracting old protocol time duration for extrapolation')
        #time_secs = time_secs - 1.53

        #p0 = [500, 2, 200]

        #Informed fitting
        if rsquare == -1:
            if actual_sweep <= 4:
                #p0 = [1000, 1.5, 200]
                p0 = [500, 1.5, 200]
            elif 5 <= actual_sweep <= 6:
                #p0 = [1000, 5, 200]
                p0 = [500, 5, 200]
            elif 7 <= actual_sweep <= 9:
                #p0 = [1000, 10, 200]
                p0 = [500, 10, 200]
            else:
                #p0 = [1000, 20, 200]
                p0 = [500, 20, 200]
        else:
            if not warning:
                p0 = params
            else:
                if actual_sweep <= 4:
                    #p0 = [1000, 1.5, 200]
                    p0 = [500, 1.5, 200]
                elif 5 <= actual_sweep <= 6:
                    #p0 = [1000, 5, 200]
                    p0 = [500, 5, 200]
                elif 7 <= actual_sweep <= 9:
                    #p0 = [1000, 10, 200]
                    p0 = [500, 10, 200]
                else:
                    #p0 = [1000, 20, 200]
                    p0 = [500, 20, 200]


        try:
            warnings.filterwarnings('ignore')
            params, cov = optimize.curve_fit(exponential_curve, time_secs*1e3, sweepData, p0, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')
        except:
            #if np.shape(np.array(time_secs))[0] <= 4:
            continue

        A = params[0]
        tau = params[1]
        C = params[2]
        model = exponential_curve(time_secs*1e3, params[0], params[1], params[2])

        rsquare = 1 - sum((sweepData - model) ** 2) / sum((sweepData - s_tats.mean(sweepData)) ** 2)


        #trim the capacitive artefact from the current if the fit was poor

        fix_artefact = 0

        # Trim data off the end of the current if the removal of the artifact didn't succeed
        fix_rsq = 0
        adj_count = 0

        adj_max = 4
        prev_sweepData = sweepData
        prev_time_secs = time_secs
        prev_params = params
        prev_rsquare = rsquare
        prev_model = model
        prev_cov = cov
        pr = 0
        if wellID == 'K02' and actual_sweep == 6:
            pr = 1
        while 1:

            #print(wellID + ' ' + str(actual_sweep))
            if adj_count == adj_max:
                #model = exp_curve(new_time_secs*1e3, A, tau, C)
                break
            if rsquare < rsq_thresh:
                fix_rsq = 1
                if adj_count == 0:
                    if fix_artefact == 1:
                        [new_time_secs, sweepData, params, rsquare, model, cov] = adjust_fit(new_time_secs, sweepData, p0, pr, numpy_pandas)
                    else:
                        [new_time_secs, sweepData, params, rsquare, model, cov] = adjust_fit(time_secs, sweepData, p0, pr, numpy_pandas)
                    A = params[0]
                    tau = params[1]
                    C = params[2]
                    #p0 = params
                else:
                    prev_sweepData = sweepData
                    prev_time_secs = new_time_secs
                    prev_params = params
                    prev_rsquare = rsquare
                    prev_model = model
                    prev_cov = cov

                    [new_time_secs, sweepData, params, rsquare, model, cov] = adjust_fit(new_time_secs, sweepData, p0, pr, numpy_pandas)
                    '''
                    except:
                        print('FAILURE')
                        print(new_time_secs)
                        print(sweepData)
                        print(p0)
                        print(pr)
                    '''
                    A = params[0]
                    tau = params[1]
                    C = params[2]
                    #p0 = params
                if params == 'N/A':
                    if adj_count == 0:
                        #print('first failure, revert to previous one')
                        sweepData = prev_sweepData
                        time_secs = prev_time_secs
                        model = prev_model
                        params = prev_params
                        rsquare = prev_rsquare
                        cov = prev_cov
                        fix_rsq = 0
                        A = params[0]
                        tau = params[1]
                        C = params[2]
                    else:
                        sweepData = prev_sweepData
                        new_time_secs = prev_time_secs
                        params = prev_params
                        rsquare = prev_rsquare
                        model = prev_model
                        cov = prev_cov
                        A = params[0]
                        tau = params[1]
                        C = params[2]
                        #model = exponential_curve(new_time_secs*1e3, params[0], params[1], params[2])
                    break

                adj_count += 1
            else:
                #if adj_count != 0:
                    #model = exp_curve(new_time_secs*1e3, A, tau, C)
                break

        warning = ''
        if numpy_pandas == 'numpy':
            duration = time_secs[-1]-time_secs[0]
        else:
            duration = time_secs.iloc[-1] - time_secs.iloc[0]
        if rsquare < rsq_thresh:
            warning = 'Poor Fit'
            #try:
            if tau < 0:
                warning = 'Poor Fit and Tau less than 0'
            else:

                if tau*1e-3 > (duration):
                    warning = 'Poor Fit and Tau has value greater than sweep duration'


        else:
            if tau < 0:
                warning = 'Tau less than 0'
            else:
                if tau*1e-3 > (duration):
                    warning = 'Tau has value greater than sweep duration'
                else:
                    if actual_sweep == summary_sweep:
                    #if actual_sweep == 10:
                        #print('warning manually enetered value for summary sweep')
                        summary_tau = tau
                        summary_current = peak_current

        if fix_rsq == 1 and fix_artefact == 0:
            fig1 = plt.figure()
            plt.plot(new_time_secs, sweepData)
            plt.plot(new_time_secs, model)
            plt.xlabel('Time (s)')
            plt.ylabel('Current (pA)')
            plt.title(wellID + ' Sweep ' + str(actual_sweep) + ' Adjusted Fit')
            # print(result_plots)
            plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep))+'_image')
            with open(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '.pickle', 'wb') as fig_file:
                pickle.dump(fig1, fig_file)
            fig_file.close()
            plt.close(fig1)


        elif fix_artefact == 1 and fix_rsq == 0:
            fig1 = plt.figure()
            plt.plot(new_time_secs, sweepData)
            plt.plot(new_time_secs, model)
            plt.xlabel('Time (s)')
            plt.ylabel('Current (pA)')
            plt.title(wellID + ' Sweep ' + str(actual_sweep) + ' Trim Additional Artefact')
            # print(result_plots)
            plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep))+'_image')
            with open(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '.pickle', 'wb') as fig_file:
                pickle.dump(fig1, fig_file)
            fig_file.close()
            plt.close(fig1)

        elif fix_rsq == 1 and fix_artefact == 1:
            fig1 = plt.figure()
            plt.plot(new_time_secs, sweepData)
            plt.plot(new_time_secs, model)
            plt.xlabel('Time (s)')
            plt.ylabel('Current (pA)')
            plt.title(wellID + ' Sweep ' + str(actual_sweep) + ' Trim Additional Artefact and Adjusted Fit')
            # print(result_plots)
            plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep))+'_image')
            with open(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '.pickle', 'wb') as fig_file:
                pickle.dump(fig1, fig_file)

            fig_file.close()
            plt.close(fig1)
        elif fix_artefact == 0 and fix_rsq == 0:
            fig1 = plt.figure()
            plt.plot(time_secs, sweepData)
            plt.plot(time_secs, model)
            plt.xlabel('Time (s)')
            plt.ylabel('Current (pA)')
            plt.title(wellID + ' Sweep ' + str(actual_sweep))
            # print(result_plots)
            plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep))+'_image')
            with open(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '.pickle', 'wb') as fig_file:
                pickle.dump(fig1, fig_file)

            fig_file.close()
            plt.close(fig1)

        fig2 = plt.figure()
        plt.plot(plot_orig_time_secs, plot_orig_sweepData)
        plt.xlabel('Time (s)')
        plt.ylabel('Current (pA)')
        plt.title('Full Trace ' + wellID + ' Sweep ' + str(actual_sweep))
        # print(result_plots)
        plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '_full_trace_image')
        with open(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '_full_trace.pickle',
                  'wb') as fig_file:
            pickle.dump(fig2, fig_file)
        fig_file.close()
        plt.close(fig2)

        sigma_params = np.sqrt(np.diagonal(cov))
        A_sigma = sigma_params[0]
        tau_sigma = sigma_params[1]
        C_sigma = sigma_params[2]

        alpha = 0.05
        if fix_rsq == 0:
            tval = t.ppf(1 - alpha / 2.0, (len(time_secs)-len(params)))
        else:
            tval = t.ppf(1 - alpha / 2.0, (len(new_time_secs) - len(params)))

        if A_sigma == 0:
            A_sigma = math.inf
        if tau_sigma == 0:
            tau_sigma = math.inf
        if C_sigma == 0:
            C_sigma = math.inf
        A_lower_ci = A - (tval * (A_sigma))
        A_upper_ci = A + (tval * (A_sigma))
        C_lower_ci = C - (tval * (C_sigma))
        C_upper_ci = C + (tval * (C_sigma))
        tau_lower_ci = tau - (tval * (tau_sigma))
        tau_upper_ci = tau + (tval * (tau_sigma))

        A_lower_ci = "{:.5f}".format(A_lower_ci)
        A_upper_ci = "{:.5f}".format(A_upper_ci)
        tau_lower_ci = "{:.5f}".format(tau_lower_ci)
        tau_upper_ci = "{:.5f}".format(tau_upper_ci)
        C_lower_ci = "{:.5f}".format(C_lower_ci)
        C_upper_ci = "{:.5f}".format(C_upper_ci)

        A_ci = str('(' + str(A_lower_ci) + ' ,' + str(A_upper_ci) + ')')
        C_ci = str('(' + str(C_lower_ci) + ' ,' + str(C_upper_ci) + ')')
        tau_ci = str('(' + str(tau_lower_ci) + ' ,' + str(tau_upper_ci) + ')')

        parameter_data[actual_sweep].append(1000*voltage_array[int(sweep/2)])
        parameter_data[actual_sweep].append(peak_current)
        parameter_data[actual_sweep].append(A)
        parameter_data[actual_sweep].append(A_ci)
        parameter_data[actual_sweep].append(tau)
        parameter_data[actual_sweep].append(tau_ci)
        parameter_data[actual_sweep].append(C)
        parameter_data[actual_sweep].append(C_ci)
        parameter_data[actual_sweep].append(rsquare)
        parameter_data[actual_sweep].append(warning)

        final_voltage_array = np.append(final_voltage_array, voltage_array[int(sweep/2)])

    #print(final_voltage_array)
    [parameter_data, include_summary] = post_analysis_qc(final_voltage_array, parameter_data, result_plots, wellID, summary_sweep_voltage)
    if include_summary == 0: #All data now bein returned for now to increase n number and up to user to filter summary results
        summary_tau = 'N/A'
        summary_current = 'N/A'

    # Now write the output
    with open(output_file, mode='w') as result_output:
        result_writer = csv.writer(result_output, delimiter=',', lineterminator='\n', dialect='excel')
        for row in range(0, total_sweeps+1):
            result_writer.writerow(parameter_data[row])

    plt.close('all')
    return [summary_tau, summary_current]