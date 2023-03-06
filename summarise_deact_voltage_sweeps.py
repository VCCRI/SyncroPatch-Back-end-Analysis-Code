
import os
import csv
import shutil
import numpy as np


def append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table, variant_peak_table, analysis):
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

def process_file(variant_name_file, full_results_dir, summary_voltage, summary_filename, no_well_summary_filename):
    SatMutVariantNames = []
    with open(variant_name_file) as var_file:
        for line in var_file:
            SatMutVariantNames.append(line)

    summary_table = np.array([])
    no_well_summary_table = np.array([])
    for var in range(0, len(SatMutVariantNames)):
        SatMutVariantNames[var] = SatMutVariantNames[var].replace(':', '_')
        SatMutVariantNames[var] = SatMutVariantNames[var].replace('\n', '')
        if len(SatMutVariantNames[var]) == 0:
            continue

        variant = SatMutVariantNames[var]
        result_var_path = os.path.join(full_results_dir, variant)
        #print(result_var_path)

        variant_summary_table = np.array([])
        variant_summary_wells = np.array([])

        variant_summary_table = np.append(variant_summary_table, variant)
        well_header = variant + '_wellID'
        variant_summary_wells = np.append(variant_summary_wells, well_header)

        variant_peak_table = np.array([])
        variant_peak_table = np.append(variant_peak_table, variant + '_peak_current')

        result_files = os.listdir(result_var_path)
        for f in range(0, len(result_files)):
            #print(result_files[f])
            res_file = os.path.join(result_var_path, result_files[f])

            wellID = result_files[f].split('.')
            wellID = wellID[0]

            data = []
            with open(res_file, 'r') as csvfile:
                read = csv.reader(csvfile)
                for row in read:
                    data.append(row)

            data = np.array(data)

            #print(data)
            for r in range(1, np.shape(data)[0]):
                if len(data[r]) == 1:
                    continue

                # print(np.array(data[r]))
                row_data = np.array(data[r])

                #print(summary_voltage)
                row_voltage = int(float(row_data[1]))
                #print(row_voltage)
                if row_voltage == summary_voltage:
                    #print('ye')
                    warning = row_data[10]
                    #print(warning)
                    if 'Poor Fit' in warning or 'Tau less than 0' in warning or 'Tau has value greater than sweep duration' in warning or 'not following increasing trend' in warning:
                        #print('cont')
                        continue

                    variant_summary_table = np.append(variant_summary_table, row_data[12])
                    variant_summary_wells = np.append(variant_summary_wells, wellID)

        [summary_table, no_well_summary_table] = append_summary_results(variant_summary_table, variant_summary_wells,
                                                                        summary_table, no_well_summary_table,
                                                                        variant_peak_table, 'ssDeact Fit')

    summary_table = summary_table.transpose()
    no_well_summary_table = no_well_summary_table.transpose()
    # print(np.shape(summary_table))

    with open(summary_filename, mode='w') as result_output:
        result_writer = csv.writer(result_output, lineterminator='\n')
        for row in range(0, np.shape(summary_table)[0]):
            result_writer.writerow(summary_table[row])

    with open(no_well_summary_filename, mode='w') as result_output:
        result_writer = csv.writer(result_output, lineterminator='\n')
        for row in range(0, np.shape(no_well_summary_table)[0]):
            result_writer.writerow(no_well_summary_table[row])


def summarise_deact(parent_dir, plate_name, results_dir, summary_voltage, variant_name_file):

    print('FIX WARNINGS')
    output_dir = os.path.join(parent_dir, 'Data Analysis Results ssDeact', plate_name)
    full_results_dir = os.path.join(parent_dir, 'Data Analysis Results ssDeact', plate_name, results_dir)
    variant_name_file = os.path.join(parent_dir, variant_name_file)


    if summary_voltage == 'all':
        summary_filename_prompt = 'Please enter the base name you would like to call each of the .csv files which store the summaries of the tau weighted values (will be tagged with summary voltage automatically): '

        # [summary_filename, no_well_summary_filename] = prompt_user(summary_filename_prompt, 'file', output_parent_dir, 1)
        summary_basename = 'summary_tau_weighted'
        no_well_summary_basename = 'summary_tau_weighted_no_wellID'

        for volt in range(20, -160, -10):
            file_tag = '_'+str(volt)+'mV.csv'
            summary_filename = summary_basename+file_tag
            no_well_summary_filename = no_well_summary_basename+file_tag
            summary_filename = os.path.join(output_dir, summary_filename)
            no_well_summary_filename = os.path.join(output_dir, no_well_summary_filename)
            process_file(variant_name_file, full_results_dir, volt, summary_filename, no_well_summary_filename)




    else:
        summary_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the summary of the tau weighted values: '
        # [summary_filename, no_well_summary_filename] = prompt_user(summary_filename_prompt, 'file', output_parent_dir, 1)
        summary_filename = 'summary_tau_weighted_sweep_-120mV.csv'
        no_well_summary_filename = 'summary_tau_weighted_sweep_-120mV_no_wellID.csv'
        summary_filename = os.path.join(output_dir, summary_filename)
        no_well_summary_filename = os.path.join(output_dir, no_well_summary_filename)
        process_file(variant_name_file, full_results_dir, summary_voltage, summary_filename, no_well_summary_filename)

def main():
    summarise_deact(os.path.join('Z://', 'Syncropatch'), '06082020_AN', 'results', 'all', os.path.join('variant names', '06082020_AN.txt'))


if __name__ == '__main__':
        main()