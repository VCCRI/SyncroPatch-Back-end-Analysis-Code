import os
import shutil
import numpy as np
from ssDeact_fit import ssDeact_fit
'''
from ssDeact_analyse_CD_sweep1mV_sweep2mV_peak_ratio import ssDeact_analyse_CD_sweep1mV_sweep2mV_peak_ratio
from ssDeact_analyse_CD_neg_40mV_neg_110mV_peak_ratio import ssDeact_analyse_CD_neg_40mV_neg_110mV_peak_ratio
from ssDeact_analyse_CD_sweep1mV_time1_time2_peak_ratio import ssDeact_analyse_CD_sweep1mV_time1_time2_peak_ratio
from ssDeact_analyse_CD_neg_40mV_time1_time2_peak_ratio import ssDeact_analyse_CD_neg_40mV_time1_time2_peak_ratio
from ssDeact_analyse_CD_sweep1mV import ssDeact_analyse_CD_sweep1mV
from ssDeact_analyse_CD_neg_40mV import ssDeact_analyse_CD_neg_40mV
# from mod_FAIV_py import mod_FAIV
'''
import csv
import time
import math
import multiprocessing
import itertools



def append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table, variant_peak_table, analysis):
    variant_summary_table = variant_summary_table.reshape(-1)
    variant_summary_wells = variant_summary_wells.reshape(-1)

    if np.shape(summary_table)[0] == 0:
        summary_table = variant_summary_table

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

            summary_table = np.hstack((summary_table, empty_table))
        elif var_len < sum_len:
            empty_table = np.empty(sum_len - var_len)
            empty_table = empty_table.astype(str)
            empty_table.fill('')
            variant_summary_table = np.append(variant_summary_table, empty_table)
            variant_summary_wells = np.append(variant_summary_wells, empty_table)


        summary_table = np.vstack((summary_table, [variant_summary_table]))

        summary_table = np.vstack((summary_table, [variant_summary_wells]))

    return summary_table

def work2(time_secs, data, sweep_pass_qc_array, num_sweeps, wellID, rsq_thresh, summary_sweep_voltage, amp_thresh, cursor_start, cursor_end):

    neg50mVTW = ssDeact_fit(time_secs, data, sweep_pass_qc_array, num_sweeps, wellID, rsq_thresh, summary_sweep_voltage, amp_thresh, cursor_start, cursor_end)

def high_throughput_ssDeact(parent_dir, plate_name, well_widgets, control_widget, num_rows, num_cols, analysis_type):
    total_tic = time.time()

    if analysis_type == 'ssDeact Fit' or analysis_type == 'ssDeact CD sweep time ratio' or analysis_type == 'ssDeact CD sweep peak ratio' or analysis_type == 'ssDeact CD sweep peak':
        parent_result_dir = os.path.join(parent_dir, 'Data Analysis Results ssDeact')

    '''
    if not os.path.isdir(parent_result_dir):
        os.mkdir(parent_result_dir)
        output_parent_dir = os.path.join(parent_result_dir, plate_name)
        if not os.path.isdir(output_parent_dir):
            os.mkdir(output_parent_dir)
    else:
        output_parent_dir = os.path.join(parent_result_dir, plate_name)
        if not os.path.isdir(output_parent_dir):
            os.mkdir(output_parent_dir)
    '''



    if analysis_type == 'ssDeact CD sweep time ratio':
        summary_time1_filename = 'ssDeact_summary'
        summary_time2_filename = ''

    elif analysis_type == 'ssDeact CD sweep peak ratio':
        summary_filename = ''
        summary_sweep1_CD_filename = ''

        summary_sweep2_CD_filename = ''
    elif analysis_type == 'ssDeact CD sweep peak':
        summary_filename = ''
    elif analysis_type == 'ssDeact Fit':
        summary_filename = ''

    print('Commencing data analysis. Please give this some time...')
    # Go through each QC mutant

    if analysis_type == 'ssDeact CD sweep time ratio':
        summary_time1_table = np.array([])
        summary_time2_table = np.array([])
        
    elif analysis_type == 'ssDeact CD sweep peak ratio':
        summary_table = np.array([])
        summary_table_sweep1 = np.array([])
        summary_table_sweep2 = np.array([])

    elif analysis_type == 'ssDeact CD sweep peak':
        summary_table = np.array([])
    elif analysis_type == 'ssDeact Fit':
        summary_table = np.array([])

    # for variants in range(0, (len(variant_dir_list))):

    '''
    for variants in range(0, (len(SatMutVariantNames))):
        var_tic = time.time()

        if analysis_type == 'ssDeact CD sweep time ratio':
            variant_summary_time1_table = np.array([])
            variant_summary_time1_wells = np.array([])

            variant_summary_time1_table = np.append(variant_summary_time1_table, variant)
            well_header = variant + '_wellID'
            variant_summary_time1_wells = np.append(variant_summary_time1_wells, well_header)

            variant_summary_time2_table = np.array([])
            variant_summary_time2_wells = np.array([])

            variant_summary_time2_table = np.append(variant_summary_time2_table, variant)
            well_header = variant + '_wellID'
            variant_summary_time2_wells = np.append(variant_summary_time2_wells, well_header)

        elif analysis_type == 'ssDeact CD sweep peak ratio':
            variant_summary_table = np.array([])
            variant_summary_wells = np.array([])

            variant_summary_table = np.append(variant_summary_table, variant)
            well_header = variant + '_wellID'
            variant_summary_wells = np.append(variant_summary_wells, well_header)

            variant_summary_sweep1_table = np.array([])
            variant_summary_sweep1_wells = np.array([])

            variant_summary_sweep1_table = np.append(variant_summary_sweep1_table, variant)
            variant_summary_sweep1_wells = np.append(variant_summary_sweep1_wells, well_header)

            variant_summary_sweep2_table = np.array([])
            variant_summary_sweep2_wells = np.array([])

            variant_summary_sweep2_table = np.append(variant_summary_sweep2_table, variant)
            variant_summary_sweep2_wells = np.append(variant_summary_sweep2_wells, well_header)

        else:
            variant_summary_table = np.array([])
            variant_summary_wells = np.array([])

            variant_summary_table = np.append(variant_summary_table, variant)
            well_header = variant + '_wellID'
            variant_summary_wells = np.append(variant_summary_wells, well_header)

        # Go through each raw data file and perform the elected data analysis
        for data_file in range(0, len(variant_files)):
            spl_name = variant_files[data_file].split('.')
            spl_name = spl_name[0].split('_')
            num_sweeps = int(spl_name[-1])
            wellID = spl_name[-2]

    '''


    data = []
    time_secs = []
    num_sweeps = []
    wellIDs = []
    sweep_pass_qc_array = []


    '''
    for row in range(0, num_rows):
        for col in range(0, num_cols):
            wellID = well_widgets[row, col].wellID
            variant = well_widgets[row, col].variant
            
            if analysis_type == 'ssDeact Fit':
                #neg50mVTW = ssDeact_fit(well_widgets[row, col], control_widget)
                data.append(well_widgets[row, col].sweep_currents)
                sweep_pass_qc_array.append(well_widgets[row, col].sweep_pass_qc_array)
                time_secs.append(well_widgets[row, col].sweep_times)
                num_sweeps.append(well_widgets[row, col].num_sweeps)
                wellIDs.append(well_widgets[row, col].wellID)
    
    


    num_cpus = int(multiprocessing.cpu_count())
    pool2 = multiprocessing.Pool(processes=20)
    #pool2 = multiprocessing.Semaphore(20)
    pool2.starmap(work2, zip(time_secs, data, sweep_pass_qc_array, num_sweeps, wellIDs, itertools.repeat(control_widget.rsq_thresh), itertools.repeat(control_widget.summary_sweep_voltage), itertools.repeat(control_widget.amp_thresh), itertools.repeat(control_widget.cursor_start), itertools.repeat(control_widget.cursor_end)))
    
    pool2.close()
    '''

    '''
    pool = multiprocessing.Pool(20)
    results = []

    for row in range(0, num_rows):
        for col in range(0, num_cols):
            wellID = well_widgets[row, col].wellID
            variant = well_widgets[row, col].variant

            if analysis_type == 'ssDeact Fit':
                # neg50mVTW = ssDeact_fit(well_widgets[row, col], control_widget)
                data.append(well_widgets[row, col].sweep_currents)
                sweep_pass_qc_array.append(well_widgets[row, col].sweep_pass_qc_array)
                time_secs.append(well_widgets[row, col].sweep_times)
                num_sweeps.append(well_widgets[row, col].num_sweeps)
                wellIDs.append(well_widgets[row, col].wellID)
                result = pool.apply_async(work2, args=(well_widgets[row, col].sweep_times, well_widgets[row, col].sweep_currents, well_widgets[row, col].sweep_pass_qc_array, well_widgets[row, col].num_sweeps, well_widgets[row, col].wellID, control_widget.rsq_thresh, control_widget.summary_sweep_voltage, control_widget.amp_thresh, control_widget.cursor_start, control_widget.cursor_end))
                results.append(result)

    for result in results:
        result.wait()

    pool.close()
    pool.join()
    '''

    with multiprocessing.Pool(20) as pool:
        # call the function for each item in parallel
        for result in pool.starmap(work2, zip(time_secs, data, sweep_pass_qc_array, num_sweeps, wellIDs, itertools.repeat(control_widget.rsq_thresh), itertools.repeat(control_widget.summary_sweep_voltage), itertools.repeat(control_widget.amp_thresh), itertools.repeat(control_widget.cursor_start), itertools.repeat(control_widget.cursor_end)))
            result.wait()
            
    pool.close()
    pool.join()

    '''
                if neg50mVTW != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_table = np.append(variant_summary_table, neg50mVTW)
                    variant_summary_wells = np.append(variant_summary_wells, wellID)
    '''

    '''
            elif analysis_type == 'ssDeact CD sweep time ratio':
                # current_density_ratio = ssDeact_analyse_CD(os.path.join(cwd_path, parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps)
                [current_density_ratio_250, current_density_ratio_500] = ssDeact_analyse_CD_time1_time2_peak_ratio(wellID, int(num_sweeps), variant, 3, total_sweeps, var_amp_thresh)

                if current_density_ratio_250 != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_time1_table = np.append(variant_summary_time1_table, current_density_ratio_250)
                    variant_summary_time1_wells = np.append(variant_summary_time1_wells, wellID)
                if current_density_ratio_500 != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_time2_table = np.append(variant_summary_time2_table, current_density_ratio_500)
                    variant_summary_time2_wells = np.append(variant_summary_time2_wells, wellID)

            elif analysis_type == 'ssDeact CD sweep peak ratio':
                [current_density_ratio, current_density_sweep1, current_density_sweep2] = ssDeact_analyse_CD_sweep1_sweep2_peak_ratio(wellID, int(num_sweeps), variant, 3, total_sweeps, 'sweep1_amp_thresh', 'sweep2_amp_thresh')
                # current_density_ratio = ssDeact_analyse_CD_sweep1mV(os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps)

                if current_density_ratio != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_table = np.append(variant_summary_table, current_density_ratio)
                    variant_summary_wells = np.append(variant_summary_wells, wellID)

                    variant_summary_sweep1_table = np.append(variant_summary_sweep1_table, current_density_sweep1)
                    variant_summary_sweep1_wells = np.append(variant_summary_sweep1_wells, wellID)

                    variant_summary_sweep2_table = np.append(variant_summary_sweep2_table, current_density_sweep2)
                    variant_summary_sweep2_wells = np.append(variant_summary_sweep2_wells, wellID)

            elif analysis_type == 'ssDeact CD sweep peak':
                [current_density] = ssDeact_analyse_CD_sweep1mV(os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps)
                if current_density != 'N/A':
                    variant_summary_table = np.append(variant_summary_table, current_density)
                    variant_summary_wells = np.append(variant_summary_wells, wellID)
                if current_density != 'N/A':
                    variant_summary_table = np.append(variant_summary_table, current_density)
                    variant_summary_wells = np.append(variant_summary_wells, wellID)

            '''
    '''
        if analysis_type == 'ssDeact Fit':
            if variant != 'neg_ctrl':
                summary_table = append_summary_results(variant_summary_table, variant_summary_wells, summary_table, [], analysis_type)

        elif analysis_type == 'ssDeact CD sweep peak ratio':
            if variant != 'neg_ctrl':
                summary_table = append_summary_results(variant_summary_table, variant_summary_wells, summary_table, [], analysis_type)
                summary_table_sweep1 = append_summary_results(variant_summary_sweep1_table, variant_summary_sweep1_wells, summary_table_sweep1, [], analysis_type)
                summary_table_sweep2 = append_summary_results(variant_summary_sweep2_table, variant_summary_sweep2_wells, summary_table_sweep2, [], analysis_type)


        elif analysis_type == 'ssDeact CD sweep time ratio':
            if variant != 'neg_ctrl':
                summary_time1_table = append_summary_results(variant_summary_time1_table, variant_summary_time1_wells, summary_time1_table, [], analysis_type)
                summary_time2_table = append_summary_results(variant_summary_time2_table, variant_summary_time2_wells, summary_time2_table, [], analysis_type)

        elif analysis_type == 'ssDeact CD sweep peak':
            summary_table = append_summary_results(variant_summary_table, variant_summary_wells, summary_table, [], analysis_type)
        '''

    '''
        var_tok = time.time()
        variant_elapsed_time_secs = var_tok - var_tic
        variant_elapsed_time_mins = variant_elapsed_time_secs / 60
        variant_elapsed_time_hours = variant_elapsed_time_mins / 60
        rem_variant_elapsed_time_mins = variant_elapsed_time_mins % 60

        print('Elapsed Run-Time for Variant ' + variant + ' was ' + str(
            math.floor(variant_elapsed_time_hours)) + ' hours and ' + str(
            math.floor(rem_variant_elapsed_time_mins)) + ' minutes.')
        '''

    '''
    if analysis_type != 'ssDeact CD sweep time ratio' and analysis_type != 'ssDeact CD sweep peak ratio':
        # Now write the output
        summary_table = summary_table.transpose()


        with open(summary_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_table)[0]):
                result_writer.writerow(summary_table[row])


    if analysis_type == 'ssDeact CD sweep time ratio':
        # Now write the output
        summary_time1_table = summary_time1_table.transpose()

        with open(summary_time1_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_time1_table)[0]):
                result_writer.writerow(summary_time1_table[row])


        summary_time2_table = summary_time2_table.transpose()

        with open(summary_time2_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_time2_table)[0]):
                result_writer.writerow(summary_time2_table[row])


    if analysis_type == 'ssDeact CD sweep peak ratio':
        summary_table = summary_table.transpose()

        with open(summary_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_table)[0]):
                result_writer.writerow(summary_table[row])

        summary_table_sweep1 = summary_table_sweep1.transpose()

        with open(summary_sweep1_CD_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_table_sweep1)[0]):
                result_writer.writerow(summary_table_sweep1[row])

        summary_table_sweep2 = summary_table_sweep2.transpose()

        with open(summary_sweep2_CD_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_table_sweep2)[0]):
                result_writer.writerow(summary_table_sweep2[row])
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

