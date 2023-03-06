
import os
import numpy as np
import csv
import shutil
import glob
import time
import statistics as sts
import matplotlib.pyplot as plt
import winsound


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



def AP_pre_stim_QC_intersection(parent_dir, success_control, success_drug, srvr_analysis):
    if srvr_analysis == 'on':
        input_srvr = input('What is the name of the drive that the server is present on: ')
        # TO D: String refinement
        # Assume just enter the letter
        input_srvr = input_srvr + '://'

        par_dir_prompt = input('Would you like to change directories into a base directory?: ')
        found_dir = 0
        while 1:
            if par_dir_prompt == 'yes':
                while 1:
                    base_dir = input('What is the name of this directory?: ')
                    srvr_path = os.path.join(input_srvr, base_dir)
                    if not os.path.isdir(srvr_path):
                        quote = '\''
                        print(
                            'The directory ' + quote + srvr_path + quote + ' was not found. Please enter one that exists.')
                    else:
                        found_dir = 1
                        break
                if found_dir == 1:
                    break
            elif par_dir_prompt == 'no':
                srvr_path = input_srvr
                break
            else:
                par_dir_prompt = input('Would you like to change directories into a base directory?: ')
        os.chdir(srvr_path)

    cwd_path = os.getcwd()

    result_parent_dir = 'Data Analysis Results AP pre-stim'
    result_parent_dir = os.path.join(cwd_path, result_parent_dir)
    if not os.path.isdir(result_parent_dir):
        os.mkdir(result_parent_dir)
        parent_dir = os.path.join(result_parent_dir, parent_dir)
        if not os.path.isdir(parent_dir):
            os.mkdir(parent_dir)
    else:
        parent_dir = os.path.join(result_parent_dir, parent_dir)
        if not os.path.isdir(parent_dir):
            os.mkdir(parent_dir)

    output_prompt = 'What would you like to name the directory that stores the files that are present in both control and drug directories?: '
    output_dir = prompt_user(output_prompt, 'dir', parent_dir, 0)

    os.mkdir(os.path.join(output_dir, 'control'))
    os.mkdir(os.path.join(output_dir, 'drug'))








def main():



if __name__ == '__main__':
    main()