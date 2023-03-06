import os
import numpy as np
import csv
import shutil
import glob
import time
import statistics as sts
import matplotlib.pyplot as plt
import winsound
import pandas as pd


def prompt_user(filename_prompt, file_dir, data_dir, summary):
    dir_name = str(input(filename_prompt))

    if not dir_name:
        dir_name = prompt_user(filename_prompt, file_dir, data_dir, summary)
        return

    # Try and join the parent_dir to the front of the file or dir
    dir_name = os.path.join(data_dir, dir_name)

    # Check the correct file extension has been appended
    if file_dir == 'file':
        if '.csv' not in dir_name:
            if summary == 1:
                no_well_dir_name = dir_name + '_no_wellID'
                dir_name = dir_name + '.csv'
                no_well_dir_name = no_well_dir_name + '.csv'
            else:
                dir_name = dir_name + '.csv'
        else:
            if summary == 1:
                no_well_dir_name = dir_name.split('.')
                no_well_dir_name = str(no_well_dir_name[0]) + '_no_wellID'
                no_well_dir_name = no_well_dir_name + '.csv'

    if file_dir == 'file':
        if os.path.isfile(dir_name):
            changed_name = 0
            while 1:
                check = input(
                    'The selected directory name already exists, do you wish to continue? If so data will be lost (yes/no):\n')
                if check == 'yes':
                    break
                elif check == 'no':
                    dir_name = input(filename_prompt)
                    dir_name = os.path.join(data_dir, dir_name)
                    if not os.path.isfile(dir_name):
                        changed_name = 1
                        break
            if changed_name == 0:
                os.remove(dir_name)
                if os.path.isfile(no_well_dir_name):
                    os.remove(no_well_dir_name)
        return [dir_name, no_well_dir_name]
    elif file_dir == 'dir':
        if os.path.isdir(dir_name):
            changed_name = 0
            while 1:
                check = input(
                    'The selected directory name already exists, do you wish to continue? If so data will be lost (yes/no):\n')
                if check == 'yes':
                    break
                elif check == 'no':
                    dir_name = input(filename_prompt)
                    dir_name = os.path.join(data_dir, dir_name)
                    if not os.path.isdir(dir_name):
                        changed_name = 1
                        break
            if changed_name == 0:
                # print(os.listdir(dir_name))
                # os.rmdir(dir_name)
                shutil.rmtree(dir_name)
        os.mkdir(dir_name)
        return dir_name


def qc_well(well_names, well, parent_dir, data_dir, analysis, numpy_pandas, total_sweeps, QC_data, seal_parameter, capacitance_parameter_lower, capacitance_parameter_upper, access_parameter, access_switch, peak_current_parameter, SatMutVariantNames, output_dir, failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps):

    if numpy_pandas == 'pandas':
        wellID = well_names.iloc[well]
        wellCol = str(well_names.iloc[well][1] + well_names.iloc[well][2])
        wellCol = int(wellCol)
    else:
        wellID = well_names[well]
        wellCol = str(well_names[well][1] + well_names[well][2])
        wellCol = int(wellCol)
    # Get the corresponding raw data file and open
    raw_pattern = '*' + wellID + '*'
    raw_path = os.path.join(parent_dir, data_dir, raw_pattern)
    current_file = glob.glob(raw_path)

    if numpy_pandas == 'numpy':
        rawWellData = []
        with open(current_file[0]) as csvfile:
            read = csv.reader(csvfile, delimiter='\t')
            for row in read:
                rawWellData.append(row)
    else:
        # pandas
        rawWellData = pd.read_csv(current_file[0], sep='\t', low_memory=False,
                                  usecols=[i for i in range((2 * total_sweeps) + 2)], header=None)

    # print(np.shape(rawWellData))
    if analysis == 'Onset':
        if numpy_pandas == 'numpy':
            rawWellData = rawWellData[3:]
            currentData = np.array(rawWellData)
            rawWellData = currentData[:, 1:]
        else:
            rawWellData = rawWellData.iloc[3:]
            rawWellData = rawWellData.iloc[:, 1:]
    elif analysis == 'AP pre-stim' or analysis == 'mod FAIV':
        rawWellData = rawWellData[3:]
        rawWellData = np.array(rawWellData)

        time_data = rawWellData[:, 1]
        current_data = rawWellData[:, 2:]
        time_data = time_data.transpose()

        rawWellData = np.vstack((np.array(time_data), current_data.transpose()))
        rawWellData = rawWellData.transpose()
    else:
        if numpy_pandas == 'pandas':
            # pands method
            voltage_row = rawWellData.iloc[1, :]
            voltage_row = voltage_row.iloc[2:]
            rawWellData = rawWellData.iloc[3:, :]

            time_data = rawWellData.iloc[:, 1]
            current_data = rawWellData.iloc[:, 2:]

            # axis=0 = vstack
            # axis=1 = hstack

            current_data = pd.concat([voltage_row, current_data.transpose()], axis=1)
            rawWellData = pd.concat([time_data, current_data.transpose()], axis=1)

            del current_data

        else:
            # numpy method

            voltage_row = rawWellData[1]
            voltage_row = voltage_row[2:]
            rawWellData = rawWellData[3:]
            rawWellData = np.array(rawWellData)
            # rawWellData = pd.array(rawWellData)

            time_data = rawWellData[:, 1]
            current_data = rawWellData[:, 2:]
            time_data = time_data.transpose()
            voltage_row = np.array(voltage_row).transpose()
            # voltage_row = pd.array(voltage_row).transpose()
            time_data = np.hstack(([-1], np.array(time_data)))
            current_data = np.vstack((np.array(voltage_row), current_data))
            # time_data = np.hstack(([-1], pd.array(time_data)))
            # current_data = np.vstack((pd.array(voltage_row), current_data))

            rawWellData = np.vstack((np.array(time_data), current_data.transpose()))
            # rawWellData = np.vstack((pd.array(time_data), current_data.transpose()))
            rawWellData = rawWellData.transpose()

            # print(rawWellData)

    passed_sweeps = 0
    if numpy_pandas == 'numpy':
        sweep_headers = np.array(['Time_us'])
        time_us = rawWellData[:, 0]
        time_ms = np.array(time_us).astype(float)
        time_secs = np.array(time_us).astype(float)
        time_ms_list = list(time_ms * 1E-3)
        time_secs_list = list(time_secs * 1E-6)
    else:
        sweep_headers = pd.DataFrame(['Time_us'])
        time_us = rawWellData.iloc[1:, 0]
        time_ms = np.array(time_us).astype(float)
        time_secs = np.array(time_us).astype(float)
        time_ms_list = list(time_ms * 1E-3)
        time_secs_list = list(time_secs * 1E-6)

    if analysis == 'ssDeact':
        # Check that -120mV (sweep 15, index 30) passes QC check
        if numpy_pandas == 'numpy':
            start_time_indx = [i for i in range(0, len(time_secs_list)) if time_secs_list[i] >= 1.202]
            end_time_indx = [i for i in range(0, len(time_secs_list)) if time_secs_list[i] > 4.2]
            neg_120mV_data = np.array(rawWellData[start_time_indx[0]:end_time_indx[0], 30]).astype(float)
            neg_120mV_time = np.array(time_secs_list[start_time_indx[0]:end_time_indx[0]]).astype(float)
        else:
            start_time_indx = [i for i in range(0, len(time_secs_list)) if time_secs_list[i] >= 1.202]
            end_time_indx = [i for i in range(0, len(time_secs_list)) if time_secs_list[i] > 4.2]
            neg_120mV_data = np.array(rawWellData.iloc[start_time_indx[0]:end_time_indx[0], 30]).astype(float)
            neg_120mV_time = np.array(time_secs_list[start_time_indx[0]:end_time_indx[0]]).astype(float)

        min_value = min(neg_120mV_data)
        # print(min_value)

        min_index = [i for i in range(0, len(neg_120mV_data)) if neg_120mV_data[i] == min_value]

        min_time_point = neg_120mV_time[min_index[0]]

        point_two_time = min_time_point + 0.05

        point_two_index = [i for i in range(0, len(neg_120mV_data)) if neg_120mV_time[i] >= point_two_time]

        try:
            point_two_value = neg_120mV_data[point_two_index[0]]
        except:
            return [failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps]

        ratio = point_two_value / min_value

        if ratio > 0.7:
            # num_failed += 1
            return [failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps]

        if min_time_point > 1.215:
            # num_failed += 1
            return [failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps]

    if analysis == 'AP pre-stim':

        interval = 1
        end_limit = total_sweeps + 1
        start = 2  # ignore the first sweep
        '''
        interval = 2
        end_limit = (2*(total_sweeps+1))
        start = 2  # ignore the first sweep
        '''
    else:
        interval = 2
        end_limit = (2 * (total_sweeps + 1))
        start = 2

    if analysis == 'ssAct' or analysis == 'ssDeact':
        if numpy_pandas == 'numpy':
            outputWellData = np.hstack(([0], rawWellData[:, 0]))
            outputWellData = np.append('Time_us', outputWellData)
        else:
            outputWellData = pd.concat((pd.DataFrame([0]), rawWellData.iloc[:, 0]), axis=0)
            outputWellData = pd.concat((pd.DataFrame(['Time_us']), outputWellData), axis=0)
    else:
        if numpy_pandas == 'numpy':
            outputWellData = np.array([rawWellData[:, 0]])
            outputWellData = np.append('Time_us', outputWellData)
        else:
            outputWellData = rawWellData.iloc[:, 0]
            outputWellData = pd.concat((pd.DataFrame(['Time_us']), outputWellData), axis=0)

    for sweep in range(start, end_limit, interval):

        if numpy_pandas == 'numpy':
            leak_time_indx_list = [i for i in range(len(time_ms_list)) if 90 >= time_ms_list[i] >= 60]
            leak_curr = np.array(rawWellData[leak_time_indx_list, sweep]).astype(float)
            leak_time = np.array(rawWellData[leak_time_indx_list, 0]).astype(float) * 1e-3
            med_leak_curr = sts.median(leak_curr)
        else:
            leak_time_indx_list = [i for i in range(len(time_ms_list)) if 90 >= time_ms_list[i] >= 60]
            leak_curr = np.array(rawWellData.iloc[leak_time_indx_list, sweep]).astype(float)
            leak_time = np.array(rawWellData.iloc[leak_time_indx_list, 0]).astype(float) * 1e-3
            med_leak_curr = sts.median(leak_curr)

        if analysis == 'ssDeact':
            # tot_range_time_indx_list = [i for i in range(0, len(time_secs_list)) if 4.2 >= time_secs_list[i] >= 1.202]

            start_time_indx = [i for i in range(0, len(time_secs_list)) if time_secs_list[i] >= 1.202]
            end_time_indx = [i for i in range(0, len(time_secs_list)) if time_secs_list[i] > 4.2]
            # start_time_indx = [i for i in range(0, len(time_secs_list)) if time_secs_list[i] >= 1.1]
            # end_time_indx = [i for i in range(0, len(time_secs_list)) if time_secs_list[i] > 4.1]

            if numpy_pandas == 'numpy':
                max_amp = max(np.array(rawWellData[start_time_indx[0]:end_time_indx[0], sweep]).astype(float))
            else:
                max_amp = max(np.array(rawWellData.iloc[start_time_indx[0]:end_time_indx[0], sweep]).astype(float))

        elif analysis == 'ssAct':
            tot_range_time_indx_list = [i for i in range(len(time_secs_list)) if 1.3 >= time_secs_list[i] >= 1.205]
            # max_amp = max(np.array(rawWellData[tot_range_time_indx_list, sweep]).astype(float))
        elif analysis == 'Onset':
            tot_range_time_indx_list = [i for i in range(len(time_secs_list)) if 1.25 >= time_secs_list[i] >= 1.175]
            if numpy_pandas == 'numpy':
                max_amp = max(np.array(rawWellData[tot_range_time_indx_list, sweep]).astype(float))
            else:
                max_amp = max(np.array(rawWellData.iloc[tot_range_time_indx_list, sweep]).astype(float))

        # Leak Current Check

        if analysis == 'Onset':
            if not 100 * 1E-12 >= med_leak_curr >= -100 * 1E-12:
                # print('LEAK CHECK REMOVED PLEASE FIX -  FIND CODE AND UNCOMMENT CONTINUE')
                failed_leak += 1
                total_fail_sweeps += 1
                continue

        else:
            if not 40 * 1E-12 >= med_leak_curr >= -40 * 1E-12:
                '''
                print(wellID)
                print(sweep)
                print(med_leak_curr)
                print('fail leak check')
                #time.sleep(5)
                '''
                # print('LEAK CHECK REMOVED PLEASE FIX -  FIND CODE AND UNCOMMENT CONTINUE')
                failed_leak += 1
                total_fail_sweeps += 1
                continue

        if analysis == 'AP pre-stim':

            seal_index = (int(sweep) - 2) * 3  # 2=0, 3=3, 4=6
            capacitance_index = ((int(sweep) - 2) * 3) + 1  # 2=1, 3=4,
            access_index = ((int(sweep) - 2) * 3) + 2
            sw = int(sweep) - 1
            '''
            seal_index = (int(sweep / 2) - 1) * 3
            capacitance_index = ((int(sweep / 2) - 1) * 3) + 1
            access_index = ((int(sweep / 2) - 1) * 3) + 2
            sw = int(sweep / 2)
            '''
        else:
            seal_index = (int(sweep / 2) - 1) * 3
            capacitance_index = ((int(sweep / 2) - 1) * 3) + 1
            access_index = ((int(sweep / 2) - 1) * 3) + 2
            sw = int(sweep / 2)
        # Check the seal
        if numpy_pandas == 'numpy':
            # Check the seal
            if float(QC_data[well, seal_index]) < float(seal_parameter):
                '''
                print(wellID)
                print(sweep)
               # print(QC_data[well, (sweep-1)*3])
                print('fail seal check')
                #ime.sleep(5)
                '''
                failed_seal += 1
                total_fail_sweeps += 1
                continue

            # Check the capacitance
            if not float(capacitance_parameter_upper) >= float(QC_data[well, capacitance_index]) >= float(
                    capacitance_parameter_lower):
                '''
                print(wellID)
                print(sweep)
                #print(QC_data[well, ((sweep-1)*3)+1])
                print('fail cap check')
                #time.sleep(5)
                '''
                failed_cap += 1
                total_fail_sweeps += 1
                continue
            # Check the access

            '''
            if float(QC_data[well, access_index]) > float(access_parameter):
                continue
            '''
            '''
            if analysis == 'ssAct':
                # actually sweep 10 but double due to skipping every 2 columns due to voltage column addition
                print(sweep)
                if sweep == 20:
                    print('in')
                    print(float(min_amp))
                    print(float(peak_current_parameter))
                    if float(min_amp) > float(peak_current_parameter):
                        print('ssAct fail peak current')
                        print(sweep)
                        continue
            '''
            if analysis == 'Onset':
                if float(max_amp) < float(peak_current_parameter):
                    failed_peak += 1
                    total_fail_sweeps += 1
                    continue
        else:
            # pandas
            if float(QC_data.iloc[well, seal_index]) < float(seal_parameter):
                '''
                print(wellID)
                print(sweep)
               # print(QC_data[well, (sweep-1)*3])
                print('fail seal check')
                #ime.sleep(5)
                '''
                failed_seal += 1
                total_fail_sweeps += 1
                continue

            # Check the capacitance
            if not float(capacitance_parameter_upper) >= float(QC_data.iloc[well, capacitance_index]) >= float(
                    capacitance_parameter_lower):
                '''
                print(wellID)
                print(sweep)
                #print(QC_data[well, ((sweep-1)*3)+1])
                print('fail cap check')
                #time.sleep(5)
                '''
                failed_cap += 1
                total_fail_sweeps += 1
                continue
            # Check the access

            '''
            if float(QC_data[well, access_index]) > float(access_parameter):
                continue
            '''
            '''
            if analysis == 'ssAct':
                # actually sweep 10 but double due to skipping every 2 columns due to voltage column addition
                print(sweep)
                if sweep == 20:
                    print('in')
                    print(float(min_amp))
                    print(float(peak_current_parameter))
                    if float(min_amp) > float(peak_current_parameter):
                        print('ssAct fail peak current')
                        print(sweep)
                        continue
            '''
            if analysis == 'Onset':
                if float(max_amp) < float(peak_current_parameter):
                    failed_peak += 1
                    total_fail_sweeps += 1
                    continue

        # Passed all QC. Copy file now

        sweep_heading = 'Sweep_' + str(sw)
        if numpy_pandas == 'numpy':
            sweep_headers = np.append(sweep_headers, sweep_heading)
        else:
            sweep_headers = pd.concat((sweep_headers, pd.DataFrame([sweep_heading])), axis=0)
        passed_sweeps += 1

        if analysis == 'AP pre-stim':

            result = np.array([])
            result = np.append(result, rawWellData[:, sweep])
            result = np.append(sweep_heading, result)

            if outputWellData.ndim == 1:
                v_result = np.array([])
                v_result = np.append(v_result, rawWellData[:, 1])
                v_result = np.append('Voltage (V)', v_result)

                # Append the raw data the output matrix
                outputWellData = np.vstack((outputWellData, v_result))
                outputWellData = np.vstack((outputWellData, result))
            else:
                # Append the raw data the output matrix
                outputWellData = np.vstack((outputWellData, result))
            '''
            result = np.array([])
            v_result = np.array([])
            result = np.append(result, rawWellData[:, sweep])
            v_result = np.append(v_result, rawWellData[:, sweep - 1])
            result = np.append(sweep_heading, result)
            v_result = np.append(sweep_heading, v_result)

            # Append the raw data the output matrix
            # print(v_result)
            # print(result)
            # print(outputWellData)
            outputWellData = np.vstack((outputWellData, v_result))
            outputWellData = np.vstack((outputWellData, result))
            '''

        else:
            if numpy_pandas == 'numpy':
                result = np.array([])
                v_result = np.array([])
                if analysis == 'ssAct' or analysis == 'ssDeact':
                    result = np.array([QC_data[well, capacitance_index]])
                    v_result = np.array([QC_data[well, capacitance_index]])
                result = np.append(result, rawWellData[:, sweep])
                v_result = np.append(v_result, rawWellData[:, sweep - 1])
                result = np.append(sweep_heading, result)
                v_result = np.append(sweep_heading, v_result)

                # Append the raw data the output matrix
                # print(v_result)
                # print(result)
                # print(outputWellData)
                outputWellData = np.vstack((outputWellData, v_result))
                outputWellData = np.vstack((outputWellData, result))
                # print(outputWellData)
                # return
            else:
                # pandas
                if analysis == 'ssAct' or analysis == 'ssDeact':
                    result = pd.concat(
                        (pd.DataFrame([QC_data.iloc[well, capacitance_index]]), rawWellData.iloc[:, sweep]), axis=0)
                    v_result = pd.concat(
                        (pd.DataFrame([QC_data.iloc[well, capacitance_index]]), rawWellData.iloc[:, sweep - 1]),
                        axis=0)
                result = pd.concat((pd.DataFrame([sweep_heading]), result), axis=0)
                v_result = pd.concat((pd.DataFrame([sweep_heading]), v_result), axis=0)
                outputWellData = pd.concat((outputWellData, v_result), axis=1)
                outputWellData = pd.concat((outputWellData, result), axis=1)

    if passed_sweeps == 0:
        num_failed += 1
        return [failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps]
    name_part = current_file[0].split('\\')
    name_part = name_part[-1].split('.csv')
    name_part = name_part[0].replace('.', '_')
    name_part = name_part + str(passed_sweeps) + '.csv'

    if wellCol % 2 == 0:
        var_indx = wellCol / 2
    else:
        var_indx = (wellCol + 1) / 2
    var_dir = SatMutVariantNames[int(var_indx - 1)]
    result_file_path = os.path.join(output_dir, var_dir, name_part)

    if numpy_pandas == 'numpy':
        outputWellData = outputWellData.transpose()

        with open(result_file_path, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(outputWellData)[0]):
                result_writer.writerow(outputWellData[row])
    else:
        '''
        with open(result_file_path, mode='w') as result_output:
            #result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, outputWellData.shape[0]):
                print(outputWellData.iloc[row])
                #result_writer.writerow(outputWellData[row])
        '''
        # print(result_file_path)

        # Trim the output data to only include rows that are pertinent to the current expression times




        outputWellData.to_csv(result_file_path, index=False, header=False, chunksize=1000)


    return [failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps]

# def quality_control_sat_mut_py(parent_path, parent_dir, qc_file, variant_name_file, total_sweeps, analysis, srvr_analysis):
def automate_quality_control_sat_mut_py(parent_dir, data_dir, plate_name, qc_file, variant_name_file, total_sweeps,
                                        analysis, seal_parameter, capacitance_parameter_upper,
                                        capacitance_parameter_lower, access_parameter, peak_current_parameter,
                                        output_dir, qc_stats_file, numpy_pandas):
    # parent_dir, data_dir, plate_name
    # seal_parameter = 1000E6

    access_switch = 0
    '''
    if analysis == 'AP pre-stim':
        seal_parameter = 500E6
    else:
        seal_parameter = 300E6  # For ssAct, ssDeact, Onset
    '''
    '''
    seal_parameter = float(input('Enter the magnitude required for the seal resistance quality (Ohms):\n'))
    capacitance_parameter_upper = float(input('Enter the magnitude required for the capacitance UPPER limit (Farads):\n'))
    #capacitance_parameter_upper = 50E-12
    capacitance_parameter_lower = float(input('Enter the magnitude required for the capacitance LOWER limit (Farads):\n'))

    #capacitance_parameter_lower = 5e-12
    '''
    '''
    if analysis == 'Onset':
        access_parameter = 15E6  # For onset
    else:
        access_parameter = 20E6  # For ssAct and Deact
        #access_parameter = 40E6
    '''
    '''
    access_parameter = float(input('Enter the magnitude required for the access resistance (Ohms):\n'))
    #access_parameter = 20E6 #For ssAct and Deact
    #access_parameter = 15E6 #For onset
    peak_current_parameter = input('Enter the magnitude required for the peak control current (Amperes):\n')
    #peak_current_parameter = 100E-12
    '''

    if analysis == 'ssDeact':
        result_parent_dir = 'Data Analysis Results ssDeact'

    elif analysis == 'ssAct':
        result_parent_dir = 'Data Analysis Results ssAct'
    elif analysis == 'Onset':
        result_parent_dir = 'Data Analysis Results Onset Inact'

    elif analysis == 'AP pre-stim':
        result_parent_dir = 'Data Analysis Results AP pre-stim'

    elif analysis == 'mod FAIV':
        result_parent_dir = 'Data Analysis Results mod FAIV'

    result_parent_dir = os.path.join(parent_dir, result_parent_dir)
    if not os.path.isdir(result_parent_dir):
        # os.mkdir(result_parent_dir)
        output_parent_dir = os.path.join(result_parent_dir, plate_name)
        if not os.path.isdir(output_parent_dir):
            os.mkdir(output_parent_dir)
    else:
        output_parent_dir = os.path.join(result_parent_dir, plate_name)
        if not os.path.isdir(output_parent_dir):
            os.mkdir(output_parent_dir)

    # output_dir = prompt_user('What would you like to name the directory that stores the data files that pass quality control requirements?:\n','dir', output_parent_dir, 0)
    # output_dir = os.path.join(output_parent_dir, 'success_QC no series resistance -120mV filtering')
    # qc_stats_file = os.path.join(output_parent_dir, 'qc_statistics_no_series_neg_120_filtering.csv')

    output_dir = os.path.join(output_parent_dir, output_dir)
    qc_stats_file = os.path.join(output_parent_dir, qc_stats_file)

    variant_name_file = os.path.join(parent_dir, variant_name_file)

    filename = os.path.join(parent_dir, data_dir, qc_file)

    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    print('Commencing Quality Control Analysis...')

    if numpy_pandas == 'numpy':

        # numpy method
        QC_data = []
        count = 1
        with open(filename) as csvfile:
            read = csv.reader(csvfile, delimiter='\t')
            for row in read:
                if 387 >= count >= 4:
                    QC_data.append(row)
                count += 1
        QC_data = np.array(QC_data)
    else:
        # pandas method
        QC_data = pd.read_csv(filename, delimiter='\t')

    # Extract the mutant names
    SatMutVariantNames = []
    with open(variant_name_file) as var_file:
        for line in var_file:
            SatMutVariantNames.append(line)

    for var in range(0, len(SatMutVariantNames)):
        SatMutVariantNames[var] = SatMutVariantNames[var].replace(':', '_')
        SatMutVariantNames[var] = SatMutVariantNames[var].replace('\n', '')

        result_path = os.path.join(output_dir, SatMutVariantNames[var])
        os.mkdir(result_path)

    if numpy_pandas == 'numpy':
        well_names = QC_data[:, 0]
        QC_data = QC_data[:, 2:]
    else:
        # pandas
        well_names = QC_data.iloc[2:386, 0]
        QC_data = QC_data.iloc[2:386, 2:]

    num_wells = len(well_names)
    num_failed = 0
    failed_seal = 0
    failed_cap = 0
    failed_peak = 0
    failed_leak = 0
    failed_access = 0
    total_fail_sweeps = 0
    for well in range(0, num_wells):
        [failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps] = qc_well(well_names, well, parent_dir, data_dir, analysis, numpy_pandas, total_sweeps, QC_data, seal_parameter, capacitance_parameter_lower, capacitance_parameter_upper, access_parameter, access_switch, peak_current_parameter, SatMutVariantNames, output_dir, failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps)

    print('The total number of wells in which all sweeps failed were ' + str(num_failed))

    if analysis == 'Onset':
        pass_qc_data = np.array([])
        pass_qc_data = np.append(pass_qc_data, ['Number of Wells where all sweeps fail qc'])
        pass_qc_data = np.append(pass_qc_data, ['Total number of failed sweeps'])
        pass_qc_data = np.append(pass_qc_data, ['Fail Seal % Sweeps'])
        pass_qc_data = np.append(pass_qc_data, ['Fail Cap % Sweeps'])
        pass_qc_data = np.append(pass_qc_data, ['Fail Leak % Sweeps'])
        pass_qc_data = np.append(pass_qc_data, ['Fail Peak % Sweeps'])
        pass_qc_data = np.append(pass_qc_data, ['Seal Parameter (Ohms)'])
        pass_qc_data = np.append(pass_qc_data, ['Capacitance Lower Parameter (Farads)'])
        pass_qc_data = np.append(pass_qc_data, ['Capacitance Upper Parameter (Farads)'])
        pass_qc_data = np.append(pass_qc_data, ['Leak Range (pA)'])
        pass_qc_data = np.append(pass_qc_data, ['Peak Threshold Parameter (Amperes)'])

        percent_data = np.array([])
        percent_data = np.append(percent_data, [str(num_failed)])
        percent_data = np.append(percent_data, [str(total_fail_sweeps)])
        percent_data = np.append(percent_data, [str(100 * (failed_seal / total_fail_sweeps)) + '%'])
        percent_data = np.append(percent_data, [str(100 * (failed_cap / total_fail_sweeps)) + '%'])
        percent_data = np.append(percent_data, [str(100 * (failed_leak / total_fail_sweeps)) + '%'])
        percent_data = np.append(percent_data, [str(100 * (failed_peak / total_fail_sweeps)) + '%'])
        percent_data = np.append(percent_data, [str(seal_parameter)])
        percent_data = np.append(percent_data, [str(capacitance_parameter_lower)])
        percent_data = np.append(percent_data, [str(capacitance_parameter_upper)])
        percent_data = np.append(percent_data, ['(-100, 100)'])
        percent_data = np.append(percent_data, [str(peak_current_parameter)])

        pass_qc_data = np.vstack((pass_qc_data, percent_data))
        print(pass_qc_data)
    else:
        pass_qc_data = np.array([])
        pass_qc_data = np.append(pass_qc_data, ['Number of Wells where all sweeps fail qc'])
        pass_qc_data = np.append(pass_qc_data, ['Total number of failed sweeps'])
        pass_qc_data = np.append(pass_qc_data, ['Fail Seal % Sweeps'])
        pass_qc_data = np.append(pass_qc_data, ['Fail Cap % Sweeps'])
        pass_qc_data = np.append(pass_qc_data, ['Fail Leak % Sweeps'])
        pass_qc_data = np.append(pass_qc_data, ['Seal Parameter (Ohms)'])
        pass_qc_data = np.append(pass_qc_data, ['Capacitance Lower Parameter (Farads)'])
        pass_qc_data = np.append(pass_qc_data, ['Capacitance Upper Parameter (Farads)'])
        pass_qc_data = np.append(pass_qc_data, ['Leak Range (pA)'])

        percent_data = np.array([])
        percent_data = np.append(percent_data, [str(num_failed)])
        percent_data = np.append(percent_data, [str(total_fail_sweeps)])
        percent_data = np.append(percent_data, [str(100 * (failed_seal / total_fail_sweeps)) + '%'])
        percent_data = np.append(percent_data, [str(100 * (failed_cap / total_fail_sweeps)) + '%'])
        percent_data = np.append(percent_data, [str(100 * (failed_leak / total_fail_sweeps)) + '%'])
        percent_data = np.append(percent_data, [str(seal_parameter)])
        percent_data = np.append(percent_data, [str(capacitance_parameter_lower)])
        percent_data = np.append(percent_data, [str(capacitance_parameter_upper)])
        percent_data = np.append(percent_data, ['(-40, 40)'])

        pass_qc_data = np.vstack((pass_qc_data, percent_data))
        print(pass_qc_data)

    with open(qc_stats_file, mode='w') as stats_output:
        result_writer = csv.writer(stats_output, lineterminator='\n')
        for row in range(0, np.shape(pass_qc_data)[0]):
            result_writer.writerow(pass_qc_data[row])

    '''
    duration = 3000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
    '''


def main():
    # automate_quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('21022020_AN', 'hERG_ssDeact_3s_AN_13.37.49', 'hERG_ssDeact_3s_AN_13.37.49'), '21022020_AN', 'parameters_21022020_AN_hERG_ssDeact_3s_AN_13.37.49.csv', os.path.join('variant names', '21022020_AN.txt'), 18, 'ssDeact CD')
    print('automating plates')
    ## INSERT YOUR INPUTS HERE
    # quality_control_sat_mut_py(parent dir, data dir, plate name, QC file name, variant file path, num sweeps, protocol)


if __name__ == '__main__':
    main()
