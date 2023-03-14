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
    return a * x + b


def post_analysis_qc(model, data, voltage_array, warning, wellID, endo_removed):
    include_summary = 1

    model_len = np.shape(model)
    data_len = np.shape(data)

    if model_len[0] % 2 == 0:
        model_midpoint = model_len[0] / 2
        data_midpoint = data_len[0] / 2
    else:
        model_midpoint = np.floor(model_len[0] / 2)
        data_midpoint = np.floor(data_len[0] / 2)

    discrepancy = 0.1 * data[int(data_midpoint)]

    warning_addition = 0
    if not (discrepancy + data[int(data_midpoint)]) >= model[int(model_midpoint)] >= (
            data[int(data_midpoint)] - discrepancy):
        warning_addition = 0
        include_summary = 0
        if warning:
            warning = warning + ' and model midpoint varies too far from the data'
        else:
            # print(wellID + ' midpoint warn')
            warning = 'model midpoint varies too far from the data'

        # Check for endogenous current
    if warning_addition == 0 and model_len[0] >= 4 and endo_removed == 'no':
        final_model_point = data[model_len[0] - 1]
        seclast_model_point = data[model_len[0] - 2]
        thridlast_model_point = data[model_len[0] - 3]
        fourthlast_model_point = data[model_len[0] - 4]

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


        if not 0.005 >= params[0] >= 0:
            include_summary = 0
            warning_addition = 1
            # print(wellID + ' plat')
            if not warning:
                warning = 'plateau not reached in model prediction'
            else:
                warning += ' and plateau not reached in model prediction'


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

        if not 0.005 >= params[0] >= 0:
            include_summary = 0
            warning_addition = 1
            # print(wellID + ' plat'+ str(params[0]))
            if not warning:
                warning = 'plateau not reached in model prediction'
            else:
                warning += ' and plateau not reached in model prediction'
        # print(warning)
    return [warning, include_summary]


# def boltzmann_v05(x, V05, k):
def boltzmann_v05(x, V05, k, top, bottom):
    # return 1/(1+np.exp((V05-x)/k))
    return bottom + ((top - bottom) / (1 + np.exp((V05 - x) / k)))
    # return expit(-((V05-x)/k))


# def boltzmann_therm(x, G0, z):
def boltzmann_therm(x, G0, z, top, bottom):
    '''
    num = G0 - (z * 96485 / 1000*x)
    dom = 8.3145 * 298
    return expit(-(num / dom))
    '''
    # Y=1/(1+exp((deltaG0-z*F/1000*X)/(R*T)))
    return bottom + ((top - bottom) / (1 + np.exp((G0 - (z * 96485 / 1000 * x)) / (8.3145 * 298))))


def V05_analysis(voltage_array, norm_currs, rsq_thresh, returnV05, returnK, pos40mVCD, wellID):
    fit_parameters = np.array(['V05', 'k', 'top', 'bottom', 'RSquared', 'Warning'])


    p0 = [20, 20, 1, 0]
    try:
        params, cov = optimize.curve_fit(boltzmann_v05, voltage_array, norm_currs, p0, maxfev=50000,bounds=([-np.inf, -np.inf, 0, -np.inf], [np.inf, np.inf, 4, np.inf]))

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

    tval = t.ppf(1 - alpha / 2.0, (len(voltage_array) - len(params)))

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
        lower_rsquare = 1 - sum((norm_currs[lower_volt_indx] - model[lower_volt_indx]) ** 2) / sum((norm_currs[lower_volt_indx] - s_tats.mean(norm_currs[lower_volt_indx])) ** 2)

    fit_params_results = np.array([V05, V05_ci, k, k_ci, top, top_ci, bottom, bottom_ci, rsquare])

    V05_ok = 1
    if rsquare < rsq_thresh:
        warning = 'Fit of Whole Data-set Poor'
        # pos40mVCD = 'N/A'
        returnV05 = 'N/A'
        returnK = 'N/A'
        if not -50 <= V05 <= 50:
            V05_ok = 0
            # pos40mVCD = 'N/A'
            warning = 'Fit of Whole Data-set Poor and V05 outside of possible range of values'

    else:

        if not -50 <= V05 <= 50:
            V05_ok = 0
            warning = 'V05 outside of possible range of values'
            returnV05 = 'V05'
            returnK = 'V05'
            # pos40mVCD = 'N/A'
        else:
            returnV05 = V05
            returnK = k

    return [returnV05, returnK, model, rsquare, V05_ok, fit_params_results, warning, V05, k, top, bottom,
            lower_volt_indx, pos40mVCD]


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

    # therm_p0 = [2500, 155, 1, 0]
    v_list = list(voltage_array)
    therm_v_list = [i for i in range(len(v_list)) if v_list[i] != 0]
    therm_voltage_array = voltage_array[therm_v_list]
    therm_norm_currs = norm_currs[therm_v_list]

    if np.shape(therm_norm_currs)[0] < 4:
        return [returnDG, returnz, np.array([]), therm_norm_currs, therm_voltage_array, 'N/A', 'N/A', 'N/A', 'N/A',
                'N/A', 'N/A', 'N/A', pos40mVCD]

    therm_params, therm_cov = optimize.curve_fit(boltzmann_therm, therm_voltage_array, therm_norm_currs, maxfev=5000000, bounds=([-np.inf, -np.inf, 0, -np.inf], [np.inf, np.inf, 4, np.inf]))

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
        therm_lower_rsquare = 1 - sum((therm_norm_currs[lower_volt_indx] - therm_model[lower_volt_indx]) ** 2) / sum((therm_norm_currs[lower_volt_indx] - s_tats.mean(therm_norm_currs[lower_volt_indx])) ** 2)

    therm_param_results = np.array([G0, G0_ci, z, z_ci, therm_top, top_ci, therm_bottom, bottom_ci, therm_rsquare])
    therm_warning = ''

    if therm_rsquare < rsq_thresh:
        returnDG = 'N/A'
        returnz = 'N/A'
        therm_warning = 'poor fit'
    else:

        returnDG = G0
        returnz = z

    return [returnDG, returnz, therm_model, therm_norm_currs, therm_voltage_array, therm_rsquare, therm_param_results,
            therm_warning, G0, z, therm_top, therm_bottom, pos40mVCD]


def ssAct_fit(well_widget, control_widget):
    # Initialise return value
    pos40mVCD = 'N/A'
    returnV05 = 'unset'
    returnDG = 'unset'
    returnK = 'unset'
    returnz = 'unset'

    data = well_widget.sweep_currents
    time_secs = well_widget.sweep_times
    num_sweeps = well_widget.num_sweeps
    total_sweeps = num_sweeps
    wellID = well_widget.wellID
    variant = well_widget.variant

    rsq_thresh = control_widget.rsq_thresh
    summary_sweep_voltage = control_widget.summary_sweep_voltage
    amp_thresh = control_widget.amp_thresh
    cursor_start = control_widget.cursor_start
    cursor_end = control_widget.cursor_end
    sweep_length = cursor_end - cursor_start

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

    # A matrix storing the results of the current densities for all the sweeps in the well
    current_dens_data = []
    current_dens_data.append([])
    current_dens_data[0].append('Voltage (mV)')
    current_dens_data[0].append('Current Density (pA/pF)')

    # create an 13 row result list

    for i in range(1, total_sweeps + 1):
        current_dens_data.append([])

    norm_currs = np.array([])  # array that stores the current densities which is then normalised using the minimum current dens

    for sweep in range(0, num_sweeps):
        if well_widget.sweep_pass_qc_array[sweep] == 0:
            continue
        actual_sweep = sweep + 1

        sweep_voltage = voltage_array[sweep]

        capacitance = well_widget.capacitance_array[sweep]
        sweepData = data[sweep, :]

        sweepData = sweepData[start_time:end_time]


        min_curr_amp = min(sweepData)

        # Current density = minimum current amplitude / capacitance
        current_density = min_curr_amp / capacitance
        current_dens_data[actual_sweep].append(voltage_array[int(sweep / 2)])
        current_dens_data[actual_sweep].append(current_density)

        if actual_sweep == summary_sweep:
            pos40mVCD = current_density

        norm_currs = np.append(norm_currs, min_curr_amp)

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

    orig_norm_currs = norm_currs
    max_normcurr = max(norm_currs)
    max_normcurr = min(norm_currs)
    norm_currs = np.divide(norm_currs, [max_normcurr])

    fit_parameters = np.array(['V05', 'V05 95% CI', 'k', 'k 95% CI', 'top', 'top 95% CI', 'bottom', 'bottom 95% CI', 'RSquared', 'Warning'])

    [returnV05, returnK, model, rsquare, V05_ok, fit_params_results, warning, V05, k, top, bottom, lower_volt_indx,
     pos40mVCD] = V05_analysis(voltage_array, norm_currs, rsq_thresh, returnV05, returnK, pos40mVCD, wellID)

    [warning, include_summary] = post_analysis_qc(model, norm_currs, voltage_array, warning, wellID, 'no')

    if include_summary == 0:
        returnV05 = 'N/A'
        returnK = 'N/A'
    if include_summary == 2:
        norm_currs = orig_norm_currs[0:-1]
        max_curr = min(norm_currs)
        norm_currs = np.divide(norm_currs, [max_curr])
        voltage_array = voltage_array[0:-1]

        [returnV05, returnK, model, rsquare, V05_ok, fit_params_results, warning, V05, k, top, bottom, lower_volt_indx, pos40mVCD] = V05_analysis(voltage_array, norm_currs, rsq_thresh, returnV05, returnK, pos40mVCD, wellID)
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

        [returnDG, returnz, therm_param_results, G0, z, therm_top, therm_bottom] = therm_analysis(V05, k, top, bottom, returnDG, returnz)


        therm_fit_parameters = np.vstack((therm_fit_parameters, therm_param_results))



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


    return [pos40mVCD, returnV05, returnDG, returnK, returnz]
