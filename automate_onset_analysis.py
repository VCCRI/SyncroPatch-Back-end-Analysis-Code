
import os
import glob
import numpy as np
import time




def automate_onset_analysis(parent_dir, variant_dir, seal, cap_upper, cap_lower, series, peak, output_plots, output_dir, sweep_length):
    plate_dirs = glob.glob(os.path.join(parent_dir, '*_AN*'))
    failed_plates = np.array([])
    for i in range(0, len(plate_dirs)):
        print(plate_dirs[i])
        plate_name = os.path.basename(plate_dirs[i])
        plate_date = plate_name.split('_')[0]
        #print(plate_name)
        #print(plate_date)

        plate_qc_file = glob.glob(os.path.join(parent_dir, plate_dirs[i], '*Onset*', '*Onset*', '*parameters*'))

        plate_variant_file = glob.glob(os.path.join(parent_dir, 'variant names', '*'+plate_name+'.txt'))
        print(plate_qc_file)
        print(plate_variant_file)
        if len(plate_qc_file) > 0:
            if len(plate_variant_file) > 0:
                #print('run')
                plate_qc_path = os.path.dirname((plate_qc_file)[0])
                #print(plate_qc_path)
                from automate_quality_control_sat_mut_py import automate_quality_control_sat_mut_py as qc
                from automate_high_throughput_sat_mut_python import automate_high_throughput
                qc(parent_dir, plate_qc_path, plate_name, os.path.basename(plate_qc_file[0]), plate_variant_file[0], 12, 'Onset', seal, cap_upper, cap_lower, series, peak)

                automate_high_throughput(parent_dir, plate_name, 'success_QC test', 0.99, plate_variant_file[0], 0, 12, 'Onset', output_plots, output_dir, sweep_length)
            else:
                failed_plates = np.append(failed_plates, plate_name)
        else:
            failed_plates = np.append(failed_plates, plate_name)

    print(failed_plates)
def main():

    #automate_onset_analysis(os.path.join('Z://', 'Syncropatch'), os.path.join('Z://', 'Syncropatch', 'variant names'), 300E6, 50E-12, 5E-12, 15E6, 100E-12, 'plots test', 'results test', 3)
    parent_dir = os.path.join('Z://', 'Syncropatch')
    variant_dir = os.path.join('Z://', 'Syncropatch', 'variant names')
    seal = 300E6
    cap_upper = 50E-12
    cap_lower = 5E-12
    series = 15E6
    peak = 100E-12
    output_plots = 'plots no series QC mem test'
    output_dir = 'results no series QC mem test'
    sweep_length = 3



    plate_dirs = glob.glob(os.path.join(parent_dir, '*_AN*'))
    failed_plates = np.array([])
    for i in range(0, len(plate_dirs)):
        print(plate_dirs[i])
        plate_name = os.path.basename(plate_dirs[i])
        plate_date = plate_name.split('_')[0]
        # print(plate_name)
        # print(plate_date)

        plate_qc_file = glob.glob(os.path.join(parent_dir, plate_dirs[i], '*Onset*', '*Onset*', '*parameters*'))

        plate_variant_file = glob.glob(os.path.join(parent_dir, 'variant names', '*' + plate_name + '.txt'))
        print(plate_qc_file)
        print(plate_variant_file)
        if len(plate_qc_file) > 0:
            if len(plate_variant_file) > 0:
                # print('run')
                plate_qc_path = os.path.dirname((plate_qc_file)[0])
                # print(plate_qc_path)
                from automate_quality_control_sat_mut_py import automate_quality_control_sat_mut_py as qc
                from automate_high_throughput_sat_mut_python import automate_high_throughput
                qc(parent_dir, plate_qc_path, plate_name, os.path.basename(plate_qc_file[0]), plate_variant_file[0], 12,
                   'Onset', seal, cap_upper, cap_lower, series, peak)

                automate_high_throughput(parent_dir, plate_name, 'success_QC_mem_test', 0.99, plate_variant_file[0], 0, 12,
                                         'Onset', output_plots, output_dir, sweep_length)
            else:
                failed_plates = np.append(failed_plates, plate_name)
        else:
            failed_plates = np.append(failed_plates, plate_name)

    print(failed_plates)
if __name__ == '__main__':
    main()
