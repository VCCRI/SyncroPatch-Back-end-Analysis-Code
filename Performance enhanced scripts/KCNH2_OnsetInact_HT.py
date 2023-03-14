import os
import shutil
import numpy as np
from onset_inact_fit import onset_inact_fit
import csv
import time
import math


def append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table,
                           variant_peak_table, analysis):
    variant_summary_table = variant_summary_table.reshape(-1)
    variant_summary_wells = variant_summary_wells.reshape(-1)
    if analysis == 'Onset':
        variant_peak_table = variant_peak_table.reshape(-1)

    if np.shape(summary_table)[0] == 0:
        summary_table = variant_summary_table
        no_well_summary_table = variant_summary_table
        '''
        if analysis == 'Onset':
            summary_table = np.append([summary_table], [variant_peak_table], axis=0)
            no_well_summary_table = np.append([no_well_summary_table], [variant_peak_table], axis=0)
            summary_table = np.vstack((summary_table, [variant_summary_wells]))
        else:
        '''

        summary_table = np.append([summary_table], [variant_summary_wells], axis=0)
    else:
        sum_len = np.shape(summary_table[1])
        var_len = np.shape(variant_summary_table)
        sum_len = sum_len[0]
        var_len = var_len[0]
        if var_len > sum_len:
            # Populate the summary table with empty entries at the end so dimensions match
            size_sum = np.shape(summary_table)
            num_rows = size_sum[0]
            num_cols = var_len - sum_len

            empty_table = np.empty([num_rows, num_cols])
            empty_table = empty_table.astype(str)
            empty_table.fill('')

            '''
            if analysis == 'Onset':
                no_well_num_rows = int(num_rows / 3)*2
                if no_well_num_rows == 1:
                    # print('1 row')
                    no_well_empty_table = np.empty(num_cols)
                else:
                    # print('mult rows')
                    no_well_empty_table = np.empty([no_well_num_rows, num_cols])
            else:
                no_well_num_rows = int(num_rows / 2)
                if no_well_num_rows == 1:
                    # print('1 row')
                    no_well_empty_table = np.empty(num_cols)
                else:
                    # print('mult rows')
                    no_well_empty_table = np.empty([no_well_num_rows, num_cols])
            '''
            no_well_num_rows = int(num_rows / 2)
            if no_well_num_rows == 1:
                # print('1 row')
                no_well_empty_table = np.empty(num_cols)
            else:
                # print('mult rows')
                no_well_empty_table = np.empty([no_well_num_rows, num_cols])

            no_well_empty_table = no_well_empty_table.astype(str)
            no_well_empty_table.fill('')

            # Axis = 0 adds as a row
            # print(no_well_summary_table)
            summary_table = np.hstack((summary_table, empty_table))
            no_well_summary_table = np.hstack((no_well_summary_table, no_well_empty_table))
        elif var_len < sum_len:
            empty_table = np.empty(sum_len - var_len)
            empty_table = empty_table.astype(str)
            empty_table.fill('')
            variant_summary_table = np.append(variant_summary_table, empty_table)
            variant_summary_wells = np.append(variant_summary_wells, empty_table)
            '''
            if analysis == 'Onset':
                variant_peak_table = np.append(variant_peak_table, empty_table)
            '''

        summary_table = np.vstack((summary_table, [variant_summary_table]))
        '''
        if analysis == 'Onset':
            summary_table = np.vstack((summary_table, [variant_peak_table]))
        '''
        summary_table = np.vstack((summary_table, [variant_summary_wells]))
        # print(summary_table)
        # print(no_well_summary_table)
        # print(variant_summary_table)
        no_well_summary_table = np.vstack((no_well_summary_table, [variant_summary_table]))
        '''
        if analysis == 'Onset':
            no_well_summary_table = np.vstack((no_well_summary_table, [variant_peak_table]))
        '''
    return [summary_table, no_well_summary_table]


def prompt_user(filename_prompt, file_dir, data_dir, summary):
    dir_name = str(input(filename_prompt))

    if not dir_name:
        if file_dir == 'file':
            print('cannot have empty file name')
        else:
            print('cannot have empty directory name')
        while 1:
            dir_name = str(input(filename_prompt))
            if dir_name:
                break
            else:
                if file_dir == 'file':
                    print('cannot have empty file name')
                else:
                    print('cannot have empty directory name')

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

    print(dir_name)

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


# def high_throughput(parent_dir, success_qc_dir, control_dir, filter, smooth, rsquare, variant_name_file, start_voltage,voltage_step_interval, summary_voltage, full_analysis, total_sweeps, analysis_type, srvr_analysis, drug_control):
def high_throughput_onset_inact(parent_dir, plate_name, well_widgets, control_widget, num_rows, num_cols, analysis_type):
    total_tic = time.time()

    # Create the parent results directory if it doesnt exist and the directory that encompasses the results for this analysis

    if analysis_type == 'Onset':
        parent_result_dir = os.path.join(parent_dir, 'Data Analysis Results Onset Inact')
    else:
        print('Did not enter protocol tag correctly, aborting program.')
        return



    print('Commencing data analysis. Please give this some time...')
    # Go through each QC mutant


    summary_table = np.array([])
    no_well_summary_table = np.array([])

    '''
    for variants in range(0, (len(SatMutVariantNames))):
        var_tic = time.time()
        variant = SatMutVariantNames[variants]


        if analysis_type == 'Onset':
            variant_summary_table = np.array([])
            variant_summary_wells = np.array([])

            variant_summary_table = np.append(variant_summary_table, variant)
            well_header = variant + '_wellID'
            variant_summary_wells = np.append(variant_summary_wells, well_header)

            variant_peak_table = np.array([])
            variant_peak_table = np.append(variant_peak_table, variant + '_peak_current')



        # Go through each raw data file and perform the elected data analysis
        for data_file in range(0, len(variant_files)):
            spl_name = variant_files[data_file].split('.')
            spl_name = spl_name[0].split('_')
            num_sweeps = int(spl_name[-1])
            wellID = spl_name[-2]
    '''

    #count = 1
    for row in range(0, num_rows):
        for col in range(0, num_cols):
            wellID = well_widgets[row, col].wellID
            variant = well_widgets[row, col].variant
            #print(count)
            #count = count+1
            if analysis_type == 'Onset':
                [zeromVtau, peak_current] = onset_inact_fit(well_widgets[row, col], control_widget)
                '''
                if zeromVtau != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_table = np.append(variant_summary_table, zeromVtau)
                    variant_summary_wells = np.append(variant_summary_wells, wellID)
                    variant_peak_table = np.append(variant_peak_table, peak_current)
                '''

        '''
        if analysis_type == 'Onset':
            if variant != 'neg_ctrl':
                [summary_table, no_well_summary_table] = append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table, variant_peak_table, analysis_type)
        '''


    '''
    # Now write the output
    summary_table = summary_table.transpose()
    no_well_summary_table = no_well_summary_table.transpose()
    # print(np.shape(summary_table))

    with open(summary_filename, mode='w') as result_output:
        result_writer = csv.writer(result_output, lineterminator='\n')
        for row in range(0, np.shape(summary_table)[0]):
            result_writer.writerow(summary_table[row])

    '''


    total_tok = time.time()
    elapsed_time_secs = total_tok - total_tic
    elapsed_time_mins = elapsed_time_secs / 60
    elapsed_time_hours = elapsed_time_mins / 60
    rem_elapsed_time_mins = elapsed_time_mins % 60
    print('Total Elapsed Run-Time was ' + str(math.floor(elapsed_time_hours)) + ' hours and ' + str(
        math.floor(rem_elapsed_time_mins)) + ' minutes.')


def main():
    print('blah')

if __name__ == '__main__':
    main()

