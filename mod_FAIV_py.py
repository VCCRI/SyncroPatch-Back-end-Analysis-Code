import csv
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import time

def mod_FAIV(drug_file, control_dir, result_plots, output_file, wellID, drug_control, result_dir):
    '''
    import gc
    #print(gc.get_count())
    gc.collect()
    #print(gc.get_count())
    '''

    raw_pattern = '*' + wellID + '*'
    raw_path = os.path.join(control_dir, raw_pattern)
    control_file = glob.glob(raw_path)

    #print(control_file[0])

    drug_data = []
    with open(drug_file) as csvfile:
        read = csv.reader(csvfile)
        for row in read:
            drug_data.append(row)

    drug_data = np.array(drug_data)

    control_data = []
    with open(control_file[0]) as csvfile:
        read_c = csv.reader(csvfile, delimiter='\t')
        for row in read_c:
            control_data.append(row)

    #control_data = np.array(control_data[3:])
    #print(control_data)

    drug_sweeps = drug_data[0, 1:]
    time_us = drug_data[1:, 0]
    voltage_stim = drug_data[1:, 1]
    drug_data = drug_data[1:, 1:]

    #Extract the control columns that correspond to the drug ones that passed QC
    control_intersect = np.array([])
    stim_voltages = np.array([])
    actual_sweeps = np.array([])
    for i in range(0, len(drug_sweeps), 2):
        control_column_index = drug_sweeps[i]
        #print(control_column_index)
        control_column_index = control_column_index.split('_')
        actual_sweeps = np.append(actual_sweeps, control_column_index[1])
        control_column_index = 2*(int(control_column_index[1])) + 1
        #print(control_column_index)




        #control_column = control_data[:, int(control_column_index)]
        control_voltage_column = np.array([row[int(control_column_index)-1] for row in control_data])
        control_column = np.array([row[int(control_column_index)] for row in control_data])
        #print(control_column)
        #print(control_column[1])
        stim_voltages = np.append(stim_voltages, control_column[1])
        control_column = control_column[3:]
        control_voltage_column = control_voltage_column[3:]
        #print(control_column)

        if np.shape(control_intersect)[0] == 0:
            control_intersect = control_voltage_column
            control_intersect = np.vstack((control_intersect, [control_column]))
        else:
            control_intersect = np.vstack((control_intersect, [control_voltage_column]))
            control_intersect = np.vstack((control_intersect, [control_column]))

    control_intersect = control_intersect.transpose()


    #time.sleep(20)
    '''
    if control_intersect.ndim > 1:

        control_average = np.mean(control_intersect.astype(np.float), axis=1)
        drug_average = np.mean(drug_data.astype(np.float), axis=1)
    elif control_intersect.ndim == 1:
        control_average = control_intersect.astype(np.float)
        drug_average = drug_data.astype(np.float).reshape(-1)
        #drug_average =
    
    
    
    #print(np.shape(control_average))
    #print(np.shape(drug_average))
    from numpy import matrix
    if drug_control == 'control':
        subtraction = (control_average - drug_average)
    elif drug_control == 'drug':
        subtraction = (drug_average - control_average)
    #print(np.shape(subtraction))
    #subtraction = subtraction.reshape((np.shape(subtraction)[1],))
    subtraction = subtraction*1e12
    #subtraction = subtraction.reshape((np.shape(subtraction)[1],))
    #subtraction = subtraction)
    #print(np.shape(subtraction))
    '''

    parameter_data = []
    parameter_data.append([])
    parameter_data[0].append('Sweep No.')
    parameter_data[0].append('AP signal Start Time (secs)')
    parameter_data[0].append('AP signal End Time (secs)')
    parameter_data[0].append('Max Peak (pA)')
    parameter_data[0].append('Min Peak (pA)')
    parameter_data[0].append('Peak Magnitude (pA)')
    #parameter_data[0].append('Peak Magnitude Ratio with Prior Adjacent AP signal')


    time_secs = time_us.astype(np.float)*1e-6
    #print('time done')

    os.mkdir(os.path.join(result_plots, wellID))
    subtracted_sweeps = np.array([])
    for sw in range(0, np.shape(control_intersect)[1], 2):
        #print(sw)
        #print(actual_sweeps[int(sw/2)])
        actual_sweep = actual_sweeps[int(sw/2)]
        stim_voltage = stim_voltages[int(sw/2)]
        #print(control_intersect[:, sw+1])
        if drug_control == 'control':
            subtracted_trace = (control_intersect[:, sw+1]).astype(np.float) - (drug_data[:, sw+1]).astype(np.float)
        elif drug_control == 'drug':
            subtracted_trace = (drug_data[:, sw+1]).astype(np.float) - (control_intersect[:, sw+1]).astype(np.float)

        fig = plt.figure()
        plt.plot(time_secs, subtracted_trace)
        if drug_control == 'control':
            plt.savefig(os.path.join(result_plots, wellID, wellID + ' sweep No. ' + str(actual_sweep) + ' control - drug full trace.png'))
        elif drug_control == 'drug':
            plt.savefig(os.path.join(result_plots, wellID, wellID + ' sweep No. ' + str(actual_sweep) + ' drug - control full trace.png'))
        plt.close(fig)

        sweep_heading = 'Sweep' + str(actual_sweep)
        if np.shape(subtracted_sweeps)[0] == 0:
            subtracted_sweeps = np.append(sweep_heading, control_intersect[:, sw])
            added_col = np.append(sweep_heading, subtracted_trace)
            subtracted_sweeps = np.vstack((subtracted_sweeps, [added_col]))
        else:
            added_col = np.append(sweep_heading, control_intersect[:, sw])
            subtracted_sweeps = np.vstack((subtracted_sweeps, [added_col]))
            added_col = np.append(sweep_heading, subtracted_trace)
            subtracted_sweeps = np.vstack((subtracted_sweeps, [added_col]))

        subtracted_trace = subtracted_trace*1e12

        baseline_voltage = voltage_stim[0]
        non_baseline_index = [i for i in range(0, len(control_intersect[:, sw])) if control_intersect[i, sw] == stim_voltage]
        # print(non_baseline_index)

        AP_indexes = np.array([])
        AP_array = np.array([])
        num_APs = 1

        peak_size = np.array([])

        #print(non_baseline_index)
        AP_signal = subtracted_trace[non_baseline_index]
        AP_times = time_secs[non_baseline_index]
        peak_magnitude = max(AP_signal) - min(AP_signal)

        max_peak = max(AP_signal)
        min_peak = min(AP_signal)

        max_time_indx = [t for t in range(len(AP_signal)) if AP_signal[t] == max_peak]
        min_time_indx = [t for t in range(len(AP_signal)) if AP_signal[t] == min_peak]
        # print(max_time_indx)
        # print(min_time_indx)

        fig1 = plt.figure()
        plt.plot(AP_times, AP_signal)

        plt.plot(AP_times[max_time_indx[0]], max_peak, 'ro')
        plt.plot(AP_times[min_time_indx[0]], min_peak, 'ro')

        plt.savefig(os.path.join(result_plots, wellID,
                                 wellID + ' sweep ' + str(actual_sweep) + ' AP signal ' + str(num_APs) + '.png'))
        plt.close(fig1)

        peak_size = np.append(peak_size, peak_magnitude)
        if np.mod(num_APs, 2) == 0:
            ratio = peak_size[num_APs - 1] / peak_size[num_APs - 2]
        else:
            ratio = ''
            # peak_ratios = np.append(peak_ratios, ratio)
            # parameter_data[i].append(ratio)

        # peak_magnitude = max(matrix(AP_array)) - min(matrix(AP_array))
        # if np.mod(num_APs, 2) == 0:
        parameter_data.append([])
        parameter_data[int(sw/2)+1].append('Sweep ' + str(actual_sweep))
        parameter_data[int(sw/2)+1].append(AP_times[0])
        parameter_data[int(sw/2)+1].append(AP_times[-1])
        parameter_data[int(sw/2)+1].append(max_peak)
        parameter_data[int(sw/2)+1].append(min_peak)
        parameter_data[int(sw/2)+1].append(peak_magnitude)
        #parameter_data[int(sw/2)+1].append(ratio)
        #print(parameter_data)

    output_file = os.path.join(result_plots, wellID, wellID + ' results.csv')
    with open(output_file, mode='w') as result_output:
        result_writer = csv.writer(result_output, delimiter=',', lineterminator='\n')
        for row in range(0, len(actual_sweeps)+1):
            result_writer.writerow(parameter_data[row])


    # Now make the output files of the subtracted trace
    if drug_control == 'drug':
        output_sub_file = os.path.join(result_dir, 'mod FAIV ' + wellID + ' drug -  control subtracted trace data.csv')
    elif drug_control == 'control':
        output_sub_file = os.path.join(result_dir, 'mod FAIV ' + wellID + ' control -  drug subtracted trace data.csv')

    #print(output_sub_file)
    time_us = np.append('Time (us)', time_us)
    output_subtracted_data = np.vstack(([time_us], subtracted_sweeps))

    output_subtracted_data = output_subtracted_data.transpose()

    with open(output_sub_file, mode='w') as result_sub_output:
        result_sub_writer = csv.writer(result_sub_output, delimiter=',', lineterminator='\n')
        for row in range(0, np.shape(output_subtracted_data)[0]):
            #print(output_subtracted_data[row])
            result_sub_writer.writerow(output_subtracted_data[row])

