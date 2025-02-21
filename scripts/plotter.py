import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime as dt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


keys = ['BX_GSM', 'BY_GSM', 'BZ_GSM', 'VX', 'VY', 'VZ', 'N', 'T']
names = [r'$B_x$ GSM (nT)', r'$B_y$ GSM (nT)', r'$B_z$ GSM (nT)', r'$V_x$ GSM (km/s)', r'$V_y$ GSM (km/s)', r'$V_z$ GSM (km/s)', r'Proton Density (n/cc)', 'Temperature (K)']

artemis_file = pd.read_csv('outputs/artemis/artemis_2018-02-15_00-00.csv', delimiter=',', header=0)
omni_file = pd.read_csv('outputs/omni/omni_2018-02-15_00-00.csv', delimiter=',', header=0)

artemis_file['Time'] = pd.to_datetime(artemis_file['Time'])
omni_file['Time'] = pd.to_datetime(omni_file['Time'])

fig, ax = plt.subplots(len(keys), 1, figsize=(12, 2*len(keys)), sharex=True)
for i, (k, n) in enumerate(zip(keys, names)):
    ax[i].plot(artemis_file['Time'], artemis_file[k], label='Artemis')
    ax[i].plot(omni_file['Time'], omni_file[k], label='Omni')
    ax[i].set_xlim([dt.datetime(2018, 2, 16, 6, 54), dt.datetime(2018, 2, 16, 7, 54)])
    ax[i].set_ylabel(n)

ax[-1].xaxis.set_major_locator(mdates.HourLocator(interval=3))
ax[-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax[-1].xaxis.set_minor_locator(mdates.HourLocator(interval=1))
ax[-1].set_xlabel('Time UTC')

plt.suptitle('Event on 2018-02-17 for 1 hour')
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig('overlap_plots/85Event-1hr', dpi=300)
plt.show()


fig, ax = plt.subplots(len(keys), 1, figsize=(12, 2*len(keys)), sharex=True)
for i, (k, n) in enumerate(zip(keys, names)):
    ax[i].plot(artemis_file['Time'], artemis_file[k], label='Artemis')
    ax[i].plot(omni_file['Time'], omni_file[k], label='Omni')
    ax[i].set_xlim([dt.datetime(2018, 2, 16, 0, 0), dt.datetime(2018, 2, 16, 23, 59)])
    ax[i].set_ylabel(n)

ax[-1].xaxis.set_major_locator(mdates.HourLocator(interval=3))
ax[-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax[-1].xaxis.set_minor_locator(mdates.HourLocator(interval=1))
ax[-1].set_xlabel('Time UTC')

plt.suptitle('Event on 2018-02-17')
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig('overlap_plots/85Event', dpi=300)
plt.show()












artemis_file = pd.read_csv('outputs/artemis/artemis_2022-04-30_00-00.csv', delimiter=',', header=0)
omni_file = pd.read_csv('outputs/omni/omni_2022-04-30_00-00.csv', delimiter=',', header=0)

artemis_file['Time'] = pd.to_datetime(artemis_file['Time'])
omni_file['Time'] = pd.to_datetime(omni_file['Time'])

fig, ax = plt.subplots(len(keys), 1, figsize=(12, 2*len(keys)), sharex=True)
for i, (k, n) in enumerate(zip(keys, names)):
    ax[i].plot(artemis_file['Time'], artemis_file[k], label='Artemis')
    ax[i].plot(omni_file['Time'], omni_file[k], label='Omni')
    ax[i].set_xlim([dt.datetime(2022, 4, 30, 2, 57), dt.datetime(2022, 4, 30, 3, 57)])
    ax[i].set_ylabel(n)

ax[-1].xaxis.set_major_locator(mdates.HourLocator(interval=3))
ax[-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax[-1].xaxis.set_minor_locator(mdates.HourLocator(interval=1))
ax[-1].set_xlabel('Time UTC')

plt.suptitle('Event on 2022-04-30 for 1 hour')
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig('overlap_plots/6Event-1hr', dpi=300)
plt.show()


fig, ax = plt.subplots(len(keys), 1, figsize=(12, 2*len(keys)), sharex=True)
for i, (k, n) in enumerate(zip(keys, names)):
    ax[i].plot(artemis_file['Time'], artemis_file[k], label='Artemis')
    ax[i].plot(omni_file['Time'], omni_file[k], label='Omni')
    ax[i].set_xlim([dt.datetime(2022, 4, 30, 0, 0), dt.datetime(2022, 4, 30, 23, 59)])
    ax[i].set_ylabel(n)

ax[-1].xaxis.set_major_locator(mdates.HourLocator(interval=3))
ax[-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax[-1].xaxis.set_minor_locator(mdates.HourLocator(interval=1))
ax[-1].set_xlabel('Time UTC')

plt.suptitle('Event on 2022-04-30')
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig('overlap_plots/6Event', dpi=300)
plt.show()