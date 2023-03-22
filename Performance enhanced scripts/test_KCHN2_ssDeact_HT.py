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
import glob
from extract_raw_data import Json_Data, Well


def append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table,
                           variant_peak_table, analysis):
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


def work2(wellID, json_data, input_folder, rsq_thresh, summary_sweep_voltage, amp_thresh, cursor_start, cursor_end):
    cap_lower_QC_input = 5 * 1e-12
    cap_upper_QC_input = 15 * 1e-12
    seal_QC_input = 300 * 1e6
    SR_QC_input = 20 * 1e6

    json_well_data = Well(json_data, input_folder, wellID, 2)

    num_sweeps = json_data.total_sweeps

    sweep_cap_array = json_well_data.get_capacitances()
    sweep_seal_array = json_well_data.get_seal_resistances()
    sweep_series_array = json_well_data.get_series_resistances()

    sweep_pass_qc_array = np.array([])
    num_sample_points = json_data.sample_count
    time_secs = json_well_data.get_sweep_times()

    plot_indexes = [i for i in range(0, len(time_secs)) if time_secs[i] >= cursor_start and time_secs[i] <= cursor_end]


    data = np.zeros([num_sweeps, len(plot_indexes)])
    for sw in range(0, num_sweeps):
        pass_qc = 1
        if float(cap_lower_QC_input) > sweep_cap_array[sw] or float(cap_upper_QC_input) < sweep_cap_array[sw]:
            pass_qc = 0

        if float(seal_QC_input) > sweep_seal_array[sw]:
            pass_qc = 0

        if float(SR_QC_input) > sweep_series_array[sw]:
            pass_qc = 0

        sweep_pass_qc_array = np.append(sweep_pass_qc_array, pass_qc)

        sw_curr = json_well_data.get_sweep_currents(sw)
        data[sw, :] = sw_curr[plot_indexes[0]:plot_indexes[len(plot_indexes)-1]]



    neg50mVTW = ssDeact_fit(time_secs, data, sweep_pass_qc_array, num_sweeps, wellID, rsq_thresh, summary_sweep_voltage,
                            amp_thresh, cursor_start, cursor_end)


def high_throughput_ssDeact(parent_dir, plate_name, control_widget, num_rows, num_cols, analysis_type):
    total_tic = time.time()

    if analysis_type == 'ssDeact Fit' or analysis_type == 'ssDeact CD sweep time ratio' or analysis_type == 'ssDeact CD sweep peak ratio' or analysis_type == 'ssDeact CD sweep peak':
        parent_result_dir = os.path.join(parent_dir, 'Data Analysis Results ssDeact')

    input_folder = os.path.join('/datadrive', 'syncropatch', 'Clinical_variant_Brett', '01092022_AN', 'hERG_ssDeact_3s_AN_11.45.32')
    # for variants in range(0, (len(variant_dir_list))):

    json_filename = glob.glob(os.path.join(input_folder, '*.json'))
    print(json_filename)
    json_data = Json_Data(json_filename[0], 16, 24, 65)


    data = []
    time_secs = []
    num_sweeps = []
    wellIDs = []
    sweep_pass_qc_array = []

    for row in range(0, num_rows):
        for col in range(0, num_cols):
            if col+1 < 10:
                wellID = chr(row+1 + 64) + str(0) + str(col+1)
            else:
                wellID = chr(row+1 + 64) + str(col+1)
            if analysis_type == 'ssDeact Fit':
                # neg50mVTW = ssDeact_fit(well_widgets[row, col], control_widget)
                wellIDs.append(wellID)

    num_cpus = int(multiprocessing.cpu_count())
    pool2 = multiprocessing.Pool(processes=20)
    # pool2 = multiprocessing.Semaphore(20)
    pool2.starmap(work2, zip(wellIDs, itertools.repeat(json_data), itertools.repeat(input_folder), itertools.repeat(control_widget.rsq_thresh), itertools.repeat(control_widget.summary_sweep_voltage), itertools.repeat(control_widget.amp_thresh), itertools.repeat(control_widget.cursor_start), itertools.repeat(control_widget.cursor_end)))

    pool2.close()

    total_tok = time.time()
    elapsed_time_secs = total_tok - total_tic
    elapsed_time_mins = elapsed_time_secs / 60
    elapsed_time_hours = elapsed_time_mins / 60
    rem_elapsed_time_mins = elapsed_time_mins % 60
    print('Total Elapsed Run-Time was ' + str(math.floor(elapsed_time_hours)) + ' hours and ' + str(
        math.floor(rem_elapsed_time_mins)) + ' minutes.')

class ControlWidget():
    def __init__(self, protocol):
        super(ControlWidget, self).__init__()

        if protocol == 'ssDeact':
            self.rsq_thresh = 0.85
            self.summary_sweep_voltage = -50
            self.amp_thresh = 100

            #ssDeact
            self.cursor_start = 1.2
            self.cursor_end = 4.2
        elif protocol == 'ssAct':
            self.rsq_thresh = 0.85
            self.summary_sweep_voltage = 40
            self.amp_thresh = 100


            self.cursor_start = 1.205
            self.cursor_end = 1.3
        elif protocol == 'Onset':
            self.rsq_thresh = 0.85
            self.summary_sweep_voltage = 0
            self.amp_thresh = 100

            self.cursor_start = 1.175
            self.cursor_end = 1.2
            self.neg_volt_cursor_start = 1.175
            self.neg_volt_cursor_end = 1.22
def main():
    print('blah')


    c = ControlWidget('ssDeact')
    high_throughput_ssDeact(os.path.join('/datadrive','syncropatch','Clinical_variant_Brett',), '01092022_AN', c, 'ssDeact Fit')


if __name__ == '__main__':
    main()

