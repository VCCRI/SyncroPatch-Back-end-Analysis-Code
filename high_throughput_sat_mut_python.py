import os
import shutil
import numpy as np
from ssDeact_fit_py import ssDeact_fit_py
from ssAct_fit_py import ssAct_fit_py
from onset_fit_py import onset_fit_py
#from AP_pre_stim_py import AP_pre_stim
from ssDeact_analyse_CD_neg_50mV_neg_120mV_peak_ratio import ssDeact_analyse_CD_neg_50mV_neg_120mV_peak_ratio
from ssDeact_analyse_CD_neg_40mV_neg_110mV_peak_ratio import ssDeact_analyse_CD_neg_40mV_neg_110mV_peak_ratio
from ssDeact_analyse_CD_neg_50mV_250ms_500ms_peak_ratio import ssDeact_analyse_CD_neg_50mV_250ms_500ms_peak_ratio
from ssDeact_analyse_CD_neg_40mV_250ms_500ms_peak_ratio import ssDeact_analyse_CD_neg_40mV_250ms_500ms_peak_ratio
from ssDeact_analyse_CD_neg_50mV import ssDeact_analyse_CD_neg_50mV
from ssDeact_analyse_CD_neg_40mV import ssDeact_analyse_CD_neg_40mV
#from mod_FAIV_py import mod_FAIV
import csv
import time
import math
import winsound

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


#def high_throughput(parent_dir, success_qc_dir, control_dir, filter, smooth, rsquare, variant_name_file, start_voltage,voltage_step_interval, summary_voltage, full_analysis, total_sweeps, analysis_type, srvr_analysis, drug_control):
def high_throughput(parent_dir, plate_name, success_qc_dir, rsquare, variant_name_file, summary_voltage, total_sweeps, analysis_type):

    total_tic = time.time()

    # Create the parent results directory if it doesnt exist and the directory that encompasses the results for this analysis
    if analysis_type == 'ssDeact Fit' or analysis_type == 'ssDeact CD -50 250/500' or analysis_type == 'ssDeact CD -40 250/500' or analysis_type == 'ssDeact CD -50/-120' or analysis_type == 'ssDeact CD -40/-110' or analysis_type == 'ssDeact CD -50' or analysis_type == 'ssDeact CD -40':
        parent_result_dir = os.path.join(parent_dir, 'Data Analysis Results ssDeact')
    elif analysis_type == 'ssAct':
        parent_result_dir = os.path.join(parent_dir, 'Data Analysis Results ssAct')
    elif analysis_type == 'Onset':
        parent_result_dir = os.path.join(parent_dir, 'Data Analysis Results Onset Inact')
    elif analysis_type == 'AP pre-stim':
        parent_result_dir = os.path.join(parent_dir, 'Data Analysis Results AP pre-stim')
    elif analysis_type == 'mod FAIV':
        parent_result_dir = os.path.join(parent_dir, 'Data Analysis Results mod FAIV')
    else:
        print('Did not enter protocol tag correctly, aborting program.')
        return

    if not os.path.isdir(parent_result_dir):
        os.mkdir(parent_result_dir)
        output_parent_dir = os.path.join(parent_result_dir, plate_name)
        if not os.path.isdir(output_parent_dir):
            os.mkdir(output_parent_dir)
    else:
        output_parent_dir = os.path.join(parent_result_dir, plate_name)
        if not os.path.isdir(output_parent_dir):
            os.mkdir(output_parent_dir)


    if analysis_type == 'ssDeact Fit':

        summary_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the summary of the tau weighted values: '
        sweep_length = int(input('Please enter the duration of the voltage pulses (seconds): '))
        var_amp_thresh = int(input('Please enter the max peak current thresholds for the summary sweep (pA): '))
        '''
        sweep_length = 3
        var_amp_thresh = 200
        '''
        #sweep_length = 3
    elif analysis_type == 'ssDeact CD -50/-120':
        summary_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the the current density ratios of sweep 8 and 15 for each well: '
        summary_neg_50_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the the current densities of sweep 8 for each well: '
        summary_neg_120_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the the current densities of sweep 15 for each well: '
        sweep_length = int(input('Please enter the duration of the voltage pulses (seconds): '))
        #neg_120_amp_thresh = int(input('Please enter the min peak current thresholds for sweep -120mV (pA): '))
        #neg_50_amp_thresh = int(input('Please enter the max peak current thresholds for sweep -50mV (pA): '))
        #neg_120_amp_thresh = neg_120_amp_thresh*1e-12
        #neg_50_amp_thresh = neg_50_amp_thresh*1e-12
    elif analysis_type == 'ssDeact CD -40/-110':
        summary_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the the current density ratios of sweep 7 and 14 for each well: '
        summary_neg_40_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the the current densities of sweep 7 for each well: '
        summary_neg_110_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the the current densities of sweep 14 for each well: '
        sweep_length = int(input('Please enter the duration of the voltage pulses (seconds): '))
        #neg_110_amp_thresh = int(input('Please enter the min peak current thresholds for sweep -120mV (pA): '))
        #neg_40_amp_thresh = int(input('Please enter the max peak current thresholds for sweep -50mV (pA): '))
        #neg_110_amp_thresh = neg_120_amp_thresh*1e-12
        #neg_40_amp_thresh = neg_50_amp_thresh*1e-12
    elif analysis_type == 'ssDeact CD -50 250/500':
        summary_250ms_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the the current density ratios of -50mV 250ms/peak for each well: '
        summary_500ms_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the the current density ratios of -50mV 500ms/peak for each well: '

        sweep_length = int(input('Please enter the duration of the voltage pulses (seconds): '))
        var_amp_thresh = int(input('Please enter the max peak current thresholds for sweep -50mV (pA): '))
        #sweep_length = 3
    elif analysis_type == 'ssDeact CD -40 250/500':
        summary_250ms_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the the current density ratios of -40mV 250ms/peak for each well: '
        summary_500ms_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the the current density ratios of -40mV 500ms/peak for each well: '

        sweep_length = int(input('Please enter the duration of the voltage pulses (seconds): '))
        var_amp_thresh = int(input('Please enter the max peak current thresholds for sweep -40mV (pA): '))
    elif analysis_type == 'ssDeact CD -50':
        summary_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the the current density of sweep 8: '
        sweep_length = int(input('Please enter the duration of the voltage pulses (seconds): '))
    elif analysis_type == 'ssDeact CD -40':
        summary_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the the current density of sweep 7: '
        sweep_length = int(input('Please enter the duration of the voltage pulses (seconds): '))
    elif analysis_type == 'ssAct':
        summary_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the current densities from the summary sweep: '
    elif analysis_type == 'Onset':
        summary_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the summary of the tau values: '


    #parent_path = os.path.join(cwd_path, parent_path)
    variant_name_file = os.path.join(parent_dir, variant_name_file)

    # Initiate the result directories

    #if analysis_type != 'AP pre-stim':

    if analysis_type == 'ssDeact CD -50 250/500':
        [summary_250ms_filename, no_well_summary_250ms_filename] = prompt_user(summary_250ms_filename_prompt, 'file', output_parent_dir, 1)
        [summary_500ms_filename, no_well_summary_500ms_filename] = prompt_user(summary_500ms_filename_prompt, 'file', output_parent_dir, 1)

        #summary_250ms_filename = os.path.join(output_parent_dir, 'summary_test_pandas_neg_50mV_250.csv')
        #no_well_summary_250ms_filename = os.path.join(output_parent_dir, 'summary_test_pandas_neg_50mV_250_no_wellID.csv')
        #summary_500ms_filename = os.path.join(output_parent_dir, 'summary_test_pandas_neg_50mV_500.csv')
        #no_well_summary_500ms_filename = os.path.join(output_parent_dir, 'summary_test_pandas_neg_50mV_500_no_wellID.csv')
    elif analysis_type == 'ssDeact CD -40 250/500':
        [summary_250ms_filename, no_well_summary_250ms_filename] = prompt_user(summary_250ms_filename_prompt, 'file', output_parent_dir, 1)
        [summary_500ms_filename, no_well_summary_500ms_filename] = prompt_user(summary_500ms_filename_prompt, 'file', output_parent_dir, 1)

        #summary_250ms_filename = os.path.join(output_parent_dir, 'summary_test_pandas_neg_50mV_250.csv')
        #no_well_summary_250ms_filename = os.path.join(output_parent_dir, 'summary_test_pandas_neg_50mV_250_no_wellID.csv')
        #summary_500ms_filename = os.path.join(output_parent_dir, 'summary_test_pandas_neg_50mV_500.csv')
        #no_well_summary_500ms_filename = os.path.join(output_parent_dir, 'summary_test_pandas_neg_50mV_500_no_wellID.csv')
    elif analysis_type == 'ssDeact CD -50/-120':
        [summary_filename, no_well_summary_filename] = prompt_user(summary_filename_prompt, 'file', output_parent_dir, 1)
        #summary_filename = 'summary_CD_neg_50_neg_120_ratio_test_pandas.csv'
        #no_well_summary_filename = 'summary_CD_neg_50_neg_120_ratio_test_pandas_no_wellID.csv'
        [summary_neg_50_CD_filename, no_well_summary_neg_50_CD_filename] = prompt_user(summary_neg_50_filename_prompt, 'file', output_parent_dir, 1)
        #summary_neg_50_CD_filename = 'summary_CD_neg_50_test_pandas.csv'
        #no_well_summary_neg_50_CD_filename = 'summary_CD_neg_50_test_pandas_no_wellID.csv'

        [summary_neg_120_CD_filename, no_well_summary_neg_120_CD_filename] = prompt_user(summary_neg_120_filename_prompt, 'file', output_parent_dir, 1)
        #summary_neg_120_CD_filename = 'summary_CD_neg_120_test_pandas.csv'
        #no_well_summary_neg_120_CD_filename = 'summary_CD_neg_120_test_pandas_no_wellID.csv'

    elif analysis_type == 'ssDeact CD -40/-110':
        [summary_filename, no_well_summary_filename] = prompt_user(summary_filename_prompt, 'file', output_parent_dir, 1)
        #summary_filename = 'summary_CD_neg_50_neg_120_ratio_test_pandas.csv'
        #no_well_summary_filename = 'summary_CD_neg_50_neg_120_ratio_test_pandas_no_wellID.csv'
        [summary_neg_40_CD_filename, no_well_summary_neg_40_CD_filename] = prompt_user(summary_neg_40_filename_prompt, 'file', output_parent_dir, 1)
        #summary_neg_50_CD_filename = 'summary_CD_neg_50_test_pandas.csv'
        #no_well_summary_neg_50_CD_filename = 'summary_CD_neg_50_test_pandas_no_wellID.csv'

        [summary_neg_110_CD_filename, no_well_summary_neg_110_CD_filename] = prompt_user(summary_neg_110_filename_prompt, 'file', output_parent_dir, 1)
        #summary_neg_120_CD_filename = 'summary_CD_neg_120_test_pandas.csv'
        #no_well_summary_neg_120_CD_filename = 'summary_CD_neg_120_test_pandas_no_wellID.csv'


    elif analysis_type == 'ssAct':


        [summary_filename, no_well_summary_filename] = prompt_user(summary_filename_prompt, 'file', output_parent_dir, 1)
        V05_summary_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the summary of the V05 fit parameters: '
        DG_summary_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the summary of the Delta_G0 fit parameters: '
        k_summary_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the summary of the k slope fit parameters: '
        z_summary_filename_prompt = 'Please enter the name you would like to call the .csv file which stores the summary of the z fit parameters: '
        CD_array_filename_prompt = 'Please enter the name you would like to call the file that stores the current densities per sweep voltage for each well: '
        
        [V05_summary_filename, V05_no_well_summary_filename] = prompt_user(V05_summary_filename_prompt, 'file', output_parent_dir, 1)
        [DG_summary_filename, DG_no_well_summary_filename] = prompt_user(DG_summary_filename_prompt, 'file', output_parent_dir, 1)
        [k_summary_filename, k_no_well_summary_filename] = prompt_user(k_summary_filename_prompt, 'file', output_parent_dir, 1)
        [z_summary_filename, z_no_well_summary_filename] = prompt_user(z_summary_filename_prompt, 'file', output_parent_dir, 1)
        [CD_array_filename, CD_array_no_well_filename] = prompt_user(CD_array_filename_prompt, 'file', output_parent_dir, 1)
        
        '''

        V05_summary_filename = os.path.join(output_parent_dir, 'summary_V05_test_pandas.csv')
        V05_no_well_summary_filename = os.path.join(output_parent_dir, 'summary_V05_test_pandas_no_wellID.csv')
        DG_summary_filename = os.path.join(output_parent_dir, 'summary_DG_test_pandas.csv')
        DG_no_well_summary_filename = os.path.join(output_parent_dir, 'summary_DG_test_pandas_no_wellID.csv')
        z_summary_filename = os.path.join(output_parent_dir, 'summary_z_test_pandas.csv')
        z_no_well_summary_filename = os.path.join(output_parent_dir, 'summary_z_test_pandas_no_wellID.csv')
        k_summary_filename = os.path.join(output_parent_dir, 'summary_k_test_pandas.csv')
        k_no_well_summary_filename = os.path.join(output_parent_dir, 'summary_k_test_pandas_no_wellID.csv')
        summary_filename = os.path.join(output_parent_dir, 'summary_CD_test_pandas.csv')
        no_well_summary_filename = os.path.join(output_parent_dir, 'summary_CD_test_pandas_no_wellID.csv')
        CD_array_filename = os.path.join(output_parent_dir, 'current_densities_prism_format.csv')
        '''

    else:
        [summary_filename, no_well_summary_filename] = prompt_user(summary_filename_prompt, 'file', output_parent_dir, 1)
        #summary_filename = os.path.join(output_parent_dir,'summary_test_pandas.csv')
        #no_well_summary_filename = os.path.join(output_parent_dir,'summary_test_pandas.csv')

    output_plots_prompt = 'Please enter the name of the directory that will store the plots of the fits for each sweep for each well: '
    output_plots = prompt_user(output_plots_prompt, 'dir', output_parent_dir, 0)
    #output_plots = 'plots test pandas CD output'



    if analysis_type != 'ssDeact CD -50 250/500' and analysis_type != 'ssDeact CD -40 250/500' and analysis_type != 'ssDeact CD -50/-120'  and analysis_type != 'ssDeact CD -40/-110' and analysis_type != 'ssDeact CD -50' and analysis_type != 'ssDeact CD -40':
        if analysis_type == 'AP pre-stim' or analysis_type == 'mod FAIV':
            output_dir_prompt = 'Please enter the name of the directory that will store the subtracted trace data: '
        else:
            output_dir_prompt = 'Please enter the name of the directory that will store the files that contain the result parameters: '
        output_dir = prompt_user(output_dir_prompt, 'dir', output_parent_dir, 0)
        #output_dir = 'results test pandas CD output'


    '''
    if analysis_type != 'ssDeact CD -50 250/500' and analysis_type != 'ssDeact CD -50/-120' and analysis_type != 'ssDeact CD -50':
        if analysis_type != 'AP pre-stim' and analysis_type != 'mod FAIV':
            summary_filename = os.path.join(output_parent_dir, summary_filename)
            no_well_summary_filename = os.path.join(output_parent_dir, no_well_summary_filename)
            output_plots = os.path.join(output_parent_dir, output_plots)
            output_dir = os.path.join(output_parent_dir, output_dir)
        else:
            output_plots = os.path.join(output_parent_dir, output_plots)
            output_dir = os.path.join(output_parent_dir, output_dir)
    else:
        if analysis_type == 'ssDeact CD -50/-120':
            output_plots = os.path.join(output_parent_dir, output_plots)
            summary_filename = os.path.join(output_parent_dir, summary_filename)
            no_well_summary_filename = os.path.join(output_parent_dir, no_well_summary_filename)
            summary_neg_50_CD_filename = os.path.join(output_parent_dir, summary_neg_50_CD_filename)
            no_well_summary_neg_50_CD_filename = os.path.join(output_parent_dir, no_well_summary_neg_50_CD_filename)

            summary_neg_120_CD_filename = os.path.join(output_parent_dir, summary_neg_120_CD_filename)
            no_well_summary_summary_neg_120_CD_filename = os.path.join(output_parent_dir, no_well_summary_neg_120_CD_filename)
        elif analysis_type == 'ssDeact CD -50 250/500':
            output_plots = os.path.join(output_parent_dir, output_plots)

        elif analysis_type == 'ssDeact CD -50':
            summary_filename = os.path.join(output_parent_dir, summary_filename)
            no_well_summary_filename = os.path.join(output_parent_dir, no_well_summary_filename)
            output_plots = os.path.join(output_parent_dir, output_plots)
    '''


    #print(no_well_summary_filename)
    #print(output_parent_dir)
    #print(variant_name_file)


    if analysis_type != 'ssDeact CD -50 250/500' and analysis_type != 'ssDeact CD -40 250/500' and analysis_type != 'ssDeact CD -50/-120' and analysis_type != 'ssDeact CD -40/-110' and analysis_type != 'ssDeact CD -50' and analysis_type != 'ssDeact CD -40':
        if os.path.isdir(output_plots):
            shutil.rmtree(output_plots)
        if os.path.isdir(output_dir):
            shutil.rmtree(output_dir)
        os.mkdir(output_dir)
        os.mkdir(output_plots)
    else:
        if os.path.isdir(output_plots):
            shutil.rmtree(output_plots)
        os.mkdir(output_plots)

    # Extract the mutant names
    SatMutVariantNames = []
    with open(variant_name_file) as var_file:
        for line in var_file:
            SatMutVariantNames.append(line)


    for var in range(0, len(SatMutVariantNames)):
        SatMutVariantNames[var] = SatMutVariantNames[var].replace(':', '_')
        SatMutVariantNames[var] = SatMutVariantNames[var].replace('\n', '')
        if len(SatMutVariantNames[var]) == 0:
            continue
        if SatMutVariantNames[var] == '.DS_Store':
            'ds_store'
            continue
        plot_path = os.path.join(output_plots, SatMutVariantNames[var])

        if analysis_type != 'ssDeact CD -50 250/500' and analysis_type != 'ssDeact CD -40 250/500' and analysis_type != 'ssDeact CD -50/-120' and analysis_type != 'ssDeact CD -40/-110' and analysis_type != 'ssDeact CD -50' and analysis_type != 'ssDeact CD -40':
            result_path = os.path.join(output_dir, SatMutVariantNames[var])
            os.mkdir(plot_path)
            os.mkdir(result_path)
        else:
            os.mkdir(plot_path)

    # Previous implementation determined the physiological voltage but now this should be in the file
    qc_var_path = os.path.join(output_parent_dir, success_qc_dir)
    variant_dir_list = os.listdir(qc_var_path)

    print('Commencing data analysis. Please give this some time...')
    # Go through each QC mutant

    if analysis_type == 'ssDeact CD -50 250/500':
        summary_250ms_table = np.array([])
        no_well_summary_250ms_table = np.array([])
        summary_500ms_table = np.array([])
        no_well_summary_500ms_table = np.array([])
    elif analysis_type == 'ssDeact CD -40 250/500':
        summary_250ms_table = np.array([])
        no_well_summary_250ms_table = np.array([])
        summary_500ms_table = np.array([])
        no_well_summary_500ms_table = np.array([])
    elif analysis_type == 'ssDeact CD -50/-120':
        summary_table = np.array([])
        no_well_summary_table = np.array([])
        summary_table_neg_50 = np.array([])
        no_well_summary_table_neg_50 = np.array([])
        summary_table_neg_120 = np.array([])
        no_well_summary_table_neg_120 = np.array([])
    elif analysis_type == 'ssDeact CD -40/-110':
        summary_table = np.array([])
        no_well_summary_table = np.array([])
        summary_table_neg_40 = np.array([])
        no_well_summary_table_neg_40 = np.array([])
        summary_table_neg_110 = np.array([])
        no_well_summary_table_neg_110 = np.array([])

    elif analysis_type == 'ssAct':
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

    else:
        summary_table = np.array([])
        no_well_summary_table = np.array([])


    #for variants in range(0, (len(variant_dir_list))):
    for variants in range(0, (len(SatMutVariantNames))):
        var_tic = time.time()
        variant = SatMutVariantNames[variants]

        variant_file_path = os.path.join(qc_var_path, variant)
        #print(variant_file_path)
        variant_files = os.listdir(variant_file_path)



        if analysis_type == 'Onset':
            variant_summary_table = np.array([])
            variant_summary_wells = np.array([])

            variant_summary_table = np.append(variant_summary_table, variant)
            well_header = variant + '_wellID'
            variant_summary_wells = np.append(variant_summary_wells, well_header)

            variant_peak_table = np.array([])
            variant_peak_table = np.append(variant_peak_table, variant+'_peak_current')

        elif analysis_type == 'ssAct':
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
        elif analysis_type == 'ssDeact CD -50 250/500':
            variant_summary_250ms_table = np.array([])
            variant_summary_250ms_wells = np.array([])

            variant_summary_250ms_table = np.append(variant_summary_250ms_table, variant)
            well_header = variant + '_wellID'
            variant_summary_250ms_wells = np.append(variant_summary_250ms_wells, well_header)

            variant_summary_500ms_table = np.array([])
            variant_summary_500ms_wells = np.array([])

            variant_summary_500ms_table = np.append(variant_summary_500ms_table, variant)
            well_header = variant + '_wellID'
            variant_summary_500ms_wells = np.append(variant_summary_500ms_wells, well_header)
        elif analysis_type == 'ssDeact CD -40 250/500':
            variant_summary_250ms_table = np.array([])
            variant_summary_250ms_wells = np.array([])

            variant_summary_250ms_table = np.append(variant_summary_250ms_table, variant)
            well_header = variant + '_wellID'
            variant_summary_250ms_wells = np.append(variant_summary_250ms_wells, well_header)

            variant_summary_500ms_table = np.array([])
            variant_summary_500ms_wells = np.array([])

            variant_summary_500ms_table = np.append(variant_summary_500ms_table, variant)
            well_header = variant + '_wellID'
            variant_summary_500ms_wells = np.append(variant_summary_500ms_wells, well_header)
        elif analysis_type == 'ssDeact CD -50/-120':
            variant_summary_table = np.array([])
            variant_summary_wells = np.array([])

            variant_summary_table = np.append(variant_summary_table, variant)
            well_header = variant + '_wellID'
            variant_summary_wells = np.append(variant_summary_wells, well_header)

            variant_summary_neg_50_table = np.array([])
            variant_summary_neg_50_wells = np.array([])

            variant_summary_neg_50_table = np.append(variant_summary_neg_50_table, variant)
            variant_summary_neg_50_wells = np.append(variant_summary_neg_50_wells, well_header)

            variant_summary_neg_120_table = np.array([])
            variant_summary_neg_120_wells = np.array([])

            variant_summary_neg_120_table = np.append(variant_summary_neg_120_table, variant)
            variant_summary_neg_120_wells = np.append(variant_summary_neg_120_wells, well_header)
        elif analysis_type == 'ssDeact CD -40/-110':
            variant_summary_table = np.array([])
            variant_summary_wells = np.array([])

            variant_summary_table = np.append(variant_summary_table, variant)
            well_header = variant + '_wellID'
            variant_summary_wells = np.append(variant_summary_wells, well_header)

            variant_summary_neg_40_table = np.array([])
            variant_summary_neg_40_wells = np.array([])

            variant_summary_neg_40_table = np.append(variant_summary_neg_40_table, variant)
            variant_summary_neg_40_wells = np.append(variant_summary_neg_40_wells, well_header)

            variant_summary_neg_110_table = np.array([])
            variant_summary_neg_110_wells = np.array([])

            variant_summary_neg_110_table = np.append(variant_summary_neg_110_table, variant)
            variant_summary_neg_110_wells = np.append(variant_summary_neg_110_wells, well_header)

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
            if analysis_type == 'ssDeact':
                sweep_length = spl_name[4]
                sweep_length = sweep_length.split('s')
                sweep_length = int(sweep_length[0])
            '''

            if analysis_type == 'ssDeact Fit':
                '''
                if -80 <= summary_voltage <= 20:
                    var_amp_thresh = 100
                elif summary_voltage >=-150 and summary_voltage <= -90:
                    var_amp_thresh = -100
                '''

                neg50mVTW = ssDeact_fit_py(
                    os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]),
                    os.path.join(output_dir, variant, wellID + '.csv'), wellID,
                    os.path.join(output_plots, variant), int(num_sweeps), variant, sweep_length, rsquare,
                    summary_voltage, total_sweeps, var_amp_thresh)
                if neg50mVTW != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_table = np.append(variant_summary_table, neg50mVTW)
                    variant_summary_wells = np.append(variant_summary_wells, wellID)


            elif analysis_type == 'ssDeact CD -50 250/500':
                #current_density_ratio = ssDeact_analyse_CD(os.path.join(cwd_path, parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps)
                [current_density_ratio_250, current_density_ratio_500] = ssDeact_analyse_CD_neg_50mV_250ms_500ms_peak_ratio(os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps, var_amp_thresh)

                if current_density_ratio_250 != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_250ms_table = np.append(variant_summary_250ms_table, current_density_ratio_250)
                    variant_summary_250ms_wells = np.append(variant_summary_250ms_wells, wellID)
                if current_density_ratio_500 != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_500ms_table = np.append(variant_summary_500ms_table, current_density_ratio_500)
                    variant_summary_500ms_wells = np.append(variant_summary_500ms_wells, wellID)
            elif analysis_type == 'ssDeact CD -40 250/500':
                #current_density_ratio = ssDeact_analyse_CD(os.path.join(cwd_path, parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps)
                [current_density_ratio_250, current_density_ratio_500] = ssDeact_analyse_CD_neg_40mV_250ms_500ms_peak_ratio(os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps, var_amp_thresh)

                if current_density_ratio_250 != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_250ms_table = np.append(variant_summary_250ms_table, current_density_ratio_250)
                    variant_summary_250ms_wells = np.append(variant_summary_250ms_wells, wellID)
                if current_density_ratio_500 != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_500ms_table = np.append(variant_summary_500ms_table, current_density_ratio_500)
                    variant_summary_500ms_wells = np.append(variant_summary_500ms_wells, wellID)
            elif analysis_type == 'ssDeact CD -50/-120':
                [current_density_ratio, current_density_neg_50,  current_density_neg_120] = ssDeact_analyse_CD_neg_50mV_neg_120mV_peak_ratio(os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps, 'neg_50_amp_thresh', 'neg_120_amp_thresh')
                #current_density_ratio = ssDeact_analyse_CD_neg_50mV(os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps)

                if current_density_ratio != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_table = np.append(variant_summary_table, current_density_ratio)
                    variant_summary_wells = np.append(variant_summary_wells, wellID)

                    variant_summary_neg_50_table = np.append(variant_summary_neg_50_table, current_density_neg_50)
                    variant_summary_neg_50_wells = np.append(variant_summary_neg_50_wells, wellID)

                    variant_summary_neg_120_table = np.append(variant_summary_neg_120_table, current_density_neg_120)
                    variant_summary_neg_120_wells = np.append(variant_summary_neg_120_wells, wellID)
            elif analysis_type == 'ssDeact CD -40/-110':
                [current_density_ratio, current_density_neg_40,  current_density_neg_110] = ssDeact_analyse_CD_neg_40mV_neg_110mV_peak_ratio(os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps, 'neg_40_amp_thresh', 'neg_110_amp_thresh')
                #current_density_ratio = ssDeact_analyse_CD_neg_50mV(os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps)

                if current_density_ratio != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_table = np.append(variant_summary_table, current_density_ratio)
                    variant_summary_wells = np.append(variant_summary_wells, wellID)

                    variant_summary_neg_40_table = np.append(variant_summary_neg_40_table, current_density_neg_40)
                    variant_summary_neg_40_wells = np.append(variant_summary_neg_40_wells, wellID)

                    variant_summary_neg_110_table = np.append(variant_summary_neg_110_table, current_density_neg_110)
                    variant_summary_neg_110_wells = np.append(variant_summary_neg_110_wells, wellID)
            elif analysis_type == 'ssDeact CD -50':
                [current_density] = ssDeact_analyse_CD_neg_50mV(os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps)
                if current_density != 'N/A':
                    variant_summary_table = np.append(variant_summary_table, current_density)
                    variant_summary_wells = np.append(variant_summary_wells, wellID)
            elif analysis_type == 'ssDeact CD -40':
                [current_density] = ssDeact_analyse_CD_neg_40mV(os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]), wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, 3, total_sweeps)
                if current_density != 'N/A':
                    variant_summary_table = np.append(variant_summary_table, current_density)
                    variant_summary_wells = np.append(variant_summary_wells, wellID)
            elif analysis_type == 'ssAct':
                [pos40mVCD, returnV05, returnDG, returnK, returnz] = ssAct_fit_py(os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]),
                    os.path.join(output_dir, variant),
                    wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, rsquare,
                    summary_voltage, total_sweeps)
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

            elif analysis_type == 'Onset':
                [zeromVtau, peak_current] = onset_fit_py(
                    os.path.join(output_parent_dir, success_qc_dir, variant, variant_files[data_file]),
                    os.path.join(output_dir, variant, wellID + '.csv'),
                    wellID, os.path.join(output_plots, variant), int(num_sweeps), variant, rsquare,
                    summary_voltage, total_sweeps)
                if zeromVtau != 'N/A' and variant != 'neg_ctrl':
                    variant_summary_table = np.append(variant_summary_table, zeromVtau)
                    variant_summary_wells = np.append(variant_summary_wells, wellID)
                    variant_peak_table = np.append(variant_peak_table, peak_current)


        if analysis_type == 'Onset':
            if variant != 'neg_ctrl':
                [summary_table, no_well_summary_table] = append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table, variant_peak_table, analysis_type)

        elif analysis_type == 'ssDeact Fit':
            if variant != 'neg_ctrl':
                [summary_table, no_well_summary_table] = append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table, [], analysis_type)

        elif analysis_type == 'ssDeact CD -50/-120':
            if variant != 'neg_ctrl':
                [summary_table, no_well_summary_table] = append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table, [], analysis_type)
                [summary_table_neg_50, no_well_summary_table_neg_50] = append_summary_results(variant_summary_neg_50_table, variant_summary_neg_50_wells, summary_table_neg_50, no_well_summary_table_neg_50, [], analysis_type)
                [summary_table_neg_120, no_well_summary_table_neg_120] = append_summary_results(variant_summary_neg_120_table, variant_summary_neg_120_wells, summary_table_neg_120, no_well_summary_table_neg_120, [], analysis_type)
        elif analysis_type == 'ssDeact CD -40/-110':
            if variant != 'neg_ctrl':
                [summary_table, no_well_summary_table] = append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table, [], analysis_type)
                [summary_table_neg_40, no_well_summary_table_neg_40] = append_summary_results(variant_summary_neg_40_table, variant_summary_neg_40_wells, summary_table_neg_40, no_well_summary_table_neg_40, [], analysis_type)
                [summary_table_neg_110, no_well_summary_table_neg_110] = append_summary_results(variant_summary_neg_110_table, variant_summary_neg_110_wells, summary_table_neg_110, no_well_summary_table_neg_110, [], analysis_type)

        elif analysis_type == 'ssDeact CD -50 250/500':
            if variant != 'neg_ctrl':
                [summary_250ms_table, no_well_summary_250ms_table] = append_summary_results(variant_summary_250ms_table, variant_summary_250ms_wells, summary_250ms_table, no_well_summary_250ms_table, [], analysis_type)
                [summary_500ms_table, no_well_summary_500ms_table] = append_summary_results(variant_summary_500ms_table, variant_summary_500ms_wells, summary_500ms_table, no_well_summary_500ms_table, [], analysis_type)
        elif analysis_type == 'ssDeact CD -40 250/500':
            if variant != 'neg_ctrl':
                [summary_250ms_table, no_well_summary_250ms_table] = append_summary_results(variant_summary_250ms_table, variant_summary_250ms_wells, summary_250ms_table, no_well_summary_250ms_table, [], analysis_type)
                [summary_500ms_table, no_well_summary_500ms_table] = append_summary_results(variant_summary_500ms_table, variant_summary_500ms_wells, summary_500ms_table, no_well_summary_500ms_table, [], analysis_type)

        elif analysis_type == 'ssDeact CD -50':
            [summary_table, no_well_summary_table] = append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table, [], analysis_type)
        elif analysis_type == 'ssDeact CD -40':
            [summary_table, no_well_summary_table] = append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table, [], analysis_type)

        elif analysis_type == 'ssAct':
            [summary_table, no_well_summary_table] = append_summary_results(variant_summary_table, variant_summary_wells, summary_table, no_well_summary_table, [], analysis_type)
            if variant != 'neg_ctrl':
                [V05_summary_table, V05_no_well_summary_table] = append_summary_results(V05_variant_summary_table, V05_variant_summary_wells, V05_summary_table, V05_no_well_summary_table, [], analysis_type)
                [DG_summary_table, DG_no_well_summary_table] = append_summary_results(DG_variant_summary_table, DG_variant_summary_wells, DG_summary_table, DG_no_well_summary_table, [], analysis_type)
                [k_summary_table, k_no_well_summary_table] = append_summary_results(k_variant_summary_table, k_variant_summary_wells, k_summary_table, k_no_well_summary_table, [], analysis_type)
                [z_summary_table, z_no_well_summary_table] = append_summary_results(z_variant_summary_table, z_variant_summary_wells, z_summary_table, z_no_well_summary_table, [], analysis_type)

        var_tok = time.time()
        variant_elapsed_time_secs = var_tok - var_tic
        variant_elapsed_time_mins = variant_elapsed_time_secs / 60
        variant_elapsed_time_hours = variant_elapsed_time_mins / 60
        rem_variant_elapsed_time_mins = variant_elapsed_time_mins % 60

        print('Elapsed Run-Time for Variant ' + variant + ' was ' + str(
            math.floor(variant_elapsed_time_hours)) + ' hours and ' + str(math.floor(rem_variant_elapsed_time_mins)) + ' minutes.')



    if analysis_type != 'AP pre-stim' and analysis_type != 'mod FAIV' and analysis_type != 'ssDeact CD -50 250/500' and analysis_type != 'ssDeact CD -40 250/500' and analysis_type != 'ssDeact CD -50/-120' and analysis_type != 'ssDeact CD -40/-110':
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

    if analysis_type == 'ssDeact CD -50 250/500':
        # Now write the output
        summary_250ms_table = summary_250ms_table.transpose()
        no_well_summary_250ms_table = no_well_summary_250ms_table.transpose()
        # print(np.shape(summary_table))

        with open(summary_250ms_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_250ms_table)[0]):
                result_writer.writerow(summary_250ms_table[row])

        with open(no_well_summary_250ms_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(no_well_summary_250ms_table)[0]):
                result_writer.writerow(no_well_summary_250ms_table[row])

        summary_500ms_table = summary_500ms_table.transpose()
        no_well_summary_500ms_table = no_well_summary_500ms_table.transpose()
        # print(np.shape(summary_table))

        with open(summary_500ms_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_500ms_table)[0]):
                result_writer.writerow(summary_500ms_table[row])

        with open(no_well_summary_500ms_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(no_well_summary_500ms_table)[0]):
                result_writer.writerow(no_well_summary_500ms_table[row])
    if analysis_type == 'ssDeact CD -40 250/500':
        # Now write the output
        summary_250ms_table = summary_250ms_table.transpose()
        no_well_summary_250ms_table = no_well_summary_250ms_table.transpose()
        # print(np.shape(summary_table))

        with open(summary_250ms_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_250ms_table)[0]):
                result_writer.writerow(summary_250ms_table[row])

        with open(no_well_summary_250ms_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(no_well_summary_250ms_table)[0]):
                result_writer.writerow(no_well_summary_250ms_table[row])

        summary_500ms_table = summary_500ms_table.transpose()
        no_well_summary_500ms_table = no_well_summary_500ms_table.transpose()
        # print(np.shape(summary_table))

        with open(summary_500ms_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_500ms_table)[0]):
                result_writer.writerow(summary_500ms_table[row])

        with open(no_well_summary_500ms_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(no_well_summary_500ms_table)[0]):
                result_writer.writerow(no_well_summary_500ms_table[row])

    if analysis_type == 'ssDeact CD -50/-120':
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

        summary_table_neg_50 = summary_table_neg_50.transpose()
        no_well_summary_table_neg_50 = no_well_summary_table_neg_50.transpose()
        # print(np.shape(summary_table))

        with open(summary_neg_50_CD_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_table_neg_50)[0]):
                result_writer.writerow(summary_table_neg_50[row])

        with open(no_well_summary_neg_50_CD_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(no_well_summary_table_neg_50)[0]):
                result_writer.writerow(no_well_summary_table_neg_50[row])

        summary_table_neg_120 = summary_table_neg_120.transpose()
        no_well_summary_table_neg_120 = no_well_summary_table_neg_120.transpose()
        # print(np.shape(summary_table))

        with open(summary_neg_120_CD_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_table_neg_120)[0]):
                result_writer.writerow(summary_table_neg_120[row])

        with open(no_well_summary_neg_120_CD_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(no_well_summary_table_neg_120)[0]):
                result_writer.writerow(no_well_summary_table_neg_120[row])

    if analysis_type == 'ssDeact CD -40/-110':
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

        summary_table_neg_40 = summary_table_neg_40.transpose()
        no_well_summary_table_neg_40 = no_well_summary_table_neg_40.transpose()
        # print(np.shape(summary_table))

        with open(summary_neg_40_CD_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_table_neg_40)[0]):
                result_writer.writerow(summary_table_neg_40[row])

        with open(no_well_summary_neg_40_CD_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(no_well_summary_table_neg_40)[0]):
                result_writer.writerow(no_well_summary_table_neg_40[row])

        summary_table_neg_110 = summary_table_neg_110.transpose()
        no_well_summary_table_neg_110 = no_well_summary_table_neg_110.transpose()
        # print(np.shape(summary_table))

        with open(summary_neg_110_CD_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(summary_table_neg_110)[0]):
                result_writer.writerow(summary_table_neg_110[row])

        with open(no_well_summary_neg_110_CD_filename, mode='w') as result_output:
            result_writer = csv.writer(result_output, lineterminator='\n')
            for row in range(0, np.shape(no_well_summary_table_neg_110)[0]):
                result_writer.writerow(no_well_summary_table_neg_110[row])

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



    total_tok = time.time()
    elapsed_time_secs = total_tok - total_tic
    elapsed_time_mins = elapsed_time_secs / 60
    elapsed_time_hours = elapsed_time_mins / 60
    rem_elapsed_time_mins = elapsed_time_mins % 60
    print('Total Elapsed Run-Time was ' + str(math.floor(elapsed_time_hours)) + ' hours and ' + str(
        math.floor(rem_elapsed_time_mins)) + ' minutes.')


def main():
    # Where to call the function from
    #high_throughput(os.path.join('Z://', 'SyncroPatch_validation'), '25032021_CJ', 'QC_success_1-30', 0.85, os.path.join('variant names', '25032021_CJ.txt'), 40, 13, 'ssAct')
    #high_throughput(os.path.join('Z://', 'Syncropatch_WThERG'), '22102020_AN', 'success_QC_tail_current_peak_check', 0.85, os.path.join('variant names', '22102020_AN.txt'), 40, 13, 'ssAct')

    #high_throughput(os.path.join('Z://', 'Functional_Genomics_Syncropatch', 'KCNH2', 'exon2'), '03102019_AN2', 'success_QC no series resistance', 0.99, os.path.join('variant names', '03102019_AN2.txt'), 0, 12, 'Onset')

    #high_throughput(os.path.join('Z://', 'Syncropatch'), '22102020_AN3', 'success_QC', 0.99, os.path.join('variant names', '22102020_AN3.txt'), 0, 12, 'Onset')

    #high_throughput(os.path.join('Z://', 'Functional_Genomics_Syncropatch', 'KCNH2', 'exon2'), '10102019_AN2', 'success_QC no series resistance -120mV filtering automate pandas', 0.85, os.path.join('variant names', '10102019_AN2.txt'), -50, 18, 'ssDeact CD -50/-120')

    #high_throughput(os.path.join('Z://', 'Functional_Genomics_Syncropatch', 'KCNH2', 'exon2'), '10102019_AN2', 'success_QC_test_pandas', 0.85, os.path.join('variant names', '10102019_AN2.txt'), 40, 13, 'ssAct')

    #high_throughput(os.path.join('Z://', 'Functional_Genomics_Syncropatch', 'KCNH2', 'Tris-HCl'), '16122021_AN', 'success_QC_test_pandas', 0.85, os.path.join('variant names', '16122021_AN.txt'), -50, 18, 'ssDeact Fit')

    #high_throughput(os.path.join('Z://', 'Functional_Genomics_Syncropatch', 'KCNH2', 'Clinical_variant_Brett'), '24032022_AN', 'success_QC', 0.85, os.path.join('variant names', '24032022_AN.txt'), 40, 13, 'ssAct')

    #high_throughput(os.path.join('Z://', 'Functional_Genomics_Syncropatch', 'KCNH2', 'Clinical_variant_Brett'), '03032022_AN', 'success_QC', 0.85, os.path.join('variant names', '03032022_AN.txt'), -40, 18, 'ssDeact CD -40 250/500')

    #high_throughput(os.path.join('Z://', 'Functional_Genomics_Syncropatch', 'KCNH2', 'Clinical_variant_Brett'), '07042022_AN3', 'success_QC', 0.85, os.path.join('variant names', '07042022_AN3.txt'), -50, 18, 'ssDeact CD -50 250/500')

    high_throughput(os.path.join('Z://', 'Functional_Genomics_Syncropatch', 'KCNH2', 'Clinical_variant_Brett'), '17022022_AN2', 'success_QC', 0.85, os.path.join('variant names', '17022022_AN.txt'), 40, 13, 'ssAct')

    '''
    high_throughput(os.path.join('Z://', 'Syncropatch'), '03102019_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '03102019_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '04062020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '04062020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '04062020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '04062020_AN4.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '05032020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '05032020_AN.txt'), 0, 12, 'Onset')

    high_throughput(os.path.join('Z://', 'Syncropatch'), '05032020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '05032020_AN2.txt'), 0, 12, 'Onset')

    high_throughput(os.path.join('Z://', 'Syncropatch'), '05092019_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '05092019_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '05122019_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '05122019_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '05122019_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '05122019_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '07052020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '07052020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '07052020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '07052020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '10102019_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '10102019_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '10102019_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '10102019_AN2.txt'), 0, 12, 'Onset')

    high_throughput(os.path.join('Z://', 'Syncropatch'), '12032020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '12032020_AN.txt'), 0, 12, 'Onset')

    high_throughput(os.path.join('Z://', 'Syncropatch'), '12032020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '12032020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '12092019_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '12092019_AN2.txt'), 0, 12, 'Onset')

    high_throughput(os.path.join('Z://', 'Syncropatch'), '12122019_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '12122019_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '12122019_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '12122019_AN2.txt'), 0, 12, 'Onset')

    high_throughput(os.path.join('Z://', 'Syncropatch'), '13022020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '13022020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '13022020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '13022020_AN2.txt'), 0, 12, 'Onset')

    high_throughput(os.path.join('Z://', 'Syncropatch'), '14032019_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '14032019_AN.txt'), 0, 12, 'Onset')


    high_throughput(os.path.join('Z://', 'Syncropatch'), '14032019_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '14032019_AN2.txt'), 0, 12, 'Onset')

    high_throughput(os.path.join('Z://', 'Syncropatch'), '14052020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '14052020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '14052020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '14052020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '14052020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '14052020_AN3.txt'), 0, 12, 'Onset')
    '''
    '''
    high_throughput(os.path.join('Z://', 'Syncropatch'), '14052020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '14052020_AN4.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '16042020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '16042020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '16042020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '16042020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '17102019_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '17102019_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '17102019_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '17102019_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '19092019_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '19092019_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '19092019_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '19092019_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '21022020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '21022020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '21022020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '21022020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '21052020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '21052020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '21052020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '21052020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '21052020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '21052020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '21052020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '21052020_AN4.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '21112019_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '21112019_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '21112019_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '21112019_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '24102019_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '24102019_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '24102019_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '24102019_AN2.txt'), 0, 12, 'Onset')

    high_throughput(os.path.join('Z://', 'Syncropatch'), '26092019_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '26092019_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '26092019_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '26092019_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '27022020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '27022020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '27022020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '27022020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '28052020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '28052020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '28052020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '28052020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '28052020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '28052020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '28052020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '28052020_AN4.txt'), 0, 12, 'Onset')
    '''
    '''
    high_throughput(os.path.join('Z://', 'Syncropatch'), '02072020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '02072020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '02072020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '02072020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '02072020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '02072020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '02072020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '02072020_AN4.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '03092020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '03092020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '03092020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '03092020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '06082020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '06082020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '06082020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '06082020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '06082020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '06082020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '06082020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '06082020_AN4.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '09072020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '09072020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '09072020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '09072020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '09072020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '09072020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '09072020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '09072020_AN4.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '13082020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '13082020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '13082020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '13082020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '13082020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '13082020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '13082020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '13082020_AN4.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '16072020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '16072020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '16072020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '16072020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '16072020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '16072020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '16072020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '16072020_AN4.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '20082020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '20082020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '20082020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '20082020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '20082020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '20082020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '20082020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '20082020_AN4.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '23072020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '23072020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '23072020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '23072020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '23072020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '23072020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '23072020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '23072020_AN4.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '27082020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '27082020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '27082020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '27082020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '27082020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '27082020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '27082020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '27082020_AN4.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '30072020_AN', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '30072020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '30072020_AN2', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '30072020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '30072020_AN3', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '30072020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '30072020_AN4', 'success_QC no series resistance', 0.99,
                    os.path.join('variant names', '30072020_AN4.txt'), 0, 12, 'Onset')
    '''

    #high_throughput(os.path.join('Z://', 'Syncropatch'), '22102020_AN', 'success_QC no series resistance -120mV filtering', 0.85, os.path.join('variant names', '22102020_AN.txt'), -50, 18, 'ssDeact CD -50/-120')
    '''
    
    high_throughput(os.path.join('Z://', 'Syncropatch'), '22102020_AN', 'success_QC no series resistance', 0.99, os.path.join('variant names', '22102020_AN.txt'), 0, 12, 'Onset')
    
    high_throughput(os.path.join('Z://', 'Syncropatch'), '22102020_AN2', 'success_QC no series resistance', 0.99, os.path.join('variant names', '22102020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '22102020_AN3', 'success_QC no series resistance', 0.99, os.path.join('variant names', '22102020_AN3.txt'), 0, 12, 'Onset')
    
    high_throughput(os.path.join('Z://', 'Syncropatch'), '22102020_AN4', 'success_QC no series resistance', 0.99, os.path.join('variant names', '22102020_AN4.txt'), 0, 12, 'Onset')

    #high_throughput(os.path.join('Z://', 'Syncropatch'), '30042020_AN2', 'success_QC no series resistance', 0.99, os.path.join('variant names', '30042020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '29102020_AN', 'success_QC no series resistance', 0.99, os.path.join('variant names', '29102020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '29102020_AN2', 'success_QC no series resistance', 0.99, os.path.join('variant names', '29102020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '05112020_AN', 'success_QC no series resistance', 0.99, os.path.join('variant names', '05112020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '05112020_AN2', 'success_QC no series resistance', 0.99, os.path.join('variant names', '05112020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '04062020_AN', 'success_QC no series resistance', 0.99, os.path.join('variant names', '04062020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '04062020_AN2', 'success_QC no series resistance', 0.99, os.path.join('variant names', '04062020_AN2.txt'), 0, 12, 'Onset')
    #high_throughput(os.path.join('Z://', 'Syncropatch'), '07052020_AN3', 'success_QC no series resistance', 0.99, os.path.join('variant names', '07052020_AN3.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '30042020_AN', 'success_QC no series resistance', 0.99, os.path.join('variant names', '30042020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '23042020_AN', 'success_QC no series resistance', 0.99, os.path.join('variant names', '23042020_AN.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '23042020_AN2', 'success_QC no series resistance', 0.99, os.path.join('variant names', '23042020_AN2.txt'), 0, 12, 'Onset')
    high_throughput(os.path.join('Z://', 'Syncropatch'), '30042020_AN2', 'success_QC no series resistance', 0.99, os.path.join('variant names', '30042020_AN2.txt'), 0, 12, 'Onset')
    '''
    #high_throughput(os.path.join('Z://', 'SyncroPatch_validation'), '11032021_CJ', 'success_QC', 0.85,os.path.join('variant names', '11032021_CJ.txt'), 40, 13, 'ssAct')

    #high_throughput(os.path.join('Z://', 'Syncropatch_WThERG'), '22102020_AN', 'success_QC', 0.85, os.path.join('variant names', '22102020_AN.txt'), -50, 18, 'ssDeact Fit')
    #high_throughput(os.path.join('Z://', 'Syncropatch_WThERG'), '22102020_AN', 'success_QC', 0.85, os.path.join('variant names', '22102020_AN.txt'), -50, 18, 'ssDeact CD -50')
    #high_throughput(os.path.join('Z://', 'Syncropatch_WThERG'), '22102020_AN', 'success_QC', 0.85, os.path.join('variant names', '22102020_AN.txt'), -50, 18, 'ssDeact CD -50/-120')
    #high_throughput(os.path.join('Z://', 'Syncropatch_WThERG'), '22102020_AN', 'success_QC', 0.99, os.path.join('variant names', '22102020_AN.txt'), 0, 12, 'Onset')
    #high_throughput(os.path.join('Z://', 'Syncropatch_WThERG'), '22102020_AN', 'success_QC', 0.85, os.path.join('variant names', '22102020_AN.txt'), 40, 13, 'ssAct')

    ## Enter your custom input parameters here:
    # high_throughput(parent dir, plate name, QC dir, fit RSquared threshold, variant filename path, summary sweep voltage, number of sweeps, protocol)

if __name__ == '__main__':
    main()

