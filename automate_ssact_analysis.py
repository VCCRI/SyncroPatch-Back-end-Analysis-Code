
import os
import glob
import numpy as np
import time
from reorder_QC import reorder_QC




def automate_ssact_analysis(parent_dir, variant_dir, seal, cap_upper, cap_lower, series, peak, output_plots, output_dir, sweep_length):
    plate_dirs = glob.glob(os.path.join(parent_dir, '*_AN*'))
    failed_plates = np.array([])
    for i in range(0, len(plate_dirs)):
        print(plate_dirs[i])
        plate_name = os.path.basename(plate_dirs[i])
        plate_date = plate_name.split('_')[0]

        plate_qc_file = glob.glob(os.path.join(parent_dir, plate_dirs[i], '*ssAct*', '*ssAct*', '*parameters*'))


        plate_variant_file = glob.glob(os.path.join(parent_dir, 'variant names', '*'+plate_name+'.txt'))
        print(plate_qc_file)
        print(plate_variant_file)
        if len(plate_qc_file) > 0:
            if len(plate_variant_file) > 0:
                #print('run')
                plate_qc_path = os.path.dirname((plate_qc_file)[0])

                if plate_name == '13122018_AN2' or plate_name == '13122018_AN':
                    continue

                plots_dir = os.path.join(parent_dir, 'Data Analysis Results ssAct', plate_name, 'plots no series QC')

                #if os.path.isdir(plots_dir):
                #    continue


                from automate_quality_control_sat_mut_py import automate_quality_control_sat_mut_py as qc
                from automate_high_throughput_sat_mut_python import automate_high_throughput

                #reorder_QC(plate_qc_path, plate_name, os.path.basename(plate_qc_file[0]), 13)
                # qc(plate_qc_path, plate_name, os.path.basename(plate_qc_file[0]) , plate_variant_file[0], 13, 'ssAct', 'off')
                reorder_plate_qc_file = glob.glob( os.path.join(parent_dir, plate_dirs[i], '*ssAct*', '*Rectified file order*', '*parameters*'))
                reorder_plate_qc_path = os.path.dirname((reorder_plate_qc_file)[0])

                qc(parent_dir, reorder_plate_qc_path, plate_name, os.path.basename(plate_qc_file[0]), plate_variant_file[0], 13, 'ssAct', seal, cap_upper, cap_lower, series, peak)
                automate_high_throughput(parent_dir, plate_name, 'success_QC no series resistance', 0.85, plate_variant_file[0], 40, 13, 'ssAct', output_plots, output_dir, sweep_length)

            else:
                failed_plates = np.append(failed_plates, plate_name)
        else:
            failed_plates = np.append(failed_plates, plate_name)

    print(failed_plates)
def main():

    automate_ssact_analysis(os.path.join('Z://', 'Syncropatch'), os.path.join('Z://', 'Syncropatch', 'variant names'), 300E6, 50E-12, 5E-12, 20E6, 100E-12, 'plots no series QC', 'results no series QC', 3)

if __name__ == '__main__':
    main()
