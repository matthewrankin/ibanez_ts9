#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023 The ibanez_ts9 developers. All rights reserved.
# Project site: https://github.com/matthewrankin/ibanez_ts9
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
'''
create_plot.py

Reads the SDF file and plots the data.
'''

# Standard module imports
import sys

# Numerical/analysis related imports
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Third-party imports
import sdfascii


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', action='store',
                        help='Input filename excluding extension')
    parser.add_argument('outputfile', action='store',
                        help='Output plot filename')
    args = parser.parse_args()

    sdf_hdr, sdf_data = sdfascii.read_sdf_file(args.inputfile)

    data_hdr = sdf_hdr['data_hdr'][0]
    x0 = data_hdr['abscissa_first_x']
    abscissa_delta_x = data_hdr['abscissa_delta_x']
    num_points = data_hdr['num_points']

    # Create the x-data.
    if data_hdr['x_resolution_type'] == 'Linear':
        x_data = np.fromfunction(
            lambda i: x0 + abscissa_delta_x * i, (num_points,))
    elif data_hdr['x_resolution_type'] == 'Logarithmic':
        x_data = np.fromfunction(
            lambda i: x0 * abscissa_delta_x ** i, (num_points,))
    else:
        sys.exit('Bad x_resolution_type')
    # If this is an FFT measurement, then the x-data is only valid (i.e., alias
    # protected) from the start_freq_index to the stop_freq_index.
    if sdf_hdr['meas_hdr']['meas_type'] == 'FFT measurement':
        start_freq_index = sdf_hdr['meas_hdr']['start_freq_index']
        stop_freq_index = sdf_hdr['meas_hdr']['stop_freq_index']
        x_data = x_data[start_freq_index:stop_freq_index+1]

    # Convert from Hz to kHz for the plot.
    x_data = x_data / 1000

    # Set the font size to small for everything
    font = {'size': 10}
    matplotlib.rc('font', **font)

    # Create the plot
    fig = plt.figure()
    axes = fig.add_subplot(111)

    # Convert the y-data to dB.
    if sdf_hdr['meas_hdr']['meas_type'] != 'FFT measurement':
        y_data = 20 * np.log10(np.abs(sdf_data))
        axes.semilogx(x_data, y_data)
    else:
        y_data = sdf_data * 1000  # Convert to mVrms
        axes.semilogy(x_data, y_data)

    # Plot the data.

    # Display the minor values
    axes.tick_params(axis='both', which='both', labelsize='x-small')

    # Display the major and minor ticks as non-exponents.
    axes.yaxis.set_major_formatter(plt.FormatStrFormatter('%g'))
    axes.xaxis.set_major_formatter(plt.FormatStrFormatter('%g'))
    axes.xaxis.set_minor_formatter(plt.FormatStrFormatter('%g'))

    # Display the minor values
    axes.tick_params(axis='both', which='both', labelsize='x-small')

    # Show gridlines
    axes.grid(visible=True, which='major', color='gray', linestyle='-')
    axes.grid(visible=True, which='minor', color='gray', linestyle='--')

    axes.set_axisbelow(True)
    axes.set_xlabel('Frequency (kHz)')

    # Set the y axis to go between -30dB and 20dB.
    if sdf_hdr['meas_hdr']['meas_type'] != 'FFT measurement':
        axes.yaxis.set_minor_formatter(plt.FormatStrFormatter('%g'))
        axes.set_ylim(ymin=-30, ymax=20)
        axes.set_xlim(xmin=0.02, xmax=20)
        axes.set_ylabel('Amplitude (dB)')
        # Override default x-axis ticks.
        plot_ticks = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09,
                      0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4,
                      5, 6, 7, 8, 9, 10, 20]
        plot_labels = ['', '', '0.03', '', '', '', '0.07', '', '', '0.1', '',
                       '0.3', '', '0.5', '', '0.7', '', '', '1', '2', '3', '4',
                       '5', '6', '', '8', '', '10', '20']
        plt.xticks(plot_ticks, plot_labels, minor=True)
    else:
        axes.set_ylabel('Amplitude (mVrms)')
        axes.set_xlim(xmin=0.00, xmax=12.8)
        axes.set_ylim(ymin=0.00001, ymax=100)

    # Save the plot to a PDF
    plt.savefig(args.outputfile)

    # Clear all the Matplotlib plots
    plt.close('all')
