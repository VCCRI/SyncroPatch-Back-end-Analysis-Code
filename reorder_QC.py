
import glob
import os
import csv
import numpy as np
import time
import shutil
from shutil import copyfile

def reorder_QC(plate_qc_path, plate_name, qc_file , num_sweeps):
    print('reorder')
    print(plate_qc_path)

    output_dir = plate_qc_path + '_Rectified file order'

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    else:
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)



    all_current_files = glob.glob(os.path.join(plate_qc_path, '*'))

    for i in range(0, len(all_current_files)):
        current_file = all_current_files[i]

        result_file = os.path.basename(current_file)
        result_output = os.path.join(output_dir, result_file)
        #print(result_output)
        if 'parameters' in current_file:
            #print('param file')
            copyfile(current_file, result_output)
            continue

        #continue
        rawWellData = []
        with open(current_file) as csvfile:
            read = csv.reader(csvfile, delimiter='\t')
            for row in read:
                rawWellData.append(row)
                #print(np.shape(rawWellData))
                #rawWellData = np.append(rawWellData, [row])


        sweep_counts = rawWellData[0]
        #print(sweep_counts)
        sweep_voltage_header = rawWellData[1]
        raw_stim_header = rawWellData[2]
        current_data = np.array(rawWellData[3:])
        #print(np.shape(current_data))

        newWellData = np.array(current_data[:, 0:2])
        #print(current_data[:, 0:2])
        #print(np.shape(newWellData))
        newWellData = np.vstack(([raw_stim_header[0:2]], newWellData))
        #print(raw_stim_header[0:2])
        newWellData = np.vstack(([sweep_voltage_header[0:2]], newWellData))
        #print(sweep_voltage_header[0:1])
        newWellData = np.vstack(([sweep_counts[0:2]], newWellData))

        newWellData = newWellData.transpose()
        #print(sweep_counts[0:1])

        #print(newWellData)

        newRawWellData = []
        for required_sweep in range(1, num_sweeps+1):
            result = []
            v_result = []
            for sw in range(3, len(sweep_counts), 2):
                #print(sweep_counts[sw])
                if int(sweep_counts[sw]) == required_sweep:
                    #print(required_sweep)
                    result = current_data[:, sw]
                    result = np.hstack(([raw_stim_header[sw]], result))
                    result = np.hstack(([sweep_voltage_header[sw]], result))
                    result = np.hstack(([sweep_counts[sw]], result))

                    v_result = current_data[:, sw-1]
                    v_result = np.hstack(([raw_stim_header[sw-1]], v_result))
                    v_result = np.hstack(([sweep_voltage_header[sw-1]], v_result))
                    v_result = np.hstack(([sweep_counts[sw-1]], v_result))

                    #print(result)
                    #print(v_result)

                    newWellData = np.vstack((newWellData, v_result))
                    newWellData = np.vstack((newWellData, result))

                    break

        newWellData = newWellData.transpose()
        #print(newWellData)

        with open(result_output, mode='w') as write:
            result_writer = csv.writer(write, lineterminator='\n', delimiter='\t')
            for row in range(0, np.shape(newWellData)[0]):
                result_writer.writerow(newWellData[row])



    print('bye')



def main():
    reorder_QC()

if __name__ == '__main__':
        main()
