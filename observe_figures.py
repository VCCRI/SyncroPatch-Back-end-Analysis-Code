import os
import csv
import warnings
import time
import pickle
import matplotlib.pyplot as plt

def plot_figures(full_trace, sweep, cwd_path, plots_path, well):
    if full_trace == 'on':
        file_name = os.path.join(cwd_path, plots_path, well, well + '_Sweep' + str(sweep)) + '_full_trace.pickle'
        with open(file_name, 'rb') as fig_file:
            pickle.load(fig_file)
            #plt.show()

        fig_file.close()
    elif full_trace == 'off':
        file_name = os.path.join(cwd_path, plots_path, well, well + '_Sweep' + str(sweep)) + '.pickle'
        with open(file_name, 'rb') as fig_file:
            pickle.load(fig_file)
            #plt.show()

        fig_file.close()
    elif full_trace == 'both':
        file_name = os.path.join(cwd_path, plots_path, well, well + '_Sweep' + str(sweep)) + '.pickle'
        with open(file_name, 'rb') as fig_file:
            pickle.load(fig_file)
        # plt.show()

        fig_file.close()

        file_name = os.path.join(cwd_path, plots_path, well, well + '_Sweep' + str(sweep)) + '_full_trace.pickle'
        with open(file_name, 'rb') as fig_file:
            pickle.load(fig_file)
        #plt.show()

        fig_file.close()


def observe_figure(srvr_analysis, plots_path, well, sweep, full_trace, analysis_type):
    '''
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
    '''


    fast_srvr_path = 'Z:'
    os.chdir(fast_srvr_path)
    cwd_path = os.getcwd()

    #os.chdir(os.path.join(cwd_path, well))
    if sweep == 'all':
        if analysis_type == 'ssDeact Fit':
            max_sweeps = 18
        elif analysis_type == 'ssAct':
            max_sweeps = 13
        elif analysis_type == 'Onset Inact':
            max_sweeps = 12

        if analysis_type != 'ssDeact CD':
            for sw in range(1, max_sweeps+1):
                if full_trace == 'off':
                    if os.path.isfile(os.path.join(cwd_path, plots_path, well, well + '_Sweep' + str(sw) + '.pickle')):
                        plot_figures(full_trace, sw, cwd_path, plots_path, well)
                if full_trace == 'on':
                    if os.path.isfile(os.path.join(cwd_path, plots_path, well, well + '_Sweep' + str(sw) + '.pickle')):
                        plot_figures(full_trace, sw, cwd_path, plots_path, well)
                elif full_trace == 'both':
                    if os.path.isfile(os.path.join(cwd_path, plots_path, well, well + '_Sweep' + str(sw) + '.pickle')):
                        if os.path.isfile(os.path.join(cwd_path, plots_path, well, well + '_Sweep' + str(sw) + '.pickle')):
                            plot_figures(full_trace, sw, cwd_path, plots_path, well)
        else:
            plot_figures(full_trace, 8, cwd_path, plots_path, well)
            plot_figures(full_trace, 15, cwd_path, plots_path, well)


    else:
        plot_figures(full_trace, sweep, cwd_path, plots_path, well)
        #plt.show()

    plt.show()

def main():
    #observe_figure('on', os.path.join('Syncropatch', 'Data Analysis Results ssDeact', '30042020_AN', 'plots_neg_50_test', 'WT1a_WT1a'), 'B01', '18', 'both', 'ssDeact')
    #observe_figure('on', os.path.join('Syncropatch', 'Data Analysis Results ssAct', '30042020_AN', 'plots_neg_50_test', 'WT1a_WT1a'), 'B01', 'all', 'off', 'ssAct')
    #observe_figure('on', os.path.join('Syncropatch', 'Data Analysis Results Onset Inact', '30042020_AN', 'plots_neg_50_test', 'WT1a_WT1a'), 'B01', 'all', 'off', 'Onset Inact')
    wellID = input('What is the wellID of interest?:\n')
    observe_figure('on', os.path.join('', 'Syncropatch', 'Data Analysis Results ssDeact', '22102020_AN', 'plots no series QC -120mV filtering 200pA -50mV thresh', 'WT1a_WT1a_0'), wellID, 17, 'both', 'ssDeact Fit')

if __name__ == '__main__':
    main()