import random
import sys
import ctypes
import glob
import os
import calendar
import pandas as pd
import numpy as np
import re
from tkinter import *
import logging
import time
import glob
import multiprocessing
import itertools
from extract_raw_data import Json_Data, Well
import tracemalloc
from KCNH2_ssDeact_HT import high_throughput_ssDeact
from KCNH2_ssAct_HT import high_throughput_ssAct
from KCNH2_OnsetInact_HT import high_throughput_onset_inact

logging.basicConfig(level=logging.INFO)


def work(wellID, num_samples, num_sweeps, json_data, input_folder, start_index, end_index):

    data = np.zeros([num_sweeps, num_samples])

    well = Well(json_data, input_folder, wellID, 2)
    sw = 0
    for sweep in range(0, num_sweeps):
        # print(sweep)
        sw_curr = well.get_sweep_currents(sweep)
        data[sw, :] = sw_curr[start_index:end_index+1]
        sw += 1

    return data

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

        #ssAct
        #self.cursor_start = 1.205
        #self.cursor_end = 1.3

        #Onset
        #self.cursor_start = 1.175
        #self.cursor_end = 1.2



class PlateWidget():
    # well_widgets = QtCore.pyqtSignal()
    def __init__(self, input_folder):
        super(PlateWidget, self).__init__()


        self.input_folder = input_folder

        self.initialise_ui()

    def initialise_ui(self):

        start_time = time.time()
        self.tic = time.time()

        print(self.input_folder)
        json_filename = glob.glob(os.path.join(self.input_folder, '*.json'))
        print(json_filename)
        self.json_data = Json_Data(json_filename[0], 16, 24, 65)

        self.well_widgets = np.full((self.json_data.row_count, self.json_data.column_count), object())

        wellIDs = []

        count = 0
        sweep_times = np.array([])
        num_samples = np.nan
        sw = np.nan
        num_sweeps = np.nan

        # Initialise UI
        for col in range(1, self.json_data.column_count + 1):
            for row in range(1, self.json_data.row_count + 1):
                count += 1
                self.well_widgets[row - 1, col - 1] = WellWidgetPYQTGraph(self, row, col, self.json_data.row_count, self.json_data.column_count, sweep_times)
                if np.isnan(num_samples):
                    num_samples = self.well_widgets[row - 1, col - 1].num_sample_points
                    sw = self.well_widgets[row - 1, col - 1].visualising_sweep
                    plot_sample_points = self.well_widgets[row - 1, col - 1].plot_sample_points
                    #plot_indexes = self.well_widgets[row - 1, col - 1].plot_indexes
                    #start_index = self.well_widgets[row - 1, col - 1].plot_indexes[0]
                    #end_index = self.well_widgets[row - 1, col - 1].plot_indexes[-1]
                    start_index = 0
                    end_index = self.well_widgets[row - 1, col - 1].num_sample_points
                    num_sweeps = self.well_widgets[row - 1, col - 1].num_sweeps

                sweep_times = self.well_widgets[row - 1, col - 1].sweep_times
                wellIDs.append(self.well_widgets[row - 1, col - 1].wellID)


        num_cpus = int(multiprocessing.cpu_count())
        # num_cpus = 1
        print(num_cpus)
        pool = multiprocessing.Pool(num_cpus)
        data = pool.starmap(work, zip(wellIDs, itertools.repeat(num_samples), itertools.repeat(num_sweeps), itertools.repeat(self.json_data), itertools.repeat(self.input_folder), itertools.repeat(start_index), itertools.repeat(end_index)))

        count = 0
        for col in range(1, self.json_data.column_count + 1):
            for row in range(1, self.json_data.row_count + 1):
                self.well_widgets[row - 1, col - 1].sweep_currents[0:self.well_widgets[row - 1, col - 1].num_sweeps] = data[count]
                count += 1

        print(time.time()-self.tic)

class WellWidgetPYQTGraph():
    def __init__(self, parent, row, col, num_rows, num_cols, sweep_times):
        super(WellWidgetPYQTGraph, self).__init__()

        self.parent = parent

        self.cap_lower_QC_input = 5*1e-12
        self.cap_upper_QC_input = 15 * 1e-12
        self.seal_QC_input = 300*1e6
        self.SR_QC_input = 20*1e6

        self.visualising_sweep = 1

        self.row = row
        self.col = col
        if col < 10:
            self.wellID = chr(self.row + 64) + str(0) + str(col)
        else:
            self.wellID = chr(self.row + 64) + str(col)

        self.json_well_data = Well(self.parent.json_data, self.parent.input_folder, self.wellID, 2)
        # self.json_well_data = Well(json_data, input_folder, self.wellID, 2)
        #self.cursor_start = self.parent.json_data.cursor_start
        #self.cursor_end = self.parent.json_data.cursor_end
        self.cursor_start = self.parent.json_data.cursor_start
        self.cursor_end = self.parent.json_data.cursor_end

        self.num_sweeps = self.parent.json_data.total_sweeps

        self.initialise_data(sweep_times)

        self.variant = self.parent.json_data.variants[self.parent.json_data.variant_layout[self.row-1, self.col-1]]


    def initialise_data(self, sweep_times):

        self.sweep_cap_array = np.array([])
        self.sweep_seal_array = np.array([])
        self.sweep_series_array = np.array([])

        self.sweep_cap_array = self.json_well_data.get_capacitances()
        self.sweep_seal_array = self.json_well_data.get_seal_resistances()
        self.sweep_series_array = self.json_well_data.get_series_resistances()

        self.sweep_pass_qc_array = np.array([])
        self.num_sample_points = self.parent.json_data.sample_count
        if len(sweep_times) == 0:
            sweep_times = self.json_well_data.get_sweep_times()

        if self.cursor_start:
            self.plot_indexes = [i for i in range(0, len(sweep_times)) if sweep_times[i] >= self.cursor_start and sweep_times[i] <= self.cursor_end]
            self.plot_sample_points = len(self.plot_indexes)
            #self.sweep_times = sweep_times[self.plot_indexes[0]:self.plot_indexes[-1] + 1]
        else:
            self.plot_indexes = [i for i in range(0, len(sweep_times)) if sweep_times[i] >= sweep_times[0] and sweep_times[i] <= sweep_times[-1]]
            self.plot_sample_points = len(self.plot_indexes)
        self.sweep_times = sweep_times

        # self.sweep_currents = np.zeros([self.num_sweeps, self.plot_sample_points])
        self.sweep_currents = np.zeros([self.num_sweeps, self.num_sample_points])

        for sw in range(0, self.num_sweeps):

            pass_qc = 1
            if float(self.cap_lower_QC_input) > self.sweep_cap_array[sw] or float(
                    self.cap_upper_QC_input) < self.sweep_cap_array[sw]:
                pass_qc = 0

            if float(self.seal_QC_input) > self.sweep_seal_array[sw]:
                pass_qc = 0

            if float(self.SR_QC_input) > self.sweep_series_array[sw]:
                pass_qc = 0

            self.sweep_pass_qc_array = np.append(self.sweep_pass_qc_array, pass_qc)




def main():
    # for taskbar icon consistency
    #tracemalloc.start()
    #input_folder = os.path.join('C:\\', 'Users', 'j.farr', 'Documents', 'hERG_ssDeact_3s_AN_11.45.32')
    #input_folder = os.path.join('/mnt','syncropatch','Clinical_variant_Brett', '01092022_AN', 'hERG_ssDeact_3s_AN_11.45.32')

    #input_folder = os.path.join('/datadrive', 'syncropatch', 'Clinical_variant_Brett', '01092022_AN', 'hERG_ssDeact_3s_AN_11.45.32')
    #input_folder = os.path.join('/mnt', 'syncropatch', 'Clinical_variant_Brett', '01092022_AN', 'hERG_ssAct_1s_50us_AN_11.42.11')
    input_folder = os.path.join('/mnt', 'syncropatch', 'Clinical_variant_Brett', '01092022_AN', 'hERG_Inact_Onset_AN_11.51.10')



    #c = ControlWidget('ssDeact')
    #c = ControlWidget('ssAct')
    c = ControlWidget('Onset')
    p = PlateWidget(input_folder)

    tic = time.time()
    #high_throughput_ssDeact(os.path.join('/datadrive','syncropatch','Clinical_variant_Brett',), '01092022_AN', p.well_widgets, c, p.json_data.row_count, p.json_data.column_count, 'ssDeact Fit')
    #high_throughput_ssAct(os.path.join('/mnt', 'syncropatch', 'Clinical_variant_Brett', ), '01092022_AN', p.well_widgets, c, p.json_data.row_count, p.json_data.column_count, 'ssAct')
    high_throughput_onset_inact(os.path.join('/mnt', 'syncropatch', 'Clinical_variant_Brett', ), '01092022_AN', p.well_widgets, c, p.json_data.row_count, p.json_data.column_count, 'Onset')

    #print(tracemalloc.get_traced_memory())
    #tracemalloc.stop()
    print(time.time()-tic)




if __name__ == "__main__":
    main()

