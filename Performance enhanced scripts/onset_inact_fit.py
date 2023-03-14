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
    return a * x + b


def exponential_curve(x, A, tau, C):
    return (A - C) * np.exp(-x / tau) + C


def exp_curve(x, A, tau, C):
    return A * np.exp(-x / tau) + C


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

            sweep_data = sweep_data.astype((str, 140))
            sweep_data[-1] = warning

            parameter_data[sweep] = list(sweep_data)


        return [parameter_data, 'N/A', 'N/A', 'N/A']

    non_lin_model = np.array(exp_curve(voltage_array_fit, params[0], params[1], params[2])).astype(float)
    non_lin_model = non_lin_model * (max(tau_array) - min(tau_array)) + min(tau_array)


    rsquare = 1 - sum((tau_array.astype(float) - non_lin_model) ** 2) / sum(
        (tau_array.astype(float) - s_tats.mean(tau_array.astype(float))) ** 2)

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

            sweep_data = sweep_data.astype((str, 140))
            sweep_data[-1] = warning

            parameter_data[sweep] = list(sweep_data)


    rsq_str = '%.4f' % rsquare
    qc_fig_name = wellID + '_postQC_exponential_fit_RSquared_' + str(rsq_str) + '.png'


    return [parameter_data, non_lin_model, rsquare, qc_fig_name]


def post_analysis_qc(voltage_array, parameter_data, wellID, summary_voltage):
    # Plot the current densities against their voltages and then extract outliers and flag these sweeps

    tau_array = np.array([])
    sweep_array = np.array([])
    fit_voltages = np.array([])
    volt_indx = 0
    include_summary = 1

    for i in range(1, len(parameter_data)):
        if len(parameter_data[i]) > 1:
            volt_indx += 1
            sweep_data = np.array(parameter_data[i])
            if sweep_data[-1] and sweep_data[1].astype(float) >= -20:
                # print(sweep_data[-1])
                continue
            tau_array = np.append(tau_array, sweep_data[5])
            sweep_array = np.append(sweep_array, i)
            fit_voltages = np.append(fit_voltages, voltage_array[volt_indx - 1])

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
        return [parameter_data, include_summary]

    prev_tau = tau_array[0]
    success_taus = np.array([tau_array[0]])
    success_v = np.array([voltage_array[0]])
    new_sw_array = np.array([sweep_array[0]])
    fail_tau_indx = np.array([])

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


    # Invert the arrays so that they exhibit order of cartesian plane for fitting purposes
    tau_array = success_taus[::-1]
    voltage_array = success_v[::-1]
    sweep_array = new_sw_array

    if np.shape(tau_array)[0] <= 4:
        return [parameter_data, include_summary]



    [parameter_data, non_lin_model, rsquare, qc_fig_name] = fit_tau(voltage_array, tau_array, sweep_array, parameter_data, wellID)
    if non_lin_model == 'N/A':

        return [parameter_data, include_summary]


    return [parameter_data, include_summary]


def adjust_fit(time_secs, sweepData, p0, pr):
    orig_sweepData = sweepData
    try:
        print(0.75*time_secs[-1])
        print(time_secs[-1])
        end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 0.75 * (time_secs[-1])]
        new_time_secs = time_secs[0:end_time_indx_list[0]]

        sweepData = sweepData[0:end_time_indx_list[0]]

        warnings.filterwarnings('ignore')
        params, cov = optimize.curve_fit(exponential_curve, new_time_secs * 1e3, sweepData, p0, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')

        if new_time_secs[-1] <= (new_time_secs[0] + 0.02):
            return [time_secs, orig_sweepData, 'N/A', -1, 'N/A', 'N/A']


    except:

        return [time_secs, orig_sweepData, 'N/A', -1, 'N/A', 'N/A']

    model = exponential_curve(new_time_secs * 1e3, params[0], params[1], params[2])

    rsquare = 1 - sum((sweepData - model) ** 2) / sum((sweepData - s_tats.mean(sweepData)) ** 2)

    return [new_time_secs, sweepData, params, rsquare, model, cov]


def onset_inact_fit(well_widget, control_widget):
    # Initialise return value

    summary_tau = 'N/A'
    summary_current = 'N/A'

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

    neg_volt_cursor_start = control_widget.neg_volt_cursor_start
    neg_volt_cursor_end = control_widget.neg_volt_cursor_end


    time_indx_list = [i for i in range(len(time_secs)) if cursor_end >= time_secs[i] >= cursor_start]
    neg_time_indx_list = [i for i in range(len(time_secs)) if neg_volt_cursor_end >= time_secs[i] >= neg_volt_cursor_start]

    orig_time_secs = time_secs
    time_secs = time_secs[time_indx_list[0]: time_indx_list[-1]+1]
    time_secs = np.subtract(np.array(time_secs), time_secs[0])
    orig_time_ms = orig_time_secs * 1 * (10 ** 3)

    neg_time_secs = orig_time_secs[neg_time_indx_list[0]:neg_time_indx_list[-1]+1]
    neg_orig_time_secs = neg_time_secs
    orig_time_secs = time_secs

    # Extract the names of the actual sweeps

    voltage_array = np.arange(60, -60, -10)
    sweepNumArray = np.arange(1, num_sweeps + 1, 1)

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
    parameter_data[0].append('Peak Current (pA)')
    parameter_data[0].append('A (pA)')
    parameter_data[0].append('A 95% CI')
    parameter_data[0].append('tau (ms)')
    parameter_data[0].append('tau 95% CI')
    parameter_data[0].append('C (pA)')
    parameter_data[0].append('C 95% CI')
    parameter_data[0].append('RSquared')
    parameter_data[0].append('Fit Warnings')

    # create a 12 row result list
    for i in range(1, total_sweeps + 1):
        parameter_data.append([])
        sw = i
        parameter_data[i].append('Sweep' + str(sw))

    rsquare = -1
    warning = 'N/A'
    final_voltage_array = np.array([])


    for sweep in range(0, num_sweeps):
        if well_widget.sweep_pass_qc_array[sweep] == 0:
            continue
        actual_sweep = sweep + 1

        sweep_voltage = voltage_array[sweep]

        sweepData = data[sweep, :]
        sweepData = sweepData * 1e12



        if actual_sweep < 6:
            sweepData = sweepData[neg_time_indx_list]

            time_secs = neg_orig_time_secs
            plot_orig_time_secs = time_secs
            #plot_orig_time_secs = np.subtract(np.array(plot_orig_time_secs), 1.17)  # new protocol
            plot_orig_sweepData = sweepData
        else:
            sweepData = sweepData[time_indx_list]

            time_secs = orig_time_secs
            plot_orig_time_secs = time_secs
            #plot_orig_time_secs = np.subtract(np.array(plot_orig_time_secs), 1.17)  # new protocol

            plot_orig_sweepData = sweepData

        peak_current = max(sweepData)
        # Trimming current values larger than 500pA as any current readings larger than this are likely noise


        sweep_list = list(sweepData)
        currents_of_interest_indx = [i for i in range(0, len(sweep_list)) if 0 <= sweep_list[i] <= 500]

        if len(currents_of_interest_indx) > 20:
            sweepData = sweepData[currents_of_interest_indx[0]:currents_of_interest_indx[-1]+1]
            time_secs = time_secs[currents_of_interest_indx[0]:currents_of_interest_indx[-1]+1]
        else:
            continue

        # 1.17 the time when voltage pulse starts so this is the time = 0 point
        time_secs = np.subtract(np.array(time_secs), 1.17)  # new protocol


        # Informed fitting
        if rsquare == -1:
            if actual_sweep <= 4:
                p0 = [500, 1.5, 200]
            elif 5 <= actual_sweep <= 6:
                p0 = [500, 5, 200]
            elif 7 <= actual_sweep <= 9:
                p0 = [500, 10, 200]
            else:
                p0 = [500, 20, 200]
        else:
            if not warning:
                p0 = params
            else:
                if actual_sweep <= 4:
                    p0 = [500, 1.5, 200]
                elif 5 <= actual_sweep <= 6:
                    p0 = [500, 5, 200]
                elif 7 <= actual_sweep <= 9:
                    p0 = [500, 10, 200]
                else:
                    p0 = [500, 20, 200]

        try:
            warnings.filterwarnings('ignore')
            params, cov = optimize.curve_fit(exponential_curve, time_secs * 1e3, sweepData, p0, maxfev=50000, loss='soft_l1', f_scale=0.1, method='trf')
        except:
            continue

        A = params[0]
        tau = params[1]
        C = params[2]
        model = exponential_curve(time_secs * 1e3, params[0], params[1], params[2])

        rsquare = 1 - sum((sweepData - model) ** 2) / sum((sweepData - s_tats.mean(sweepData)) ** 2)

        # trim the capacitive artefact from the current if the fit was poor
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

            if adj_count == adj_max:
                break
            if rsquare < rsq_thresh:
                fix_rsq = 1
                if adj_count == 0:
                    if fix_artefact == 1:
                        [new_time_secs, sweepData, params, rsquare, model, cov] = adjust_fit(new_time_secs, sweepData, p0, pr)
                    else:
                        [new_time_secs, sweepData, params, rsquare, model, cov] = adjust_fit(time_secs, sweepData, p0, pr)
                    A = params[0]
                    tau = params[1]
                    C = params[2]
                    # p0 = params
                else:
                    prev_sweepData = sweepData
                    prev_time_secs = new_time_secs
                    prev_params = params
                    prev_rsquare = rsquare
                    prev_model = model
                    prev_cov = cov

                    [new_time_secs, sweepData, params, rsquare, model, cov] = adjust_fit(new_time_secs, sweepData, p0, pr)

                    A = params[0]
                    tau = params[1]
                    C = params[2]
                if params == 'N/A':
                    if adj_count == 0:
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
                    break

                adj_count += 1
            else:
                break

        warning = ''
        duration = time_secs[-1] - time_secs[0]

        if rsquare < rsq_thresh:
            warning = 'Poor Fit'
            # try:
            if tau < 0:
                warning = 'Poor Fit and Tau less than 0'
            else:

                if tau * 1e-3 > (duration):
                    warning = 'Poor Fit and Tau has value greater than sweep duration'


        else:
            if tau < 0:
                warning = 'Tau less than 0'
            else:
                if tau * 1e-3 > (duration):
                    warning = 'Tau has value greater than sweep duration'
                else:
                    if actual_sweep == summary_sweep:
                        # if actual_sweep == 10:
                        # print('warning manually enetered value for summary sweep')
                        summary_tau = tau
                        summary_current = peak_current



        sigma_params = np.sqrt(np.diagonal(cov))
        A_sigma = sigma_params[0]
        tau_sigma = sigma_params[1]
        C_sigma = sigma_params[2]

        alpha = 0.05
        if fix_rsq == 0:
            tval = t.ppf(1 - alpha / 2.0, (len(time_secs) - len(params)))
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

        parameter_data[actual_sweep].append(1000 * voltage_array[int(sweep / 2)])
        parameter_data[actual_sweep].append(peak_current)
        parameter_data[actual_sweep].append(A)
        parameter_data[actual_sweep].append(A_ci)
        parameter_data[actual_sweep].append(tau)
        parameter_data[actual_sweep].append(tau_ci)
        parameter_data[actual_sweep].append(C)
        parameter_data[actual_sweep].append(C_ci)
        parameter_data[actual_sweep].append(rsquare)
        parameter_data[actual_sweep].append(warning)

        final_voltage_array = np.append(final_voltage_array, voltage_array[int(sweep / 2)])

    [parameter_data, include_summary] = post_analysis_qc(final_voltage_array, parameter_data, wellID, summary_sweep_voltage)
    if include_summary == 0:  # All data now bein returned for now to increase n number and up to user to filter summary results
        summary_tau = 'N/A'
        summary_current = 'N/A'


    print([summary_tau, summary_current])
    return [summary_tau, summary_current]