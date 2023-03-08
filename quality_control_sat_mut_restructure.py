import os
import numpy as np
import csv
import shutil
import glob
import time
import statistics as sts
import matplotlib.pyplot as plt
#import winsound
import pandas as pd
import math


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

            while 1:
                changed_name = 0
                check = input(
                    'The selected file name already exists, do you wish to continue? If so data will be lost (yes/no):\n')
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
                if summary == 1:
                    if os.path.isfile(no_well_dir_name):
                        os.remove(no_well_dir_name)
        if summary == 1:
            return [dir_name, no_well_dir_name]
        else:
            return dir_name
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

    print(wellID)
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
        rawWellData = rawWellData.iloc[3:]
        # rawWellData = np.array(rawWellData)
        # rawWellData = pd.array(rawWellData)
        rawWellData = rawWellData.iloc[:, 1:]  # CHECK
    elif analysis == 'AP pre-stim' or analysis == 'mod FAIV':
        rawWellData = rawWellData[3:]
        # rawWellData = np.array(rawWellData)
        # rawWellData = .array(rawWellData)

        ###### FIXXXX PANDAS

        time_data = rawWellData[:, 1]
        current_data = rawWellData[:, 2:]
        time_data = time_data.transpose()

        # rawWellData = np.vstack((np.array(time_data), current_data.transpose()))
        rawWellData = np.vstack((pd.array(time_data), current_data.transpose()))
        rawWellData = rawWellData.transpose()
    else:
        # print(rawWellData)
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
        # print(min_time_point)

        point_two_time = min_time_point + 0.05
        # print(point_two_time)

        point_two_index = [i for i in range(0, len(neg_120mV_data)) if neg_120mV_time[i] >= point_two_time]

        try:
            point_two_value = neg_120mV_data[point_two_index[0]]
        except:
            return [failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps]

        ratio = point_two_value / min_value

        if ratio > 0.7:
            # print(wellID)
            # print('ratio fail')
            # print(ratio)
            # num_failed += 1
            return [failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps]

        if min_time_point > 1.215:
            # print(wellID)
            # print('too much capacitance')
            # num_failed += 1
            return [failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps]

    if analysis == 'ssAct' or analysis == 'ssDeact':
        if numpy_pandas == 'numpy':
            outputWellData = np.hstack(([0], rawWellData[:, 0]))
            outputWellData = np.append('Time_us', outputWellData)
            # print(outputWellData)
            # return
        else:
            outputWellData = pd.concat((pd.DataFrame([0]), rawWellData.iloc[:, 0]), axis=0)
            # print(outputWellData)
            outputWellData = pd.concat((pd.DataFrame(['Time_us']), outputWellData), axis=0)
            # print(outputWellData)
            # return
    else:
        if numpy_pandas == 'numpy':
            outputWellData = np.array([rawWellData[:, 0]])
            outputWellData = np.append('Time_us', outputWellData)
        else:
            outputWellData = rawWellData.iloc[:, 0]
            outputWellData = pd.concat((pd.DataFrame(['Time_us']), outputWellData), axis=0)

    passed_sweeps = 0

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

            if numpy_pandas == 'numpy':
                min_amp = min(np.array(rawWellData[tot_range_time_indx_list, sweep]).astype(float))
            else:
                min_amp = min(np.array(rawWellData.iloc[tot_range_time_indx_list, sweep]).astype(float))
            # print(max_amp)
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

            if access_switch == 1:
                if float(QC_data[well, access_index]) > float(access_parameter):
                    failed_access += 1
                    total_fail_sweeps += 1
                    continue

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

            if access_switch == 1:
                if float(QC_data.iloc[well, access_index]) > float(access_parameter):
                    failed_access += 1
                    total_fail_sweeps += 1
                    continue

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
                else:
                    result = rawWellData.iloc[:, sweep]
                    v_result = rawWellData.iloc[:, sweep - 1]

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
        print(result_file_path)
        outputWellData.to_csv(result_file_path, index=False, header=False)

    return [failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps]

        # return
# def quality_control_sat_mut_py(parent_path, parent_dir, qc_file, variant_name_file, total_sweeps, analysis, srvr_analysis):
def quality_control_sat_mut_py(parent_dir, data_dir, plate_name, qc_file, variant_name_file, total_sweeps, analysis):
    # STORE QC PARAMETER STATISTICS
    # STORE THE CD VALUES
    # parent_dir, data_dir, plate_name
    # seal_parameter = 1000E6

    numpy_pandas = 'pandas'

    if analysis == 'AP pre-stim':
        seal_parameter = 500E6
    else:
        seal_parameter = 300E6  # For ssAct, ssDeact, Onset

    # seal_parameter = float(input('Enter the magnitude required for the seal resistance quality (Ohms):\n'))
    # capacitance_parameter_upper = float(input('Enter the magnitude required for the capacitance UPPER limit (Farads):\n'))
    capacitance_parameter_upper = 50E-12
    # capacitance_parameter_lower = float(input('Enter the magnitude required for the capacitance LOWER limit (Farads):\n'))
    capacitance_parameter_lower = 5e-12

    access_switch = 0

    if analysis == 'Onset':
        # 50E6 now
        access_parameter = 20E6  # For onset
    else:
        access_parameter = 20E6  # For ssAct and Deact
        # access_parameter = 40E6

    # access_parameter = float(input('Enter the magnitude required for the access resistance (Ohms):\n'))
    # access_parameter = 20E6 #For ssAct and Deact
    # access_parameter = 15E6 #For onset
    if analysis == 'Onset':
        # peak_current_parameter = input('Enter the magnitude required for the peak control current (Amperes):\n')
        peak_current_parameter = 100E-12
    else:
        peak_current_parameter = math.nan
    # 50pA/pF for onset

    if analysis == 'ssDeact':
        result_parent_dir = 'Data Analysis Results ssDeact'
    elif analysis == 'ssAct':
        result_parent_dir = 'Data Analysis Results ssAct'
    elif analysis == 'Onset':
        result_parent_dir = 'Data Analysis Results Onset Inact'
    elif analysis == 'Nina':
        result_parent_dir = 'Data Analysis Results Pharm 40 Nina'
    else:
        print('Did not enter protocol tag correctly, aborting program.')
        return

    result_parent_dir = os.path.join(parent_dir, result_parent_dir)
    if not os.path.isdir(result_parent_dir):
        os.mkdir(result_parent_dir)
        output_parent_dir = os.path.join(result_parent_dir, plate_name)
        if not os.path.isdir(output_parent_dir):
            os.mkdir(output_parent_dir)
    else:
        output_parent_dir = os.path.join(result_parent_dir, plate_name)
        if not os.path.isdir(output_parent_dir):
            os.mkdir(output_parent_dir)

    output_dir = prompt_user(
        'What would you like to name the directory that stores the data files that pass quality control requirements?:\n',
        'dir', output_parent_dir, 0)
    # output_dir = os.path.join(output_parent_dir, 'success_QC no series resistance -120mV filtering')

    # output_dir = os.path.join(output_parent_dir, 'success_QC_test_pandas')
    qc_stats_file = prompt_user('What would you like to name the file that stores the quality control statistics?:\n',
                                'file', output_parent_dir, 0)
    # qc_stats_file = os.path.join(output_parent_dir, 'qc_statistics_test_pandas.csv')

    variant_name_file = os.path.join(parent_dir, variant_name_file)

    filename = os.path.join(parent_dir, data_dir, qc_file)

    print(output_dir)
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
    # print(QC_data)
    # return

    # Extract the mutant names
    SatMutVariantNames = []
    with open(variant_name_file) as var_file:
        for line in var_file:
            SatMutVariantNames.append(line)

    for var in range(0, len(SatMutVariantNames)):
        SatMutVariantNames[var] = SatMutVariantNames[var].replace(':', '_')
        SatMutVariantNames[var] = SatMutVariantNames[var].replace('\n', '')
        if SatMutVariantNames[var] == '':
            continue

        result_path = os.path.join(output_dir, SatMutVariantNames[var])
        print(result_path)
        os.mkdir(result_path)

    # print(QC_data.info())

    ###!!! pandas array access now required
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
    failed_access = 0
    failed_cap = 0
    failed_peak = 0
    failed_leak = 0
    total_fail_sweeps = 0

    print(num_wells)
    for well in range(0, num_wells):
        print(well)
        [failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps] = qc_well(well_names, well, parent_dir, data_dir, analysis, numpy_pandas, total_sweeps, QC_data, seal_parameter, capacitance_parameter_lower, capacitance_parameter_upper, access_parameter, access_switch, peak_current_parameter, SatMutVariantNames, output_dir, failed_leak, failed_seal, failed_cap, num_failed, failed_access, failed_peak, total_fail_sweeps)

    print('The total number of wells in which all sweeps failed were ' + str(num_failed))
    if analysis == 'Onset':
        pass_qc_data = np.array([])
        pass_qc_data = np.append(pass_qc_data, ['Number of Wells where all sweeps fail qc'])
        pass_qc_data = np.append(pass_qc_data, ['Total number of failed sweeps'])
        pass_qc_data = np.append(pass_qc_data, ['Fail Seal % Sweeps'])
        pass_qc_data = np.append(pass_qc_data, ['Fail Cap % Sweeps'])
        if access_switch == 1:
            pass_qc_data = np.append(pass_qc_data, ['Fail Access % Sweeps'])
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
        if access_switch == 1:
            percent_data = np.append(percent_data, [str(100 * (failed_access / total_fail_sweeps)) + '%'])
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
        if access_switch == 1:
            pass_qc_data = np.append(pass_qc_data, ['Fail Access % Sweeps'])
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
        if access_switch == 1:
            percent_data = np.append(percent_data, [str(100 * (failed_access / total_fail_sweeps)) + '%'])
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


def main():
    # quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch_WThERG'), os.path.join('22102020_AN', 'hERG_ssDeact_3s_AN_12.31.17', 'hERG_ssDeact_3s_AN_12.31.17'), '22102020_AN', 'parameters_22102020_AN_hERG_ssDeact_3s_AN_12.31.17.csv', os.path.join('variant names', '22102020_AN.txt'), 18, 'ssDeact', 'numpy')

    # quality_control_sat_mut_py(os.path.join('Z://', 'SyncroPatch_validation'), os.path.join('25032021_CJ', 'hERG_ssAct_1s_AN_14.35.42', 'hERG_ssAct_1s_AN_14.35.42'), '25032021_CJ', 'parameters_hERG_ssAct_1s_AN_14.35.42.csv', os.path.join('variant names', '25032021_CJ.txt'), 13, 'ssAct')

    # quality_control_sat_mut_py(os.path.join('N://', 'Syncropatch'), os.path.join('22102020_AN', 'hERG_ssAct_1s_AN_12.26.22', 'hERG_ssAct_1s_AN_12.26.22'), '22102020_AN', 'parameters_22102020_AN_hERG_ssAct_1s_AN_12.26.22.csv', os.path.join('variant names', '22102020_AN.txt'), 13, 'ssAct')

    # quality_control_sat_mut_py(os.path.join('N://', 'Synchropatch'), os.path.join('n2_14_cpds', 'hERG_Pharm_40_Nina_16.25.57', '210401'), 'n2_14_cpds', 'all_sweeps.csv', os.path.join('n2_14_cpds', 'well_data.txt'), 75, 'Nina')
    # quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('03102019_AN', 'hERG_Inact_Onset_AN_13.00.30', 'hERG_Inact_Onset_AN_13.00.30'), '03102019_AN', 'parameters_03102019_AN_hERG_Inact_Onset_AN_13.00.30.csv', os.path.join('variant names', '03102019_AN.txt'), 12, 'Onset')

    # quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('06082020_AN', 'hERG_ssDeact_3s_AN_12.41.11', 'hERG_ssDeact_3s_AN_12.41.11'), '06082020_AN', 'parameters_06082020_AN_hERG_ssDeact_3s_AN_12.41.11.csv', os.path.join('variant names', '06082020_AN.txt'), 12, 'ssDeact Fit')
    # quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('22102020_AN2', 'hERG_ssDeact_3s_AN_13.13.24', 'hERG_ssDeact_3s_AN_13.13.24'), '22102020_AN2', 'parameters_22102020_AN2_hERG_ssDeact_3s_AN_13.13.24.csv', os.path.join('variant names', '22102020_AN2.txt'), 12, 'ssDeact Fit')

    # quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('12052021_AN', 'hERG_ssDeact_3s_AN_13.12.03', 'hERG_ssDeact_3s_AN_13.12.03'), '12052021_AN', 'parameters_12052021_AN_hERG_ssDeact_3s_AN_13.12.03.csv', os.path.join('variant names', '12052021_AN.txt'), 18, 'ssDeact')

    # quality_control_sat_mut_py(os.path.join('Z://', 'SyncroPatch_validation'), os.path.join('27052021_CJ2', 'hERG_ssDeact_3s_AN_15.36.13', '210802'), '27052021_CJ2', 'parameters_hERG_ssDeact_3s_AN_15.36.13.csv', os.path.join('variant names', '20210527_CJ.txt'), 18, 'ssDeact', 'pandas')

    # quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('10102019_AN2', 'hERG_ssAct_1s_AN_14.19.06', 'hERG_ssAct_1s_AN_14.19.06_Rectified file order'), '10102019_AN2', 'parameters_10102019_AN2_hERG_ssAct_1s_AN_14.19.06.csv', os.path.join('variant names', '10102019_AN2.txt'), 13, 'ssAct', 'pandas')

    # quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('10102019_AN2', 'hERG_Inact_Onset_AN_14.16.36', 'hERG_Inact_Onset_AN_14.16.36'), '10102019_AN2', 'parameters_10102019_AN2_hERG_Inact_Onset_AN_14.16.36.csv', os.path.join('variant names', '10102019_AN2.txt'), 12, 'Onset', 'pandas')

    #quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('01092022_AN', 'hERG_ssDeact_3s_AN_11.45.32', 'parameters_01092022_AN_hERG_ssDeact_3s_AN_11.45.32.csv'), os.path.join('variant names', '01092022_AN.txt'), 18, 'ssDeact', 'pandas')

    #parent_dir, data_dir, plate_name, qc_file, variant_name_file, total_sweeps, analysis
    quality_control_sat_mut_py(os.path.join('/mnt','syncropatch','Clinical_variant_Brett'), os.path.join('01092022_AN', 'hERG_ssDeact_3s_AN_11.45.32', 'hERG_ssDeact_3s_AN_11.45.32'), '01092022_AN', 'parameters_01092022_AN_hERG_ssDeact_3s_AN_11.45.32.csv', os.path.join('variant names', '01092022_AN.txt'), 18, 'ssDeact')

    #quality_control_sat_mut_py(os.path.join('Z://', 'Functional_Genomics_Syncropatch', 'KCNH2', 'Tris-HCl'), os.path.join('16122021_AN', 'hERG_ssDeact_3s_AN_14.07.31', 'hERG_ssDeact_3s_AN_14.07.31'), '16122021_AN', 'parameters_16122021_AN_hERG_ssDeact_3s_AN_14.07.31.csv', os.path.join('variant names', '16122021_AN.txt'), 18, 'ssDeact', 'pandas')

    # quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('03102019_AN', 'hERG_Inact_Onset_AN_13.00.30', 'hERG_Inact_Onset_AN_13.00.30'), '03102019_AN', 'parameters_03102019_AN_hERG_Inact_Onset_AN_13.00.30.csv', os.path.join('variant names', '03102019_AN.txt'), 12, 'Onset')

    '''
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('03102019_AN2', 'hERG_Inact_Onset_AN_13.51.43', 'hERG_Inact_Onset_AN_13.51.43'), '03102019_AN2', 'parameters_03102019_AN2_hERG_Inact_Onset_AN_13.51.43.csv', os.path.join('variant names', '03102019_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('04062020_AN3', 'hERG_Inact_Onset_AN_15.52.46', 'hERG_Inact_Onset_AN_15.52.46'), '04062020_AN3', 'parameters_04062020_AN3_hERG_Inact_Onset_AN_15.52.46.csv', os.path.join('variant names', '04062020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('04062020_AN4', 'hERG_Inact_Onset_AN_16.40.51', 'hERG_Inact_Onset_AN_16.40.51'), '04062020_AN4', 'parameters_04062020_AN4_hERG_Inact_Onset_AN_16.40.51.csv', os.path.join('variant names', '04062020_AN4.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('05032020_AN', 'hERG_Inact_Onset_AN_13.41.07','hERG_Inact_Onset_AN_13.41.07'), '05032020_AN','parameters_05032020_AN_hERG_Inact_Onset_AN_13.41.07.csv',os.path.join('variant names', '05032020_AN.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('05032020_AN2', 'hERG_Inact_Onset_AN_14.26.24', 'hERG_Inact_Onset_AN_14.26.24'), '05032020_AN2', 'parameters_05032020_AN2_hERG_Inact_Onset_AN_14.26.24.csv', os.path.join('variant names', '05032020_AN2.txt'), 12, 'Onset')


    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('05092019_AN2', 'hERG_Inact_Onset_AN_16.05.02', 'hERG_Inact_Onset_AN_16.05.02'), '05092019_AN2', 'parameters_05092019_AN2_hERG_Inact_Onset_AN_16.05.02.csv', os.path.join('variant names', '05092019_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('05122019_AN', 'hERG_Inact_Onset_AN_14.27.52', 'hERG_Inact_Onset_AN_14.27.52'), '05122019_AN', 'parameters_05122019_AN_hERG_Inact_Onset_AN_14.27.52.csv', os.path.join('variant names', '05122019_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('05122019_AN2', 'hERG_Inact_Onset_AN_15.30.02', 'hERG_Inact_Onset_AN_15.30.02'), '05122019_AN2', 'parameters_05122019_AN2_hERG_Inact_Onset_AN_15.30.02.csv', os.path.join('variant names', '05122019_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('07052020_AN2', 'hERG_Inact_Onset_AN_14.29.34', 'hERG_Inact_Onset_AN_14.29.34'), '07052020_AN2', 'parameters_07052020_AN2_hERG_Inact_Onset_AN_14.29.34.csv', os.path.join('variant names', '07052020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('07052020_AN', 'hERG_Inact_Onset_AN_13.34.15', 'hERG_Inact_Onset_AN_13.34.15'), '07052020_AN', 'parameters_07052020_AN_hERG_Inact_Onset_AN_13.34.15.csv', os.path.join('variant names', '07052020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('10102019_AN', 'hERG_Inact_Onset_AN_13.31.17', 'hERG_Inact_Onset_AN_13.31.17'), '10102019_AN', 'parameters_10102019_AN_hERG_Inact_Onset_AN_13.31.17.csv', os.path.join('variant names', '10102019_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('10102019_AN2', 'hERG_Inact_Onset_AN_14.16.36', 'hERG_Inact_Onset_AN_14.16.36'), '10102019_AN2', 'parameters_10102019_AN2_hERG_Inact_Onset_AN_14.16.36.csv', os.path.join('variant names', '10102019_AN2.txt'), 12, 'Onset')


    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('12032020_AN', 'hERG_Inact_Onset_AN_13.37.19', 'hERG_Inact_Onset_AN_13.37.19'), '12032020_AN', 'parameters_12032020_AN_hERG_Inact_Onset_AN_13.37.19.csv', os.path.join('variant names', '12032020_AN.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('12032020_AN2', 'hERG_Inact_Onset_AN_14.39.11', 'hERG_Inact_Onset_AN_14.39.11'), '12032020_AN2', 'parameters_12032020_AN2_hERG_Inact_Onset_AN_14.39.11.csv', os.path.join('variant names', '12032020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('12092019_AN2', 'hERG_Inact_Onset_AN_14.32.59', 'hERG_Inact_Onset_AN_14.32.59'), '12092019_AN2', 'parameters_12092019_AN2_hERG_Inact_Onset_AN_14.32.59.csv', os.path.join('variant names', '12092019_AN2.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('12122019_AN', 'hERG_Inact_Onset_AN_13.23.49', 'hERG_Inact_Onset_AN_13.23.49'), '12122019_AN', 'parameters_12122019_AN_hERG_Inact_Onset_AN_13.23.49.csv', os.path.join('variant names', '12122019_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('12122019_AN2', 'hERG_Inact_Onset_AN_14.13.39', 'hERG_Inact_Onset_AN_14.13.39'), '12122019_AN2', 'parameters_12122019_AN2_hERG_Inact_Onset_AN_14.13.39.csv', os.path.join('variant names', '12122019_AN2.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('13022020_AN', 'hERG_Inact_Onset_AN_13.33.42', 'hERG_Inact_Onset_AN_13.33.42'), '13022020_AN', 'parameters_13022020_AN_hERG_Inact_Onset_AN_13.33.42.csv', os.path.join('variant names', '13022020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('13022020_AN2', 'hERG_Inact_Onset_AN_14.23.59', 'hERG_Inact_Onset_AN_14.23.59'), '13022020_AN2', 'parameters_13022020_AN2_hERG_Inact_Onset_AN_14.23.59.csv', os.path.join('variant names', '13022020_AN2.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('14032019_AN', 'hERG_Inact_Onset_13.21.29', '201026'), '14032019_AN', 'parameters_20190314MPAN_hERG_Inact_Onset_13.21.29.csv', os.path.join('variant names', '14032019_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('14032019_AN2', 'hERG_Inact_Onset_14.15.31', '201026'), '14032019_AN2', 'parameters_20190314MPAN2_hERG_Inact_Onset_14.15.31.csv', os.path.join('variant names', '14032019_AN2.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('14052020_AN', 'hERG_Inact_Onset_AN_13.17.47', 'hERG_Inact_Onset_AN_13.17.47'), '14052020_AN', 'parameters_14052020_AN_hERG_Inact_Onset_AN_13.17.47.csv', os.path.join('variant names', '14052020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('14052020_AN2', 'hERG_Inact_Onset_AN_14.17.29', 'hERG_Inact_Onset_AN_14.17.29'), '14052020_AN2', 'parameters_14052020_AN2_hERG_Inact_Onset_AN_14.17.29.csv', os.path.join('variant names', '14052020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('14052020_AN3', 'hERG_Inact_Onset_AN_15.42.39', 'hERG_Inact_Onset_AN_15.42.39'), '14052020_AN3', 'parameters_14052020_AN3_hERG_Inact_Onset_AN_15.42.39.csv', os.path.join('variant names', '14052020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('14052020_AN4', 'hERG_Inact_Onset_AN_16.33.49', 'hERG_Inact_Onset_AN_16.33.49'), '14052020_AN4', 'parameters_14052020_AN4_hERG_Inact_Onset_AN_16.33.49.csv', os.path.join('variant names', '14052020_AN4.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('16042020_AN', 'hERG_Inact_Onset_AN_13.46.58', 'hERG_Inact_Onset_AN_13.46.58'), '16042020_AN', 'parameters_16042020_AN_hERG_Inact_Onset_AN_13.46.58.csv',  os.path.join('variant names', '16042020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('16042020_AN2', 'hERG_Inact_Onset_AN_14.37.25', 'hERG_Inact_Onset_AN_14.37.25'), '16042020_AN2', 'parameters_16042020_AN2_hERG_Inact_Onset_AN_14.37.25.csv', os.path.join('variant names', '16042020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('17102019_AN', 'hERG_Inact_Onset_AN_13.26.12', 'hERG_Inact_Onset_AN_13.26.12'), '17102019_AN', 'parameters_17102019_AN_hERG_Inact_Onset_AN_13.26.12.csv', os.path.join('variant names', '17102019_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('17102019_AN2', 'hERG_Inact_Onset_AN_14.24.07', 'hERG_Inact_Onset_AN_14.24.07'), '17102019_AN2', 'parameters_17102019_AN2_hERG_Inact_Onset_AN_14.24.07.csv', os.path.join('variant names', '17102019_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('19092019_AN', 'hERG_Inact_Onset_AN_13.45.46', 'hERG_Inact_Onset_AN_13.45.46'), '19092019_AN', 'parameters_19092019_AN_hERG_Inact_Onset_AN_13.45.46.csv', os.path.join('variant names', '19092019_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('19092019_AN2', 'hERG_Inact_Onset_AN_14.40.05', 'hERG_Inact_Onset_AN_14.40.05'), '19092019_AN2', 'parameters_19092019_AN2_hERG_Inact_Onset_AN_14.40.05.csv', os.path.join('variant names', '19092019_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('21022020_AN', 'hERG_Inact_Onset_AN_13.35.19', 'hERG_Inact_Onset_AN_13.35.19'), '21022020_AN', 'parameters_21022020_AN_hERG_Inact_Onset_AN_13.35.19.csv', os.path.join('variant names', '21022020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('21022020_AN2', 'hERG_Inact_Onset_AN_14.51.21', 'hERG_Inact_Onset_AN_14.51.21'), '21022020_AN2', 'parameters_21022020_AN2_hERG_Inact_Onset_AN_14.51.21.csv', os.path.join('variant names', '21022020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('21052020_AN', 'hERG_Inact_Onset_AN_13.00.53', 'hERG_Inact_Onset_AN_13.00.53'), '21052020_AN', 'parameters_21052020_AN_hERG_Inact_Onset_AN_13.00.53.csv', os.path.join('variant names', '21052020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('21052020_AN2', 'hERG_Inact_Onset_AN_14.05.58', 'hERG_Inact_Onset_AN_14.05.58'), '21052020_AN2', 'parameters_21052020_AN2_hERG_Inact_Onset_AN_14.05.58.csv', os.path.join('variant names', '21052020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('21052020_AN3', 'hERG_Inact_Onset_AN_15.49.47', 'hERG_Inact_Onset_AN_15.49.47'), '21052020_AN3', 'parameters_21052020_AN3_hERG_Inact_Onset_AN_15.49.47.csv', os.path.join('variant names', '21052020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('21052020_AN4', 'hERG_Inact_Onset_AN_16.35.34', 'hERG_Inact_Onset_AN_16.35.34'), '21052020_AN4', 'parameters_21052020_AN4_hERG_Inact_Onset_AN_16.35.34.csv', os.path.join('variant names', '21052020_AN4.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('21112019_AN', 'hERG_Inact_Onset_AN_12.57.01', 'hERG_Inact_Onset_AN_12.57.01'), '21112019_AN', 'parameters_21112019_AN_hERG_Inact_Onset_AN_12.57.01.csv', os.path.join('variant names', '21112019_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('21112019_AN2', 'hERG_Inact_Onset_AN_13.45.14', 'hERG_Inact_Onset_AN_13.45.14'), '21112019_AN2', 'parameters_21112019_AN2_hERG_Inact_Onset_AN_13.45.14.csv', os.path.join('variant names', '21112019_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('24102019_AN', 'hERG_Inact_Onset_AN_13.34.20', 'hERG_Inact_Onset_AN_13.34.20'), '24102019_AN', 'parameters_24102019_AN_hERG_Inact_Onset_AN_13.34.20.csv', os.path.join('variant names', '24102019_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('24102019_AN2', 'hERG_Inact_Onset_AN_14.28.03', 'hERG_Inact_Onset_AN_14.28.03'), '24102019_AN2', 'parameters_24102019_AN2_hERG_Inact_Onset_AN_14.28.03.csv', os.path.join('variant names', '24102019_AN2.txt'), 12, 'Onset')
    '''
    '''
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('26092019_AN', 'hERG_Inact_Onset_AN_13.03.24', 'hERG_Inact_Onset_AN_13.03'), '26092019_AN', 'parameters_26092019_AN_hERG_Inact_Onset_AN_13.03.24.csv', os.path.join('variant names', '26092019_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('26092019_AN2', 'hERG_Inact_Onset_AN_14.05.52', 'hERG_Inact_Onset_AN_14.05.52'), '26092019_AN2', 'parameters_26092019_AN2_hERG_Inact_Onset_AN_14.05.52.csv', os.path.join('variant names', '26092019_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('27022020_AN', 'hERG_Inact_Onset_AN_13.08.00', 'hERG_Inact_Onset_AN_13.08.00'), '27022020_AN', 'parameters_27022020_AN_hERG_Inact_Onset_AN_13.08.00.csv', os.path.join('variant names', '27022020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('27022020_AN2', 'hERG_Inact_Onset_AN_14.20.14', 'hERG_Inact_Onset_AN_14.20.14'), '27022020_AN2', 'parameters_27022020_AN2_hERG_Inact_Onset_AN_14.20.14.csv',os.path.join('variant names', '27022020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('28052020_AN', 'hERG_Inact_Onset_AN_12.28.04', 'hERG_Inact_Onset_AN_12.28.04'), '28052020_AN', 'parameters_28052020_AN_hERG_Inact_Onset_AN_12.28.04.csv', os.path.join('variant names', '28052020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('28052020_AN2', 'hERG_Inact_Onset_AN_13.20.01', 'hERG_Inact_Onset_AN_13.20.01'), '28052020_AN2', 'parameters_28052020_AN2_hERG_Inact_Onset_AN_13.20.01.csv', os.path.join('variant names', '28052020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('28052020_AN3', 'hERG_Inact_Onset_AN_15.35.01', 'hERG_Inact_Onset_AN_15.35.01'), '28052020_AN3', 'parameters_28052020_AN3_hERG_Inact_Onset_AN_15.35.01.csv', os.path.join('variant names', '28052020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('28052020_AN4', 'hERG_Inact_Onset_AN_16.23.18', 'hERG_Inact_Onset_AN_16.23.18'), '28052020_AN4', 'parameters_28052020_AN4_hERG_Inact_Onset_AN_16.23.18.csv', os.path.join('variant names', '28052020_AN4.txt'), 12, 'Onset')

    '''
    '''
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('02072020_AN', 'hERG_Inact_Onset_AN_12.27.41', 'hERG_Inact_Onset_AN_12.27.41'), '02072020_AN', 'parameters_02072020_AN_hERG_Inact_Onset_AN_12.27.41.csv', os.path.join('variant names', '02072020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('02072020_AN2', 'hERG_Inact_Onset_AN_13.34.02', 'hERG_Inact_Onset_AN_13.34.02'), '02072020_AN2', 'parameters_02072020_AN2_hERG_Inact_Onset_AN_13.34.02.csv', os.path.join('variant names', '02072020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('02072020_AN3', 'hERG_Inact_Onset_AN_15.10.01', 'hERG_Inact_Onset_AN_15.10.01'), '02072020_AN3', 'parameters_02072020_AN3_hERG_Inact_Onset_AN_15.10.01.csv', os.path.join('variant names', '02072020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('02072020_AN4', 'hERG_Inact_Onset_AN_15.54.38', 'hERG_Inact_Onset_AN_15.54.38'), '02072020_AN4', 'parameters_02072020_AN4_hERG_Inact_Onset_AN_15.54.38.csv', os.path.join('variant names', '02072020_AN4.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('03092020_AN', 'hERG_Inact_Onset_AN_13.26.42', 'hERG_Inact_Onset_AN_13.26.42'), '03092020_AN', 'parameters_03092020_AN_hERG_Inact_Onset_AN_13.26.42.csv', os.path.join('variant names', '03092020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('03092020_AN2', 'hERG_Inact_Onset_AN_14.12.24', 'hERG_Inact_Onset_AN_14.12.24'), '03092020_AN2', 'parameters_03092020_AN2_hERG_Inact_Onset_AN_14.12.24.csv', os.path.join('variant names', '03092020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('06082020_AN', 'hERG_Inact_Onset_AN_12.38.40', 'hERG_Inact_Onset_AN_12.38.40'), '06082020_AN', 'parameters_06082020_AN_hERG_Inact_Onset_AN_12.38.40.csv', os.path.join('variant names', '06082020_AN.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('06082020_AN2', 'hERG_Inact_Onset_AN_13.23.10','hERG_Inact_Onset_AN_13.23.10'), '06082020_AN2','parameters_06082020_AN2_hERG_Inact_Onset_AN_13.23.10.csv',os.path.join('variant names', '06082020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('06082020_AN3', 'hERG_Inact_Onset_AN_15.13.55', 'hERG_Inact_Onset_AN_15.13.55'), '06082020_AN3', 'parameters_06082020_AN3_hERG_Inact_Onset_AN_15.13.55.csv', os.path.join('variant names', '06082020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('06082020_AN4', 'hERG_Inact_Onset_AN_15.59.29', 'hERG_Inact_Onset_AN_15.59.29'), '06082020_AN4', 'parameters_06082020_AN4_hERG_Inact_Onset_AN_15.59.29.csv', os.path.join('variant names', '06082020_AN4.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('09072020_AN', 'hERG_Inact_Onset_AN_12.22.18', 'hERG_Inact_Onset_AN_12.22.18'), '09072020_AN', 'parameters_09072020_AN_hERG_Inact_Onset_AN_12.22.18.csv', os.path.join('variant names', '09072020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('09072020_AN2', 'hERG_Inact_Onset_AN_13.26.18', 'hERG_Inact_Onset_AN_13.26.18'), '09072020_AN2', 'parameters_09072020_AN2_hERG_Inact_Onset_AN_13.26.18.csv', os.path.join('variant names', '09072020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('09072020_AN3', 'hERG_Inact_Onset_AN_15.13.26', 'hERG_Inact_Onset_AN_15.13.26'), '09072020_AN3', 'parameters_09072020_AN3_hERG_Inact_Onset_AN_15.13.26.csv', os.path.join('variant names', '09072020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('09072020_AN4', 'hERG_Inact_Onset_AN_15.58.32', 'hERG_Inact_Onset_AN_15.58.32'), '09072020_AN4', 'parameters_09072020_AN4_hERG_Inact_Onset_AN_15.58.32.csv', os.path.join('variant names', '09072020_AN4.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('13082020_AN', 'hERG_Inact_Onset_AN_12.55.19', 'hERG_Inact_Onset_AN_12.55.19'), '13082020_AN', 'parameters_13082020_AN_hERG_Inact_Onset_AN_12.55.19.csv', os.path.join('variant names', '13082020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('13082020_AN2', 'hERG_Inact_Onset_AN_13.39.28', 'hERG_Inact_Onset_AN_13.39.28'), '13082020_AN2', 'parameters_13082020_AN2_hERG_Inact_Onset_AN_13.39.28.csv', os.path.join('variant names', '13082020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('13082020_AN3', 'hERG_Inact_Onset_AN_15.06.56', 'hERG_Inact_Onset_AN_15.06.56'), '13082020_AN3', 'parameters_13082020_AN3_hERG_Inact_Onset_AN_15.06.56.csv', os.path.join('variant names', '13082020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('13082020_AN4', 'hERG_Inact_Onset_AN_15.53.33', 'hERG_Inact_Onset_AN_15.53.33'), '13082020_AN4', 'parameters_13082020_AN4_hERG_Inact_Onset_AN_15.53.33.csv', os.path.join('variant names', '13082020_AN4.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('16072020_AN', 'hERG_Inact_Onset_AN_12.06.19', 'hERG_Inact_Onset_AN_12.06.19'), '16072020_AN', 'parameters_16072020_AN_hERG_Inact_Onset_AN_12.06.19.csv', os.path.join('variant names', '16072020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('16072020_AN2', 'hERG_Inact_Onset_AN_13.18.20', 'hERG_Inact_Onset_AN_13.18.20'), '16072020_AN2', 'parameters_16072020_AN2_hERG_Inact_Onset_AN_13.18.20.csv', os.path.join('variant names', '16072020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('16072020_AN3', 'hERG_Inact_Onset_AN_14.58.26', 'hERG_Inact_Onset_AN_14.58.26'), '16072020_AN3', 'parameters_16072020_AN3_hERG_Inact_Onset_AN_14.58.26.csv', os.path.join('variant names', '16072020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('16072020_AN4', 'hERG_Inact_Onset_AN_15.45.35', 'hERG_Inact_Onset_AN_15.45.35'), '16072020_AN4', 'parameters_16072020_AN4_hERG_Inact_Onset_AN_15.45.35.csv', os.path.join('variant names', '16072020_AN4.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('20082020_AN', 'hERG_Inact_Onset_AN_16.08.41', 'hERG_Inact_Onset_AN_16.08.41'), '20082020_AN', 'parameters_20082020_AN_hERG_Inact_Onset_AN_16.08.41.csv', os.path.join('variant names', '20082020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('20082020_AN2', 'hERG_Inact_Onset_AN_16.52.32', 'hERG_Inact_Onset_AN_16.52.32'), '20082020_AN2', 'parameters_20082020_AN2_hERG_Inact_Onset_AN_16.52.32.csv', os.path.join('variant names', '20082020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('20082020_AN3', 'hERG_Inact_Onset_AN_18.05.18', 'hERG_Inact_Onset_AN_18.05.18'), '20082020_AN3', 'parameters_20082020_AN3_hERG_Inact_Onset_AN_18.05.18.csv', os.path.join('variant names', '20082020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('20082020_AN4', 'hERG_Inact_Onset_AN_18.49.59', 'hERG_Inact_Onset_AN_18.49.59'), '20082020_AN4', 'parameters_20082020_AN4_hERG_Inact_Onset_AN_18.49.59.csv', os.path.join('variant names', '20082020_AN4.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('23072020_AN', 'hERG_Inact_Onset_AN_12.33.02', 'hERG_Inact_Onset_AN_12.33.02'), '23072020_AN', 'parameters_23072020_AN_hERG_Inact_Onset_AN_12.33.02.csv', os.path.join('variant names', '23072020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('23072020_AN2', 'hERG_Inact_Onset_AN_13.43.49', 'hERG_Inact_Onset_AN_13.43.49'), '23072020_AN2', 'parameters_23072020_AN2_hERG_Inact_Onset_AN_13.43.49.csv', os.path.join('variant names', '23072020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('23072020_AN3', 'hERG_Inact_Onset_AN_15.03.25', 'hERG_Inact_Onset_AN_15.03.25'), '23072020_AN3', 'parameters_23072020_AN3_hERG_Inact_Onset_AN_15.03.25.csv', os.path.join('variant names', '23072020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('23072020_AN4', 'hERG_Inact_Onset_AN_15.48.22', 'hERG_Inact_Onset_AN_15.48.22'), '23072020_AN4', 'parameters_23072020_AN4_hERG_Inact_Onset_AN_15.48.22.csv', os.path.join('variant names', '23072020_AN4.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('27082020_AN', 'hERG_Inact_Onset_AN_12.45.30', 'hERG_Inact_Onset_AN_12.45.30'), '27082020_AN', 'parameters_27082020_AN_hERG_Inact_Onset_AN_12.45.30.csv', os.path.join('variant names', '27082020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('27082020_AN2', 'hERG_Inact_Onset_AN_13.30.28', 'hERG_Inact_Onset_AN_13.30.28'), '27082020_AN2', 'parameters_27082020_AN2_hERG_Inact_Onset_AN_13.30.28.csv', os.path.join('variant names', '27082020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('27082020_AN3', 'hERG_Inact_Onset_AN_14.59.42', 'hERG_Inact_Onset_AN_14.59.42'), '27082020_AN3', 'parameters_27082020_AN3_hERG_Inact_Onset_AN_14.59.42.csv', os.path.join('variant names', '27082020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('27082020_AN4', 'hERG_Inact_Onset_AN_15.44.49', 'hERG_Inact_Onset_AN_15.44.49'), '27082020_AN4', 'parameters_27082020_AN4_hERG_Inact_Onset_AN_15.44.49.csv', os.path.join('variant names', '27082020_AN4.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('30072020_AN', 'hERG_Inact_Onset_AN_12.38.15', 'hERG_Inact_Onset_AN_12.38.15'), '30072020_AN', 'parameters_30072020_AN_hERG_Inact_Onset_AN_12.38.15.csv', os.path.join('variant names', '30072020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('30072020_AN2', 'hERG_Inact_Onset_AN_13.43.52', 'hERG_Inact_Onset_AN_13.43.52'), '30072020_AN2', 'parameters_30072020_AN2_hERG_Inact_Onset_AN_13.43.52.csv', os.path.join('variant names', '30072020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('30072020_AN3', 'hERG_Inact_Onset_AN_15.08.18', 'hERG_Inact_Onset_AN_15.08.18'), '30072020_AN3', 'parameters_30072020_AN3_hERG_Inact_Onset_AN_15.08.18.csv', os.path.join('variant names', '30072020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('30072020_AN4', 'hERG_Inact_Onset_AN_16.00.29', 'hERG_Inact_Onset_AN_16.00.29'), '30072020_AN4', 'parameters_30072020_AN4_hERG_Inact_Onset_AN_16.00.29.csv', os.path.join('variant names', '30072020_AN4.txt'), 12, 'Onset')
    '''
    '''

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('22102020_AN', 'hERG_Inact_Onset_AN_12.28.46', 'hERG_Inact_Onset_AN_12.28.46'), '22102020_AN', 'parameters_22102020_AN_hERG_Inact_Onset_AN_12.28.46.csv', os.path.join('variant names', '22102020_AN.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('22102020_AN2', 'hERG_Inact_Onset_AN_13.10.57', 'hERG_Inact_Onset_AN_13.10.57'), '22102020_AN2', 'parameters_22102020_AN2_hERG_Inact_Onset_AN_13.10.57.csv', os.path.join('variant names', '22102020_AN2.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('22102020_AN3', 'hERG_Inact_Onset_AN_15.08.28', 'hERG_Inact_Onset_AN_15.08.28'), '22102020_AN3', 'parameters_22102020_AN3_hERG_Inact_Onset_AN_15.08.28.csv', os.path.join('variant names', '22102020_AN3.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('22102020_AN4', 'hERG_Inact_Onset_AN_15.44.37', 'hERG_Inact_Onset_AN_15.44.37'), '22102020_AN4', 'parameters_22102020_AN4_hERG_Inact_Onset_AN_15.44.37.csv', os.path.join('variant names', '22102020_AN4.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('30042020_AN2', 'hERG_Inact_Onset_AN_14.27.27', 'hERG_Inact_Onset_AN_14.27.27'), '30042020_AN2', 'parameters_30042020_AN2_hERG_Inact_Onset_AN_14.27.27.csv', os.path.join('variant names', '30042020_AN2.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('29102020_AN', 'hERG_Inact_Onset_AN_15.43.50', 'hERG_Inact_Onset_AN_15.43.50'), '29102020_AN', 'parameters_29102020_AN_hERG_Inact_Onset_AN_15.43.50.csv', os.path.join('variant names', '29102020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('29102020_AN2', 'hERG_Inact_Onset_AN_16.20.19', 'hERG_Inact_Onset_AN_16.20.19'), '29102020_AN2', 'parameters_29102020_AN2_hERG_Inact_Onset_AN_16.20.19.csv', os.path.join('variant names', '29102020_AN2.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('05112020_AN', 'hERG_Inact_Onset_AN_12.16.19', 'hERG_Inact_Onset_AN_12.16.19'), '05112020_AN', 'parameters_05112020_AN_hERG_Inact_Onset_AN_12.16.19.csv', os.path.join('variant names', '05112020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('05112020_AN2', 'hERG_Inact_Onset_AN_12.49.44', 'hERG_Inact_Onset_AN_12.49.44'), '05112020_AN2', 'parameters_05112020_AN2_hERG_Inact_Onset_AN_12.49.44.csv', os.path.join('variant names', '05112020_AN2.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('04062020_AN', 'hERG_Inact_Onset_AN_13.07.16', 'hERG_Inact_Onset_AN_13.07.16'), '04062020_AN', 'parameters_04062020_AN_hERG_Inact_Onset_AN_13.07.16.csv', os.path.join('variant names', '04062020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('04062020_AN2', 'hERG_Inact_Onset_AN_14.13.59', 'hERG_Inact_Onset_AN_14.13.59'), '04062020_AN2', 'parameters_04062020_AN2_hERG_Inact_Onset_AN_14.13.59.csv', os.path.join('variant names', '04062020_AN2.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('07052020_AN3', 'hERG_Inact_Onset_AN_15.38.50', 'hERG_Inact_Onset_AN_15.38.50'), '07052020_AN3', 'parameters_07052020_AN3_hERG_Inact_Onset_AN_15.38.50.csv', os.path.join('variant names', '07052020_AN3.txt'), 12, 'Onset')


    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('23042020_AN', 'hERG_Inact_Onset_AN_13.25.58', 'hERG_Inact_Onset_AN_13.25.58'), '23042020_AN', 'parameters_23042020_AN_hERG_Inact_Onset_AN_13.25.58.csv', os.path.join('variant names', '23042020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('23042020_AN2', 'hERG_Inact_Onset_AN_14.19.43', 'hERG_Inact_Onset_AN_14.19.43'), '23042020_AN2', 'parameters_23042020_AN2_hERG_Inact_Onset_AN_14.19.43.csv', os.path.join('variant names', '23042020_AN2.txt'), 12, 'Onset')

    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('30042020_AN', 'hERG_Inact_Onset_AN_13.29.40', 'hERG_Inact_Onset_AN_13.29.40'), '30042020_AN', 'parameters_30042020_AN_hERG_Inact_Onset_AN_13.29.40.csv', os.path.join('variant names', '30042020_AN.txt'), 12, 'Onset')
    quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch'), os.path.join('30042020_AN2', 'hERG_Inact_Onset_AN_14.27.27', 'hERG_Inact_Onset_AN_14.27.27'), '30042020_AN2', 'parameters_30042020_AN2_hERG_Inact_Onset_AN_14.27.27.csv', os.path.join('variant names', '30042020_AN2.txt'), 12, 'Onset')


    #quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch_WThERG'), os.path.join('22102020_AN', 'hERG_ssAct_1s_AN_12.26.22', 'hERG_ssAct_1s_AN_12.26.22'), '22102020_AN', 'parameters_22102020_AN_hERG_ssAct_1s_AN_12.26.22.csv', os.path.join('variant names', '22102020_AN.txt'), 13, 'ssAct')

    #quality_control_sat_mut_py(os.path.join('Z://', 'Syncropatch_WThERG'), os.path.join('22102020_AN', 'hERG_ssDeact_3s_AN_12.31.17', 'hERG_ssDeact_3s_AN_12.31.17'), '22102020_AN', 'parameters_22102020_AN_hERG_ssDeact_3s_AN_12.31.17.csv', os.path.join('variant names', '22102020_AN.txt'), 18, 'ssDeact')

    '''

    ## INSERT YOUR INPUTS HERE
    # quality_control_sat_mut_py(parent dir, data dir, plate name, QC file name, variant file path, num sweeps, protocol)


if __name__ == '__main__':
    main()
