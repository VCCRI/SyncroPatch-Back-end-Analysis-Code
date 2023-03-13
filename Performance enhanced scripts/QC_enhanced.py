import os
import numpy as np
import csv
import shutil
import glob
import time
import statistics as sts
import matplotlib.pyplot as plt
# import winsound
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


def qc_well(well_names, well, parent_dir, data_dir, analysis, numpy_pandas, total_sweeps, QC_data, seal_parameter,
            capacitance_parameter_lower, capacitance_parameter_upper, access_parameter, access_switch,
            peak_current_parameter, SatMutVariantNames, output_dir, failed_leak, failed_seal, failed_cap, num_failed,
            failed_access, failed_peak, total_fail_sweeps):
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

    # name_part = current_file[0].split('\\')
    name_part = current_file[0].split('/')
    name_part = name_part[-1].split('.csv')
    name_part = name_part[0].replace('.', '_')
    name_part = name_part + str(passed_sweeps) + '.csv'

    if wellCol % 2 == 0:
        var_indx = wellCol / 2
    else:
        var_indx = (wellCol + 1) / 2
    var_dir = SatMutVariantNames[int(var_indx - 1)]
    result_file_path = os.path.join(output_dir, var_dir, name_part)
    print(output_dir)
    print(var_dir)
    print(name_part)

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


    variant_name_file = os.path.join(parent_dir, variant_name_file)


    # Extract the mutant names
    SatMutVariantNames = []
    with open(variant_name_file) as var_file:
        for line in var_file:
            SatMutVariantNames.append(line)


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

if __name__ == '__main__':
    main()
