import numpy as np
from scipy.stats import pearsonr, linregress
import pandas as pd
import os

def prediction_efficiency_artemis(omni, artemis):  # This function just finds prediction efficiency
    return 1 - (np.sum((omni-artemis)**2)/np.sum((artemis - np.mean(artemis))**2))

def prediction_efficiency_omni(omni, artemis):  # This function just finds prediction efficiency
    return 1 - (np.sum((artemis-omni)**2)/np.sum((omni - np.mean(omni))**2))

def get_pe(file_pair, shift_vals, output_path):
    data_rows = []  # Data storage array
    a_dat, o_dat = file_pair  # The pair of files contain Artemis and Omni data

    print('Artemis: '+ a_dat['Time'][0].strftime('%Y-%m-%d'))
    print('Omni: ' + o_dat['Time'][0].strftime('%Y-%m-%d'))
    print('Shift: '+shift_vals['Start'][0])

    num_windows = len(o_dat) - 60  # The number of correlation windows is the number of unique 60 minute chunks

    print(f'Computing {num_windows} windows...')  # Message to let you know what's going on

    for n in range(num_windows):  # Loop over each window of 60 minutes
        a_start = a_dat.loc[a_dat['Time'] == o_dat['Time'].iloc[n]].index[0]  # The starting value in Artemis is the one that matches the first OMNI point
        a_stop = a_dat.loc[a_dat['Time'] == o_dat['Time'].iloc[n + 59]].index[0]  # The stopping value in Artemis is 60 minutes after the start

        shift = shift_vals['Pearson'][n]
        o_slice = o_dat['BZ_GSM'][n:n + 60]  # Make OMNI slice
        a_slice = a_dat['BZ_GSM'][a_start - shift:a_stop - shift]  # Step the Artemis slice to the right amount

        pe = prediction_efficiency(o_slice, a_slice)

        data_rows.append(np.concatenate(([o_dat['Time'][n]], [o_dat['Time'][n + 60]], pe), axis=None))

    values = pd.DataFrame(data_rows, columns=['Start', 'Stop','PE'])


    if os.path.exists(os.path.join(output_path, '{}/metrics'.format('PEs'))):
        values.to_csv(os.path.join(output_path, '{}/metrics/{}.csv'.format('PEs', a_dat['Time'][0].strftime('%Y-%m-%d'))))

    else:
        os.makedirs(os.path.join(output_path, '{}/metrics'.format('PEs')))
        values.to_csv(os.path.join(output_path, '{}/metrics/{}.csv'.format('PEs', a_dat['Time'][0].strftime('%Y-%m-%d'))))
