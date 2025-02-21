import os
import pandas as pd
import numpy as np
from doCorrelate import correlate

def process_files(file_pair, mode, base_output_dir):
    artemis_file = pd.read_csv(file_pair[0], delimiter=',', header=0)
    omni_file = pd.read_csv(file_pair[1], delimiter=',', header=0)
    artemis_file = artemis_file.rename(columns={'XPOS': 'Xpos'})
    artemis_file['Time'] = pd.to_datetime(artemis_file['Time'], format='%Y-%m-%d %H:%M:%S')
    omni_file['Time'] = pd.to_datetime(omni_file['Time'], format='%Y-%m-%d %H:%M:%S')

    if mode == "Bx":
        output_dir = os.path.join(base_output_dir, 'Bx')
        os.makedirs(output_dir, exist_ok=True)
        print(f"Processing Bx: {artemis_file['Time'][0]} vs {omni_file['Time'][0]}")
        correlate((artemis_file, omni_file), output_dir, 'BX_GSM')
    elif mode == "V":
        output_dir = os.path.join(base_output_dir, 'V')
        os.makedirs(output_dir, exist_ok=True)
        artemis_file['V'] = np.sqrt(artemis_file['VX']**2 + artemis_file['VY']**2 + artemis_file['VZ']**2)
        omni_file['V'] = np.sqrt(omni_file['VX']**2 + omni_file['VY']**2 + omni_file['VZ']**2)
        print(f"Processing V (quadrature): {artemis_file['Time'][0]} vs {omni_file['Time'][0]}")
        correlate((artemis_file, omni_file), output_dir, 'V')