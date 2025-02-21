'''
This script is used to import the ARTEMIS and OMNI data for lots of events in a *.csv file
To do this, you must have a file in the same directory as this folder with the following columns:
    - Date_Start (format yyyy-mm-dd or yyyy-mm-ddTHH:MM:SS)
    - Date_Stop (same format as above)
'''

import numpy as np
import datetime as dt
import pandas as pd
import pyspedas
from pytplot import get_data
from scipy.constants import physical_constants
import os

keys = ['BX_GSM', 'BY_GSM', 'BZ_GSM', 'VX', 'VY', 'VZ', 'N', 'T']

def get_artemis_gsm(start, stop):   # Function that gets the ARTEMIS data in GSM
    trange = [(start-pd.Timedelta(minutes=30)).strftime("%Y-%m-%d/%H:%M:%S"), (stop + pd.Timedelta(minutes=1)).strftime("%Y-%m-%d/%H:%M:%S")]  # Timeseries should be in the format [pd.Timestamp, pd.Timestamp]
    print(trange)
    artemis = {}    # Create a storage array for data
    for probe in ['b', 'c']:    # Iterate through ARTEMIS probes 1 and 2 (THEMIS B and C) to get data for both. Used for substituting later.
        artemis_fgm_import = pyspedas.themis.fgm(trange=trange, probe=probe, level='l2', time_clip=True, varnames=f'th{probe}_fgs_gsm') # Import the mag data

        fgm = pd.DataFrame({'Time': get_data(f'th{probe}_fgs_gsm')[0], 'BX_GSM': get_data(f'th{probe}_fgs_gsm')[1][:, 0], 'BY_GSM': get_data(f'th{probe}_fgs_gsm')[1][:, 1], 'BZ_GSM': get_data(f'th{probe}_fgs_gsm')[1][:, 2]}, columns=['Time', 'BX_GSM', 'BY_GSM', 'BZ_GSM'])
        fgm['Time'] = pd.to_datetime(fgm['Time'], unit='s') # Convert the time column to a DateTime, the unit is seconds.
        fgm = fgm.set_index('Time') # Make the time column the index, so that we can interpolate time steps
        fgm = fgm.resample('min').mean().interpolate(method='linear').ffill().bfill()   # Interpolate any gaps, and fill in any missing or NaN values at the start and end.
        fgm = fgm.reset_index() # Revert the time column index since we already interpolated

        artemis_esa_import = pyspedas.themis.esa(trange=trange, probe=probe, level='l2', time_clip=True, varnames=[f'th{probe}_peif_velocity_gsm', f'th{probe}_peif_density', f'th{probe}_peif_avgtemp'])

        esa = pd.DataFrame({'Time': get_data(f'th{probe}_peif_velocity_gsm')[0], 'VX': get_data(f'th{probe}_peif_velocity_gsm')[1][:, 0], 'VY': get_data(f'th{probe}_peif_velocity_gsm')[1][:, 1], 'VZ': get_data(f'th{probe}_peif_velocity_gsm')[1][:, 2], 'N': get_data(f'th{probe}_peif_density')[1], 'T': get_data(f'th{probe}_peif_avgtemp')[1]/physical_constants['Boltzmann constant in eV/K'][0]}, columns=['Time', 'VX', 'VY', 'VZ', 'N', 'T'])
        esa['Time'] = pd.to_datetime(esa['Time'], unit='s')
        esa = esa.set_index('Time')
        esa = esa.resample('min').mean().interpolate(method='linear').ffill().bfill()
        esa = esa.reset_index()

        artemis_stt_import = pyspedas.themis.state(trange=trange, probe=probe, time_clip=True, varnames=[f'th{probe}_pos_gsm', f'th{probe}_pos_sse'])

        stt = pd.DataFrame({'Time': get_data(f'th{probe}_pos_gsm')[0], 'XPOS': get_data(f'th{probe}_pos_gsm')[1][:, 0], 'XSSE': get_data(f'th{probe}_pos_sse')[1][:, 0]/1737.4, 'YSSE': get_data(f'th{probe}_pos_sse')[1][:, 1]/1737.4}, columns=['Time', 'XPOS', 'XSSE', 'YSSE'])
        stt['Time'] = pd.to_datetime(stt['Time'], unit='s')
        stt = stt.set_index('Time')
        stt = stt.resample('min').mean().interpolate(method='linear').ffill().bfill()
        stt = stt.reset_index()

        print(fgm['Time'][0])
        print(esa['Time'][0])
        print(stt['Time'][0])

        latest_start_time = max(fgm['Time'][0], esa['Time'][0], stt['Time'][0]) # Sometimes these don't all start at the same time due to cadence or missing data, so get the latest starting variable

        fgm = fgm[(fgm['Time'] >= latest_start_time) & (fgm['Time'] <= stop)]
        esa = esa[(esa['Time'] >= latest_start_time) & (esa['Time'] <= stop)]
        stt = stt[(stt['Time'] >= latest_start_time) & (stt['Time'] <= stop)]

        artemis[probe] = pd.merge(pd.merge(fgm, esa, on='Time', how='outer'), stt, on='Time', how='outer')
        artemis[probe] = artemis[probe].ffill().bfill()
        #artemis[probe] = artemis[probe][(artemis[probe]['Time'] >= start) & (artemis[probe]['Time'] <= stop)]

    for index, row in artemis['b'].iterrows():
        if row['XSSE'] <= 0 and -1 <= row['YSSE'] <= 1:
            if index in artemis['c'].index:  # Check if the index exists in artemis['c']
                for k in keys:
                    if k in artemis['b'].columns and k in artemis['c'].columns:
                        artemis['b'].at[index, k] = artemis['c'].at[index, k]

    start_omni = artemis['b']['Time'][0] + dt.timedelta(minutes=30)

    trange_omni = [start_omni.strftime("%Y-%m-%d/%H:%M:%S"), (stop+pd.Timedelta(minutes=1)).strftime(
        "%Y-%m-%d/%H:%M:%S")]  # Timeseries should be in the format [pd.Timestamp, pd.Timestamp]
    omni_import = pyspedas.omni.data(trange=trange_omni, datatype='1min', level='hro2', time_clip=True)
    omni = pd.DataFrame({'Time': get_data('IMF')[0], 'BX_GSM': get_data('BX_GSE')[1], 'BY_GSM': get_data('BY_GSM')[1],
                         'BZ_GSM': get_data('BZ_GSM')[1], 'VX': get_data('Vx')[1], 'VY': get_data('Vy')[1],
                         'VZ': get_data('Vz')[1], 'N': get_data('proton_density')[1], 'T': get_data('T')[1],
                         'XPOS': get_data('BSN_x')[1] * 6378.14},
                        columns=['Time', 'BX_GSM', 'BY_GSM', 'BZ_GSM', 'VX', 'VY', 'VZ',
                                 'N', 'T', 'XPOS']).replace(to_replace=[999.990, 9999.99, 99999.9, 9999999],
                                                            value=np.nan)

    omni['Time'] = pd.to_datetime(omni['Time'], unit='s')
    omni = omni.set_index('Time').ffill().bfill()
    omni.reset_index(inplace=True)
    omni = omni[(omni['Time'] >= start_omni) & (omni['Time'] <= stop)]

    return omni, artemis['b']

#-------------------------------------------------------------------------------------------------------------------
'''
events = pd.read_csv('test_dates.csv', delimiter=',', header=0)
events['Date_Start'] = pd.to_datetime(events['Start_Date'])
events['Date_Stop'] = pd.to_datetime(events['Stop_Date'])

for event in range(len(events['Date_Start'])):
    print(events['Date_Start'][event])
    omni_data, artemis_data = get_artemis_gsm(events['Date_Start'][event], events['Date_Stop'][event])

    if os.path.exists(f'outputs/artemis') and os.path.exists(f'outputs/omni'):
        artemis_data.to_csv(f'outputs/artemis/artemis_{events["Date_Start"][event].strftime("%Y-%m-%d_%H-%M")}.csv')
        omni_data.to_csv(f'outputs/omni/omni_{events["Date_Start"][event].strftime("%Y-%m-%d_%H-%M")}.csv')
    else:
        os.makedirs(f'outputs/artemis')
        os.makedirs(f'outputs/omni')
        artemis_data.to_csv(f'outputs/artemis/artemis_{events["Date_Start"][event].strftime("%Y-%m-%d_%H-%M")}.csv')
        omni_data.to_csv(f'outputs/omni/omni_{events["Date_Start"][event].strftime("%Y-%m-%d_%H-%M")}.csv')
'''