# -*- coding: utf-8 -*-

"""
Test the implementatio of circumsolar shading, for front diffuse shading
calculations
"""

from pvfactors.pvcore import calculate_circumsolar_shading
from pvfactors.pvarray import Array
from pvfactors.tools import calculate_radiosities_serially_perez
import pandas as pd
import os
import numpy as np

TEST_DIR = os.path.dirname(__file__)
TEST_DATA = os.path.join(TEST_DIR, 'test_files')
idx_slice = pd.IndexSlice


def test_calculate_circumsolar_shading():
    """
    Test that the disk shading function stays consistent
    """
    # Test for one value of 20% of the diameter being covered
    percentage_distance_covered = 20.
    percent_shading = calculate_circumsolar_shading(
        percentage_distance_covered, model='uniform_disk')

    # Compare to expected
    expected_disk_shading_perc = 14.2378489933
    atol = 0
    rtol = 1e-8
    assert np.isclose(expected_disk_shading_perc, percent_shading, atol=atol,
                      rtol=rtol)


def test_serial_circumsolar_shading_calculation():
    """
    Calculate and save results from front surface circumsolar shading on
    pvrows. Test that it functions with the given data.
    """

    # Choose a PV array configuration and pass the arguments necessary for
    # the calculation to be triggered:
    # eg 'calculate_front_circ_horizon_shading'
    arguments = {
        'array_azimuth': 90.0,
        'array_tilt': 20.0,
        'cut': [(1, 5, 'front')],
        'gcr': 0.3,
        'n_pvrows': 2,
        'pvrow_height': 1.5,
        'pvrow_width': 1.,
        'rho_ground': 0.2,
        'rho_pvrow_back': 0.03,
        'rho_pvrow_front': 0.01,
        'solar_azimuth': 90.0,
        'solar_zenith': 30.0,
        'circumsolar_angle': 50.,
        'horizon_band_angle': 6.5,
        'calculate_front_circ_horizon_shading': True,
        'circumsolar_model': 'gaussian'
    }
    save = (1, 'front')
    # Load inputs for the serial calculation
    test_file = os.path.join(
        TEST_DATA, 'file_test_serial_circumsolar_shading_calculation.csv')
    df_inputs = pd.read_csv(test_file, index_col=0)
    df_inputs.index = pd.DatetimeIndex(df_inputs.index)

    # Create shapely PV array
    array = Array(**arguments)

    # Run the calculation for functional testing
    df_outputs, df_bifacial, df_inputs_perez, df_outputs_segments = (
        calculate_radiosities_serially_perez((arguments, df_inputs, save))
    )
