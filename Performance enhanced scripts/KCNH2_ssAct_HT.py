import os
import shutil
import numpy as np
from ssAct_fit import ssAct_fit
import csv
import time
import math
import multiprocessing
import itertools


def append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table,
                           variant_peak_table, analysis):
    variant_summary_table = variant_summary_table.reshape(-1)
    variant_summary_wells = variant_summary_wells.reshape(-1)
    if analysis == 'Onset':
        variant_peak_table = variant_peak_table.reshape(-1)

    if np.shape(summary_table)[0] == 0:
        summary_table = variant_summary_table
        no_well_summary_table = variant_summary_table


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


        summary_table = np.vstack((summary_table, [variant_summary_table]))

        summary_table = np.vstack((summary_table, [variant_summary_wells]))

        no_well_summary_table = np.vstack((no_well_summary_table, [variant_summary_table]))

    return [summary_table, no_well_summary_table]



def work(time_secs, data, sweep_pass_qc_array, sweep_cap_array, num_sweeps, wellID, rsq_thresh, summary_sweep_voltage, amp_thresh, cursor_start, cursor_end):
    [pos40mVCD, returnV05, returnDG, returnK, returnz] = ssAct_fit(time_secs, data, sweep_pass_qc_array, sweep_cap_array, num_sweeps, wellID, rsq_thresh, summary_sweep_voltage, amp_thresh, cursor_start, cursor_end)


# def high_throughput(parent_dir, success_qc_dir, control_dir, filter, smooth, rsquare, variant_name_file, start_voltage,voltage_step_interval, summary_voltage, full_analysis, total_sweeps, analysis_type, srvr_analysis, drug_control):
def high_throughput_ssAct(parent_dir, plate_name, well_widgets, control_widget, num_rows, num_cols, analysis_type):
    total_tic = time.time()

    # Create the parent results directory if it doesnt exist and the directory that encompasses the results for this analysis
    if analysis_type == 'ssAct':
        parent_result_dir = os.path.join(parent_dir, 'Data Analysis Results ssAct')
    else:
        print('Did not enter protocol tag correctly, aborting program.')
        return



    if analysis_type == 'ssAct':

        summary_filename = ''
        V05_summary_filename = ''
        DG_summary_filename = ''
        k_summary_filename = ''
        z_summary_filename = ''


    print('Commencing data analysis. Please give this some time...')
    # Go through each QC mutant


    if analysis_type == 'ssAct':
        summary_table = np.array([])
        no_well_summary_table = np.array([])
        V05_summary_table = np.array([])
        V05_no_well_summary_table = np.array([])
        DG_summary_table = np.array([])
        DG_no_well_summary_table = np.array([])
        k_summary_table = np.array([])
        k_no_well_summary_table = np.array([])
        z_summary_table = np.array([])
        z_no_well_summary_table = np.array([])

    '''
    for variants in range(0, (len(variant_dir_list))):
        if analysis_type == 'ssAct':
            variant_summary_table = np.array([])
            variant_summary_wells = np.array([])

            variant_summary_table = np.append(variant_summary_table, variant)
            well_header = variant + '_wellID'
            variant_summary_wells = np.append(variant_summary_wells, well_header)

            V05_variant_summary_table = np.array([])
            V05_variant_summary_wells = np.array([])
            DG_variant_summary_table = np.array([])
            DG_variant_summary_wells = np.array([])
            k_variant_summary_table = np.array([])
            k_variant_summary_wells = np.array([])
            z_variant_summary_table = np.array([])
            z_variant_summary_wells = np.array([])

            V05_variant_summary_table = np.append(V05_variant_summary_table, variant)
            V05_variant_summary_wells = np.append(V05_variant_summary_wells, well_header)
            DG_variant_summary_table = np.append(DG_variant_summary_table, variant)
            DG_variant_summary_wells = np.append(DG_variant_summary_wells, well_header)
            k_variant_summary_table = np.append(k_variant_summary_table, variant)
            k_variant_summary_wells = np.append(k_variant_summary_wells, well_header)
            z_variant_summary_table = np.append(z_variant_summary_table, variant)
            z_variant_summary_wells = np.append(z_variant_summary_wells, well_header)

            CD_array_table = np.array([])
            
    '''
    #count = 1

    data = []
    time_secs = []
    num_sweeps = []
    wellIDs = []
    sweep_pass_qc_array = []
    sweep_cap_array = []

    for row in range(0, num_rows):
        for col in range(0, num_cols):
            wellID = well_widgets[row, col].wellID
            variant = well_widgets[row, col].variant
            #print(count)
            #count = count + 1
            if analysis_type == 'ssAct':
                #[pos40mVCD, returnV05, returnDG, returnK, returnz] = ssAct_fit(well_widgets[row, col], control_widget)
                data.append(well_widgets[row, col].sweep_currents)
                sweep_pass_qc_array.append(well_widgets[row, col].sweep_pass_qc_array)
                time_secs.append(well_widgets[row, col].sweep_times)
                num_sweeps.append(well_widgets[row, col].num_sweeps)
                wellIDs.append(well_widgets[row, col].wellID)
                sweep_cap_array.append(well_widgets[row, col].sweep_cap_array)
                '''
                if pos40mVCD != 'N/A':
                    variant_summary_table = np.append(variant_summary_table, pos40mVCD)
                    variant_summary_wells = np.append(variant_summary_wells, wellID)
                if returnV05 != 'N/A' and variant != 'neg_ctrl':
                    V05_variant_summary_table = np.append(V05_variant_summary_table, returnV05)
                    V05_variant_summary_wells = np.append(V05_variant_summary_wells, wellID)
                if returnDG != 'N/A' and variant != 'neg_ctrl':
                    DG_variant_summary_table = np.append(DG_variant_summary_table, returnDG)
                    DG_variant_summary_wells = np.append(DG_variant_summary_wells, wellID)
                if returnK != 'N/A' and variant != 'neg_ctrl':
                    k_variant_summary_table = np.append(k_variant_summary_table, returnK)
                    k_variant_summary_wells = np.append(k_variant_summary_wells, wellID)
                if returnz != 'N/A' and variant != 'neg_ctrl':
                    z_variant_summary_table = np.append(z_variant_summary_table, returnz)
                    z_variant_summary_wells = np.append(z_variant_summary_wells, wellID)
                '''


        '''
        if analysis_type == 'ssAct':
            [summary_table, no_well_summary_table] = append_summary_results(variant_summary_table,
                                                                            variant_summary_wells, summary_table,
                                                                            no_well_summary_table, [], analysis_type)
            if variant != 'neg_ctrl':
                [V05_summary_table, V05_no_well_summary_table] = append_summary_results(V05_variant_summary_table,
                                                                                        V05_variant_summary_wells,
                                                                                        V05_summary_table,
                                                                                        V05_no_well_summary_table, [],
                                                                                        analysis_type)
                [DG_summary_table, DG_no_well_summary_table] = append_summary_results(DG_variant_summary_table,
                                                                                      DG_variant_summary_wells,
                                                                                      DG_summary_table,
                                                                                      DG_no_well_summary_table, [],
                                                                                      analysis_type)
                [k_summary_table, k_no_well_summary_table] = append_summary_results(k_variant_summary_table,
                                                                                    k_variant_summary_wells,
                                                                                    k_summary_table,
                                                                                    k_no_well_summary_table, [],
                                                                                    analysis_type)
                [z_summary_table, z_no_well_summary_table] = append_summary_results(z_variant_summary_table,
                                                                                    z_variant_summary_wells,
                                                                                    z_summary_table,
                                                                                    z_no_well_summary_table, [],
                                                                                    analysis_type)
        '''
    num_cpus = int(multiprocessing.cpu_count())
    pool = multiprocessing.Pool(num_cpus)
    pool.starmap(work, zip(time_secs, data, sweep_pass_qc_array, sweep_cap_array, num_sweeps, wellIDs, itertools.repeat(control_widget.rsq_thresh), itertools.repeat(control_widget.summary_sweep_voltage), itertools.repeat(control_widget.amp_thresh), itertools.repeat(control_widget.cursor_start), itertools.repeat(control_widget.cursor_end)))

    '''
     
    # Now write the output
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

    if analysis_type == 'ssAct':

        V05_summary_table = V05_summary_table.transpose()
        V05_no_well_summary_table = V05_no_well_summary_table.transpose()
        DG_summary_table = DG_summary_table.transpose()
        DG_no_well_summary_table = DG_no_well_summary_table.transpose()
        k_summary_table = k_summary_table.transpose()
        k_no_well_summary_table = k_no_well_summary_table.transpose()
        z_summary_table = z_summary_table.transpose()
        z_no_well_summary_table = z_no_well_summary_table.transpose()

        if not os.path.isfile(V05_summary_filename):
            with open(V05_summary_filename, mode='w') as result_output:
                result_writer = csv.writer(result_output, lineterminator='\n')
                for row in range(0, np.shape(V05_summary_table)[0]):
                    result_writer.writerow(V05_summary_table[row])

        if not os.path.isfile(V05_no_well_summary_filename):
            with open(V05_no_well_summary_filename, mode='w') as result_output:
                result_writer = csv.writer(result_output, lineterminator='\n')
                for row in range(0, np.shape(V05_no_well_summary_table)[0]):
                    result_writer.writerow(V05_no_well_summary_table[row])

        if not os.path.isfile(DG_summary_filename):
            with open(DG_summary_filename, mode='w') as result_output:
                result_writer = csv.writer(result_output, lineterminator='\n')
                for row in range(0, np.shape(DG_summary_table)[0]):
                    result_writer.writerow(DG_summary_table[row])

        if not os.path.isfile(DG_no_well_summary_filename):
            with open(DG_no_well_summary_filename, mode='w') as result_output:
                result_writer = csv.writer(result_output, lineterminator='\n')
                for row in range(0, np.shape(DG_no_well_summary_table)[0]):
                    result_writer.writerow(DG_no_well_summary_table[row])

        if not os.path.isfile(k_summary_filename):
            with open(k_summary_filename, mode='w') as result_output:
                result_writer = csv.writer(result_output, lineterminator='\n')
                for row in range(0, np.shape(k_summary_table)[0]):
                    result_writer.writerow(k_summary_table[row])

        if not os.path.isfile(k_no_well_summary_filename):
            with open(k_no_well_summary_filename, mode='w') as result_output:
                result_writer = csv.writer(result_output, lineterminator='\n')
                for row in range(0, np.shape(k_no_well_summary_table)[0]):
                    result_writer.writerow(k_no_well_summary_table[row])

        if not os.path.isfile(z_summary_filename):
            with open(z_summary_filename, mode='w') as result_output:
                result_writer = csv.writer(result_output, lineterminator='\n')
                for row in range(0, np.shape(z_summary_table)[0]):
                    result_writer.writerow(z_summary_table[row])

        if not os.path.isfile(z_no_well_summary_filename):
            with open(z_no_well_summary_filename, mode='w') as result_output:
                result_writer = csv.writer(result_output, lineterminator='\n')
                for row in range(0, np.shape(z_no_well_summary_table)[0]):
                    result_writer.writerow(z_no_well_summary_table[row])
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

