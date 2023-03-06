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
import pandas as pd

def min_current_greater_threshold(times, currents, peak_current_parameter, start_time=0.002, end_time=3.0):
    min_current = min([float(c) for t,c in zip(times,currents) if start_time <= float(t) <= end_time])
    return (min_current > peak_current_parameter)

def ssDeact_analyse_CD(input_file, wellID, result_plots, num_sweeps, variant, sweep_length, total_sweeps, neg_50_amp_thresh, neg_120_amp_thresh):
    # TO DO:
    # Pass
    # Take peak at -120mv and then 50ms see if it decreased by 50%
    # Negative peak occurs in before 1.15ms (10ms after start trim point)

    # Take CD at 1.26

    numpy_pandas = 'pandas'

    if numpy_pandas == 'numpy':
        data = []
        with open(input_file) as csvfile:
            read = csv.reader(csvfile)
            for row in read:
                data.append(row)

        # Filtering the time data and removing noisy time regions
        # time_us = data[1:, 0]  #np array implementation
        time_us = [row[0] for row in data]
        time_us = time_us[1:]
        # print(time_us)
        # return neg50mVTW
        time_us = np.array(time_us)

        time_us = time_us.astype(np.float)
        # time_us = list(time_us)


        time_secs = time_us * 1e-6
        full_time_secs = time_secs
        time_secs = list(time_secs)
        # start_time = time_secs.index(1.215)
        #print('using old protocol time range')
        start_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 1.20] #new protocol
        #start_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 1.10]
        start_time = start_time_indx_list[0]
        end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= (sweep_length + 1.2)] #new protocol
        #end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= (sweep_length + 1.1)]
        end_time = end_time_indx_list[0]

        # end_time = time_secs.index(sweep_length + 1.2)
        time_secs = time_secs[start_time:end_time]
        time_secs = np.array(time_secs)
        orig_time_secs = time_secs

        orig_time_ms = time_secs * 1e3

        # T=1.2s is when the voltage pulse was applied to the well, and the amplitudes need to be extracted back to this point. i.e. treat this as t=0
        orig_time_secs = orig_time_secs - orig_time_secs[0]
        orig_time_ms = orig_time_ms - orig_time_ms[0]

        # Extract the names of the actual sweeps
        # sweepNumArray = data[0, 1:]    #np array implementation
        # voltage_array = data[1, 1:]    #np array implementation
        sweepNumArray = data[0]
        sweepNumArray = sweepNumArray[1:]
        voltage_array = data[2]
        voltage_array = voltage_array[1:]
        voltage_array = np.array(voltage_array)
        # if summary_sweep_voltage != 52:
        voltage_array = voltage_array[1::2].astype(float)

        # Convert to mV units
        voltage_array = voltage_array * 1e3
    else:
        data = pd.read_csv(input_file, sep=',', low_memory=False, header=None)

        # Filtering the time data and removing noisy time regions
        # time_us = data[1:, 0]  #np array implementation
        time_us = data.iloc[3:, 0].astype(float)

        # time_us = list(time_us)

        time_secs = time_us * 1e-6
        full_time_secs = time_secs

        # start_time = time_secs.index(1.215)
        # print('using old protocol time range')
        start_time_indx_list = [i for i in range(len(time_secs)) if time_secs.iloc[i] >= 1.20]  # new protocol
        # start_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= 1.10]
        start_time = start_time_indx_list[0]
        end_time_indx_list = [i for i in range(len(time_secs)) if time_secs.iloc[i] >= (sweep_length + 1.2)]  # new protocol
        # end_time_indx_list = [i for i in range(len(time_secs)) if time_secs[i] >= (sweep_length + 1.1)]
        end_time = end_time_indx_list[0]

        # end_time = time_secs.index(sweep_length + 1.2)
        time_secs = time_secs.iloc[start_time:end_time]
        orig_time_secs = time_secs

        orig_time_ms = time_secs * 1e3

        # T=1.2s is when the voltage pulse was applied to the well, and the amplitudes need to be extracted back to this point. i.e. treat this as t=0
        #print('before')
        #print(orig_time_secs)
        orig_time_secs = orig_time_secs - orig_time_secs.iloc[0]
        orig_time_ms = orig_time_ms - orig_time_ms.iloc[0]
        #print('after')
        #print(orig_time_secs)
        # Extract the names of the actual sweeps
        # sweepNumArray = data[0, 1:]    #np array implementation
        # voltage_array = data[1, 1:]    #np array implementation
        sweepNumArray = data.iloc[0]
        sweepNumArray = sweepNumArray.iloc[1:]
        voltage_array = data.iloc[2]
        voltage_array = voltage_array.iloc[1:]
        voltage_array = np.array(voltage_array)
        # if summary_sweep_voltage != 52:
        voltage_array = voltage_array[1::2].astype(float)

        # Convert to mV units
        voltage_array = voltage_array * 1e3


    # Start at index 1 and iterate every second column so not to analyse voltage columns
    current_density_neg_50mV = 'N/A'
    current_density_neg_120mV = 'N/A'
    peak_neg_50mV = 'N/A'
    peak_neg_120mV = 'N/A'
    cap_neg_50mV = 'N/A'
    cap_neg_120mV = 'N/A'

    os.mkdir(os.path.join(result_plots, wellID))
    for sweep in range(1, (2*num_sweeps), 2):
        if numpy_pandas == 'numpy':
            actual_sweep = sweepNumArray[sweep]
            actual_sweep = actual_sweep.split('_')
            actual_sweep = int(actual_sweep[1])

            sweep_voltage = voltage_array[int(sweep / 2)]

            sweepData = [row[sweep + 1] for row in data]
            sweepData = np.array(sweepData[1:]).astype(np.float)

            full_sweepData = sweepData
            capacitance = sweepData[0]
            sweepData = sweepData[start_time:end_time]
            orig_sweepData = sweepData

            time_secs = orig_time_secs
            time_ms = orig_time_ms
        else:
            actual_sweep = sweepNumArray.iloc[sweep]
            actual_sweep = actual_sweep.split('_')
            actual_sweep = int(actual_sweep[1])

            sweep_voltage = voltage_array[int(sweep / 2)]

            sweepData = data.iloc[1:, sweep+1].astype(float)


            full_sweepData = sweepData
            capacitance = sweepData.iloc[0]
            sweepData = sweepData.loc[2:]
            sweepData = sweepData.iloc[start_time:end_time]
            orig_sweepData = sweepData

            time_secs = orig_time_secs
            time_ms = orig_time_ms

        #if actual_sweep == 8: #new
        # -50mV
        #if actual_sweep == 2:
        if sweep_voltage == -50:
            #capacitance = sweepData[0]
            sweepData = sweepData

            if numpy_pandas == 'numpy':
                cd_sweep_indx = [i for i in range(0, len(list(sweepData))) if (time_secs[i] >= 0.002 and time_secs[i] <= 2)]
                cd_data = sweepData[cd_sweep_indx]
                cd_time_data = time_secs[cd_sweep_indx]

                max_cd_peak = max(cd_data)

                max_cd_peak_indx = [i for i in range(0, len(list(cd_data))) if (cd_data[i] == max_cd_peak)]

                if max_cd_peak_indx[0] >= 5:
                    max_cd_peak_array = cd_data[max_cd_peak_indx[0] - 5:max_cd_peak_indx[0] + 6]

                    max_cd_peak = np.mean(max_cd_peak_array)

                '''
                if max_cd_peak < neg_50_amp_thresh*1e-12:
                    continue
                '''
                current_density_neg_50mV = max_cd_peak / capacitance
                peak_neg_50mV = max_cd_peak
                cap_neg_50mV = capacitance

                loc_max_cd = [i for i in range(0, len(list(cd_data))) if cd_data[i] >= max_cd_peak]
                loc_max_cd = cd_time_data[loc_max_cd][0]

            else:
                cd_sweep_indx = [i for i in range(0, len(sweepData)) if (time_secs.iloc[i] >= 0.002 and time_secs.iloc[i] <= 2)]
                #print(cd_sweep_indx)
                cd_data = sweepData.iloc[cd_sweep_indx]
                cd_time_data = time_secs.iloc[cd_sweep_indx]

                max_cd_peak = max(cd_data)

                max_cd_peak_indx = [i for i in range(0, len(list(cd_data))) if (cd_data.iloc[i] == max_cd_peak)]

                if max_cd_peak_indx[0] >= 5:
                    max_cd_peak_array = cd_data.iloc[max_cd_peak_indx[0] - 5:max_cd_peak_indx[0] + 6]

                    max_cd_peak = s_tats.mean(max_cd_peak_array)
                    #print(max_cd_peak)

                '''
                    if max_cd_peak < neg_50_amp_thresh*1e-12:
                        continue
                '''

                current_density_neg_50mV = max_cd_peak / capacitance
                peak_neg_50mV = max_cd_peak
                cap_neg_50mV = capacitance

                loc_max_cd = [i for i in range(0, len(list(cd_data))) if cd_data.iloc[i] >= max_cd_peak]
                loc_max_cd = cd_time_data.iloc[loc_max_cd[0]]





            fig1 = plt.figure()
            plt.plot(orig_time_secs, orig_sweepData)
            plt.plot(loc_max_cd, max_cd_peak, 'ro')
            plt.xlabel('Time (s)')
            plt.ylabel('Current (pA)')
            plt.title(wellID + ' Sweep ' + str(actual_sweep))
            #plt.show()
            plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '_image')
            with open(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '.pickle', 'wb') as fig_file:
                pickle.dump(fig1, fig_file)

        #elif actual_sweep == 9:
        elif sweep_voltage == -120:
        #elif actual_sweep == 15: #new
        # -120mV
            '''
            if min_current_greater_threshold(time_secs, sweepData, peak_current_parameter=neg_120_amp_thresh):
            #if min_current_greater_threshold(time_secs, sweepData, peak_current_parameter=-100.0E-12):
                continue
            '''

            sweepData = sweepData

            if numpy_pandas == 'numpy':
                cd_sweep_indx = [i for i in range(0, len(list(sweepData))) if (time_secs[i] >= 0.002 and time_secs[i] <= 2)]
                cd_data = sweepData[cd_sweep_indx]
                cd_time_data = time_secs[cd_sweep_indx]

                min_cd_peak = min(cd_data)

                min_cd_peak_indx = [i for i in range(0, len(list(cd_data))) if (cd_data[i] == min_cd_peak)]

                if min_cd_peak_indx[0] >= 5:
                    min_cd_peak_array = cd_data[min_cd_peak_indx[0] - 5:min_cd_peak_indx[0] + 6]
                    min_cd_peak = np.mean(min_cd_peak_array)

                '''
                if min_cd_peak > neg_120_amp_thresh*1e-12: # pA
                    continue
                '''

                peak_neg_120mV = min_cd_peak
                cap_neg_120mV = capacitance
                current_density_neg_120mV = min_cd_peak / capacitance

                loc_min_cd = [i for i in range(0, len(list(cd_data))) if cd_data[i] >= min_cd_peak]
                loc_min_cd = cd_time_data[loc_min_cd][0]

            else:
                cd_sweep_indx = [i for i in range(0, len(list(sweepData))) if (time_secs.iloc[i] >= 0.002 and time_secs.iloc[i] <= 2)]
                cd_data = sweepData.iloc[cd_sweep_indx]
                cd_time_data = time_secs.iloc[cd_sweep_indx]

                min_cd_peak = min(cd_data)

                min_cd_peak_indx = [i for i in range(0, len(list(cd_data))) if (cd_data.iloc[i] == min_cd_peak)]

                if min_cd_peak_indx[0] >= 5:
                    min_cd_peak_array = cd_data.iloc[min_cd_peak_indx[0] - 5:min_cd_peak_indx[0] + 6]
                    min_cd_peak = s_tats.mean(min_cd_peak_array)

                '''
                if min_cd_peak > neg_120_amp_thresh*1e-12: # pA
                    continue
                '''

                peak_neg_120mV = min_cd_peak
                cap_neg_120mV = capacitance
                current_density_neg_120mV = min_cd_peak / capacitance

                loc_min_cd = [i for i in range(0, len(list(cd_data))) if cd_data.iloc[i] >= min_cd_peak]
                loc_min_cd = cd_time_data.iloc[loc_min_cd[0]]


            fig2 = plt.figure()
            plt.plot(orig_time_secs, orig_sweepData)
            plt.plot(loc_min_cd, min_cd_peak, 'ro')
            plt.xlabel('Time (s)')
            plt.ylabel('Current (pA)')
            plt.title(wellID + ' Sweep ' + str(actual_sweep))
            #plt.show()
            plt.savefig(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '_image')
            with open(os.path.join(result_plots, wellID, wellID + '_Sweep' + str(actual_sweep)) + '.pickle',
                      'wb') as fig_file:
                pickle.dump(fig2, fig_file)


    plt.close('all')
    if current_density_neg_50mV != 'N/A' and current_density_neg_120mV != 'N/A':
        #current_density_ratio = current_density_neg_120mV / current_density_neg_50mV

        if current_density_neg_120mV > -50: #pA/pF
            current_density_ratio = 'N/A'
        else:
            current_density_ratio = current_density_neg_50mV/ current_density_neg_120mV
    else:
        current_density_ratio = 'N/A'


    if current_density_ratio != 'N/A':
        if current_density_ratio > 0:
            current_density_ratio = 'N/A'

    return [current_density_ratio, current_density_neg_50mV, current_density_neg_120mV]
