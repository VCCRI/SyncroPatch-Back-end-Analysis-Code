import csv
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

def AP_pre_stim(drug_file, control_dir, result_plots, output_file, wellID, drug_control, result_dir):
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

    drug_sweeps = drug_data[0, 2:]
    time_us = drug_data[1:, 0]
    voltage_stim = drug_data[1:, 1]
    drug_data = drug_data[1:, 2:]

    #Extract the control columns that correspond to the drug ones that passed QC
    control_intersect = np.array([])
    for i in range(0, len(drug_sweeps)):
        control_column_index = drug_sweeps[i]
        control_column_index = control_column_index.split('_')
        control_column_index = int(control_column_index[1]) + 2

        #control_column = control_data[:, int(control_column_index)]
        control_column = np.array([row[int(control_column_index)] for row in control_data])
        control_column = control_column[3:]
        if np.shape(control_intersect)[0] == 0:
            control_intersect = control_column
        else:
            control_intersect = np.vstack((control_intersect, [control_column]))
    control_intersect = control_intersect.transpose()

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

    time_secs = time_us.astype(np.float)*1e-6
    #print('time done')


    os.mkdir(os.path.join(result_plots, wellID))

    fig = plt.figure()
    plt.plot(time_us, subtraction)
    if drug_control == 'control':
        plt.savefig(os.path.join(result_plots, wellID, wellID + ' control - drug full trace.png'))
    elif drug_control == 'drug':
        plt.savefig(os.path.join(result_plots, wellID, wellID + ' drug - control full trace.png'))
    plt.close(fig)


    baseline_voltage = voltage_stim[0]
    non_baseline_index = [i for i in range(0, len(voltage_stim)) if voltage_stim[i] != baseline_voltage]
    #print(non_baseline_index)

    AP_indexes = np.array([])
    AP_array = np.array([])
    num_APs = 1

    peak_size = np.array([])

    parameter_data = []
    parameter_data.append([])
    parameter_data[0].append('AP signal Number')
    parameter_data[0].append('AP signal Start Time (secs)')
    parameter_data[0].append('AP signal End Time (secs)')
    parameter_data[0].append('Max Peak (pA)')
    parameter_data[0].append('Min Peak (pA)')
    parameter_data[0].append('Peak Magnitude (pA)')
    parameter_data[0].append('Peak Magnitude Ratio with Prior Adjacent AP signal')

    #for i in range(1, 7):

        #parameter_data[i].append('AP signal ' + str(i))

    for i in range(0, len(non_baseline_index)-1):
        if num_APs == 7:
            break
        if non_baseline_index[i] != non_baseline_index[i+1]-1:
            '''
            print(AP_array)
            if np.shape(AP_indexes)[0] == 0:
                AP_indexes = AP_array
            else:
                print(np.shape(AP_indexes))
                print(np.shape(AP_array))

                if np.shape(AP_indexes)[0] > np.shape(AP_array)[0]:
                    num_rows = np.shape(AP_indexes)[0] - np.shape(AP_array)[0]

                    empty_table = np.empty([num_rows])
                    empty_table = empty_table.astype(str)
                    empty_table.fill('')

                    # AP_array = np.hstack((AP_array, [empty_table]))
                    AP_array = np.append(AP_array, empty_table)
                    print(AP_array)

                elif np.shape(AP_indexes)[0] < np.shape(AP_array)[0]:
                    num_rows = np.shape(AP_array)[0] - np.shape(AP_indexes)[0]
                    try:
                        num_cols = np.shape(AP_indexes)[1]
                        empty_table = np.empty([num_rows, num_cols])
                        empty_table = empty_table.astype(str)
                        empty_table.fill('')

                        AP_indexes = np.hstack((AP_indexes, [empty_table]))
                    except:
                        empty_table = np.empty([num_rows])
                        empty_table = empty_table.astype(str)
                        empty_table.fill('')

                        AP_indexes = np.append(AP_indexes, empty_table)
                        AP_indexes = AP_indexes.transpose()
                        AP_array = AP_array.transpose()


                print(np.shape(AP_indexes))
                print(np.shape(AP_array))
                AP_indexes = np.vstack((AP_indexes, [AP_array]))
                print(AP_indexes)

            AP_array = np.array([])
            num_APs += 1
            '''
            AP_array = AP_array.astype(int)
            '''
            plt.figure(num_APs)
            plt.plot(time_us[list(AP_array)], subtraction[list(AP_array)])
            plt.show()
            '''
            '''
            import gc
            #print(gc.get_count())
            gc.collect()
            #print(gc.get_count())
            '''

            AP_signal = subtraction[list(AP_array)]
            AP_times = time_secs[list(AP_array)]
            peak_magnitude = max(AP_signal) - min(AP_signal)

            max_peak = max(AP_signal)
            min_peak = min(AP_signal)


            max_time_indx = [t for t in range(len(AP_signal)) if AP_signal[t] == max_peak]
            min_time_indx = [t for t in range(len(AP_signal)) if AP_signal[t] == min_peak]
            #print(max_time_indx)
            #print(min_time_indx)


            fig1 = plt.figure()
            plt.plot(AP_times, AP_signal)

            plt.plot(AP_times[max_time_indx[0]], max_peak, 'ro')
            plt.plot(AP_times[min_time_indx[0]], min_peak, 'ro')

            plt.savefig(os.path.join(result_plots, wellID, wellID + ' AP signal ' + str(num_APs) +'.png'))
            plt.close(fig1)

            peak_size = np.append(peak_size, peak_magnitude)
            if np.mod(num_APs, 2) == 0:
                ratio = peak_size[num_APs-1] / peak_size[num_APs-2]
            else:
                ratio = ''
                #peak_ratios = np.append(peak_ratios, ratio)
                #parameter_data[i].append(ratio)

            #peak_magnitude = max(matrix(AP_array)) - min(matrix(AP_array))
            #if np.mod(num_APs, 2) == 0:
            parameter_data.append([])
            parameter_data[num_APs].append('AP signal ' + str(num_APs))
            parameter_data[num_APs].append(AP_times[0])
            parameter_data[num_APs].append(AP_times[-1])
            parameter_data[num_APs].append(max_peak)
            parameter_data[num_APs].append(min_peak)
            parameter_data[num_APs].append(peak_magnitude)
            parameter_data[num_APs].append(ratio)


            AP_array = np.array([])
            num_APs += 1
        else:
            AP_array = np.append(AP_array, non_baseline_index[i])

    '''
    peak_ratios = np.array([])
    for i in range(0, len(peak_size)):
        if np.mod(i, 2) != 0:
            ratio = peak_size[i-1]/peak_size[i]
            peak_ratios = np.append(peak_ratios, ratio)
            parameter_data[i].append(ratio)
    '''

    #print(wellID)
    #print(peak_ratios)
    #print(AP_indexes)

    #print(parameter_data)

    output_file = os.path.join(result_plots, wellID, 'results.csv')
    with open(output_file, mode='w') as result_output:
        result_writer = csv.writer(result_output, delimiter=',', lineterminator='\n')
        for row in range(0, num_APs):
            result_writer.writerow(parameter_data[row])

    if drug_control == 'drug':
        output_sub_file = os.path.join(result_dir, 'mod FAIV ' + wellID + ' drug -  control subtracted trace data.csv')
    elif drug_control == 'control':
        output_sub_file = os.path.join(result_dir, 'mod FAIV ' + wellID + ' control -  drug subtracted trace data.csv')

    subtraction = subtraction * 1e-12

    time_output = np.append('Time us', time_us)
    volt_output = np.append('Voltage Stimulus (mV)', voltage_stim)
    sub_output = np.append('Average Subtracted Signal', subtraction)

    output_sub_data = np.vstack(([time_output], [volt_output]))
    output_sub_data = np.vstack((output_sub_data, [sub_output]))

    output_sub_data = output_sub_data.transpose()

    with open(output_sub_file, mode='w') as result_sub_output:
        result_sub_writer = csv.writer(result_sub_output, delimiter=',', lineterminator='\n')
        for row in range(0, np.shape(output_sub_data)[0]):
            #print(output_subtracted_data[row])
            result_sub_writer.writerow(output_sub_data[row])

    #print(drug_sweeps)
    for element in dir():
        if element[0:2] != "__":
            #print(globals()[element])
            #print(element)
            #del globals()[element]
            del element


    import gc
    #print(gc.get_count())
    gc.collect()
    #print(gc.get_count())







