#import constants
import numpy as np
import json

'''
path = "/Users/s.arjunan/wrk/ttra_data/drug_dose"
input_path = f"{path}/raw_syncropatch"
output_path = f"{path}/output"
plate = "n2_14 cpds"
suffix = "hERG_Pharm_40_Nina_16.25.57"
well_rows = 16
well_cols = 24
char_offset = 65
int16_size = 2 # in bytes
'''

#def initiate_extraction(path, input_path, output_path, plate, suffix, well_rows, well_cols, char_offset, int16_size):



class Json_Data():
    def __init__(self, path, well_rows, well_cols, char_offset):
        meta = json.load(open(path, 'r'))
        self.row_count = meta['TraceHeader']['Chiplayout']['WP_nRows']
        assert(self.row_count == well_rows)
        self.column_count = meta['TraceHeader']['MeasurementLayout'][
            'nCols']
        assert(self.column_count == well_cols)
        self.total_sweeps = meta['TraceHeader']['MeasurementLayout'][
            'NofSweeps']
        self.file_count = meta['TraceHeader']['FileInformation']['NofFiles']
        self.dat_files = meta['TraceHeader']['FileInformation']['FileList']
        assert(len(self.dat_files) == self.file_count)
        #self.sweeps_times = meta['TraceHeader']['TimeScaling']['SweepTime']
        #self.sweeps_times = meta['TraceHeader']['TimeScalingIV']['SweepTime']
        self.sweeps_times = meta['TraceHeader']['TimeScalingIV']['TR_Time']
        #assert(np.asarray(self.sweeps_times).shape == (self.column_count, self.total_sweeps))
        # True if a sweep is valid
        # False if a sweep should be disregarded
        self.valid_sweeps = np.asarray(meta['QCData']['DisregardedSweeps']
            ).astype(bool)
        assert(len(self.valid_sweeps) == self.total_sweeps)
        self.tiled_disregarded_sweeps = np.tile(~self.valid_sweeps,
            (self.row_count * self.column_count, 1))

        self.cursor_bounds = meta['ExperimentConditions']['OAFunctions']
        self.cursor_region = self.cursor_bounds['CursorName' == 'tail']
        self.cursor_start = float(self.cursor_region['TimeStart_ms'])
        self.cursor_start = self.cursor_start - 0.1 * self.cursor_start
        self.cursor_end = float(self.cursor_region['TimeEnd_ms'])
        self.cursor_end = self.cursor_end + 0.1 * self.cursor_end

        self.sample_count = meta['TraceHeader']['MeasurementLayout'][
            'NofSamples']
        self.well_names = [chr(row + char_offset) +
            "{:02}".format(column + 1)
            for column in range(self.column_count)
            for row in range(self.row_count)]
        self.sweeps_per_file = meta['TraceHeader']['FileInformation'][
          'SweepsPerFile']
        self.data_count = meta['TraceHeader']['MeasurementLayout']['Leakdata']
        assert(self.data_count == 2)
        self.column_scales = meta['TraceHeader']['TimeScalingIV']['I2DScale']
        assert(len(self.column_scales) == self.column_count)
        self.sweep_compound_indices = np.array(meta['CompoundAddition'][
            'Sweep2CompIndex'])
        self.compound_states = meta['CompoundAddition']['CompStateProt']
        self.compound_types = np.array(meta['CompoundAddition'][
            'RequiredDef']['CompType_Enum']['AllowedText'])
        self.compound_table = meta['CompTable']['TableData']

        self.seal_resistances = np.asarray(
          [[self.nanify(val) for column in sweep for val in column] for sweep in
            meta['QCData']['RSeal']]).T
        self.seal_resistances[self.tiled_disregarded_sweeps] = np.nan
        assert(self.seal_resistances.shape == (self.row_count *
            self.column_count, self.total_sweeps))

        self.capacitances = np.asarray(
          [[self.nanify(val) for column in sweep for val in column] for sweep in
            meta['QCData']['Capacitance']]).T
        self.capacitances[self.tiled_disregarded_sweeps] = np.nan
        assert(self.capacitances.shape == (self.row_count *
            self.column_count, self.total_sweeps))

        self.series_resistances = np.asarray(
          [[self.nanify(val) for column in sweep for val in column] for sweep in
            meta['QCData']['Rseries']]).T
        self.series_resistances[self.tiled_disregarded_sweeps] = np.nan
        assert (self.series_resistances.shape == (self.row_count *
            self.column_count, self.total_sweeps))
        self.voltages = meta['TraceHeader']['TimeScalingIV']['Stimulus']

        self.variants = np.array(meta['CellTable']['TableData'])
        self.variants = self.variants[:, 0]


        self.variant_layout = np.array(meta['CellState']['CellLayout'])

        self.voltage_protocol = np.array(meta['ExperimentConditions']['VoltageProtocol'])
        print(self.voltage_protocol)
        #assert(len(self.voltages) == self.sample_count)

    def nanify(self, val):
        return val if val is not None else np.nan

    def get_sweep_compound_name(self, sweep, row, col):
        sweep_compound_index = self.sweep_compound_indices[sweep]
        compound_layout_index = self.compound_states[sweep_compound_index][
            'CompLayout'][row][col]
        if (compound_layout_index < 0):
            compound_type_index = self.compound_states[sweep_compound_index][
                'CompType_Enum']
            return self.compound_types[compound_type_index]
        else:
            return self.compound_table[compound_layout_index][0]

    def get_sweep_compound_concentration(self, sweep, row, col):
        sweep_compound_index = self.sweep_compound_indices[sweep]
        compound_concentration = self.compound_states[sweep_compound_index][
            'Concentration'][row][col]
        return compound_concentration

    def get_well_seal_resistances(self, well):
        return self.seal_resistances[well]

    def get_well_capacitances(self, well):
        return self.capacitances[well]

    def get_well_series_resistances(self, well):
        return self.series_resistances[well]

    def get_sweep_times(self, col):
        #return self.sweeps_times[col]
        return self.sweeps_times

    def get_voltages(self):
        return self.voltages

class File_Section():
    def __init__(self, path, offset, length):
        self.__path = path
        self.__offset = offset
        self.__length = length
        #print("path:", path)

    def get(self):
        try:
            with open(self.__path, "rb") as file:
                file.seek(self.__offset)
                return file.read(self.__length)
        except FileNotFoundError:
            print("file not found")
            return None
        print("pass")
        pass

class Well():
    def __init__(self, json_data, data_path, well_name, int16_size):
        self.json_data = json_data
        self.index = json_data.well_names.index(well_name)
        # self.row: 0 to 15; A?? to P??; when self.row == 0, A01 to A24
        self.row = self.index%json_data.row_count
        # self.col: 0 to 23; ?01 to ?24; when self.col == 0, A01 to P01
        self.col = self.index//json_data.row_count
        self.data_path = data_path
        self.int16_size = int16_size

    def get_sweep_currents(self, sweep):
        # sweep is sweep number (0 to json_data.total_sweeps-1)
        if (self.json_data.valid_sweeps[sweep]):
            path = f"{self.data_path}/" + self.json_data.dat_files[
                sweep // self.json_data.sweeps_per_file]
            offset = (((((sweep % self.json_data.sweeps_per_file) *
                self.json_data.column_count + self.col) *
                self.json_data.row_count + self.row) *
                self.int16_size + self.json_data.data_count - 1) *
                self.json_data.sample_count * self.int16_size)
            length = self.json_data.sample_count * self.int16_size
            # read *.dat binary file with File_Section
            file_section = File_Section(path, offset, length)
            return list(map(lambda n:
                n * self.json_data.column_scales[self.col],
                np.frombuffer(bytearray(file_section.get()), dtype=np.int16)))
        else:
            return list([np.nan]*self.json_data.sample_count)

    def get_sweep_compound_name(self, sweep):
        return self.json_data.get_sweep_compound_name(sweep, self.row, self.col)

    def get_sweep_compound_concentration(self, sweep):
        return self.json_data.get_sweep_compound_concentration(sweep, self.row,
            self.col)

    def get_seal_resistances(self):
        return self.json_data.get_well_seal_resistances(self.index)

    def get_capacitances(self):
        return self.json_data.get_well_capacitances(self.index)

    def get_series_resistances(self):
        return self.json_data.get_well_series_resistances(self.index)

    def get_sweep_times(self):
        return self.json_data.get_sweep_times(self.col)

'''
data_path = f"{input_path}/{plate}/{suffix}"
json_data = Json_Data(f"{data_path}/{suffix}.json")
well = Well(json_data, data_path, "A01")
print(well.get_sweep_currents(2))
print(well.get_sweep_compound_name(45))
print(well.get_sweep_compound_concentration(45))
print(well.get_seal_resistances())
print(well.get_capacitances())
print(well.get_series_resistances())
print(well.get_sweep_times())
print(json_data.get_voltages())
'''

