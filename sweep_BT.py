############################################################################
### 2024-05-16 - Sweep Algorithm & Lock-In/Magnet Control - Needs Testing
############################################################################

'''
In this script, we set up a loop to collect voltage
measurements as we sweep the temperature and B-field 
on our sample. 
This codes assumes that we have a function 
set_temperature(Device, Value), which calls an instrument 
named 'Device' and sets the temperature of the experiment to 
'Value'. Assumes the time for temperature to stabilise is 
't_temp'.
'''


### IMPORT RELEVANT PACKAGES

import numpy as np 
import time
from time import sleep
import qcodes as qc
from qcodes.dataset import do0d, load_or_create_experiment
from qcodes.instrument import Instrument
from qcodes.instrument_drivers.stanford_research import SR830
from qcodes.validators import Numbers
from qcodes_contrib_drivers.drivers.Lakeshore.Model_625 import Lakeshore625


### SET-UP MAGNET 

# MAGNET PARAMS 
magnet_GPI = 20 
magnet_coil_const = ... # manufacturer-determined
magnet_max_curr = ... # manufacturer-determined
magnet_field_ramp_rate = ... # manufacturer-determined
magnet_curr_ramp_rate = ... # manufacturer-determined

# CONNECT TO MAGNET
magnet = Lakeshore625(name = 'magnet', address = 'GPIB0::' + str(magnet_GPI) + '::INSTR', coil_constant = magnet_coil_const, field_ramp_rate = magnet_field_ramp_rate)
magnet.current_ramp_rate(magnet_curr_ramp_rate)
magnet.print_readable_snapshot(update = True) # check magnet status


### SET-UP LOCK-IN

# LOCK-IN PARAMS 
lockin_GPI = 7 
lockin_sensivity = ... #
lockin_ref_freq = 100 # stay at ~100 Hz, based on discussion with sandesh
lockin_ref_V = ... # ! what determines this? (think it does not matter, as long as we don't heat things up)
lockin_ref_phi = 0
lockin_tc = 0.03 # lock-in time constant, must be larger than 1 / (lock-in ref. frequency)
lockin_calib_time = 3 * lockin_tc # calibration time is ~3 * (time constant)

# CONNECT TO LOCK-IN
lockin = SR830('lockin', 'GPIB0::' + str(lockin_GPI) + '::INSTR') 
lockin.print_readable_snapshot() # check lock-in status

# SET LOCK-IN PARAMS
lockin.time_constant(lockin_tc)
lockin.sensitivity(lockin_sensitivity)
lockin.reference_source('internal')
lockin.set('amplitude', lockin_ref_V) # set reference amp
lockin.set('frequency', lockin_ref_freq)
lockin.set('phase', lockin_ref_phi) 
lockin.print_readable_snapshot() # check updated params


### DO SWEEP 

# SET-UP SWEEP
temp_min, temp_max, temp_points = 1, 10, 100 # ! examples, need to determine  
B_min, B_max, B_points = 1e-5, 5, 200 
temps = np.linspace(temp_min, temp_max, temp_points)
Bs = np.linspace(B_min, B_max, B_points)
i = 0

# RUN SWEEP 
for T in temps: 
    set_temperature(..., float(T)) # !
    time.sleep(t_temp) # ! wait for temperature to calibrate 
    dat = []
    for B in Bs:
        # Set up field measurement
        B_curr = magnet.field()
        t_field = np.abs(B - B_curr) / magnet_field_ramp_rate
        magnet.field(B) # set field 
        # Wait for instruments to callibrate 
        time.sleep(t_field) 
        time.sleep(lockin_calib_time)
        # Extract data points 
        V, B, T, magnet_current = lockin.R(), magnet.field(), ..., magnet.field() / magnet_coil_const # ! add temp
        print('V, B, T, magnet current')
        print(V, B, T, magnet_current) # print current status 
        dat.append(np.array([V, B, T, magnet_current]))
    dat = np.array(dat)
    np.save('sweep_' + str(i) + '.npy', dat)
    i += 1
