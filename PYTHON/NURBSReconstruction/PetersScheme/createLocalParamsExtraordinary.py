# ported from MATLAB/Sandbox/GSpline/createLocalParamsExtraordinary.m
import numpy as np


def createLocalParamsExtraordinary(global_quad_params):
    assert type(global_quad_params) is np.ndarray

    nearWhich = -1  # default error!
    whichPatch = np.floor(global_quad_params * 4)
    whichPatch[whichPatch > 3.5] = 3  # cap at 4 - can get 5 otherwise
    shifted_scaled_coords = global_quad_params * 4 - whichPatch
    shifted_scaled_coords[global_quad_params >= 1] = 1  # so param 1 doesn't give 0)

    localParams = shifted_scaled_coords
    if global_quad_params[0] <= 0.25:
        if global_quad_params[1] <= 0.25:
            # bottom-left. Need to rotate by 180 degrees, but u stays u-dir and v
            # stays v-dir
            coordinatesReversed = 1 - shifted_scaled_coords
            localParams = [coordinatesReversed[0], coordinatesReversed[1]]
            nearWhich = 0
        elif global_quad_params[1] >= 0.75:
            # upper-left corner. Local u is global v, and local v is global 1-u.
            localParams = [shifted_scaled_coords[1], 1 - shifted_scaled_coords[0]]
            nearWhich = 3

    elif global_quad_params[0] >= 0.75:
        if global_quad_params[1] <= 0.25:
            # bottom-right. Local u is global 1-v, local v is u.
            localParams = [1 - shifted_scaled_coords[1], shifted_scaled_coords[0]]
            nearWhich = 1
        elif global_quad_params[1] >= 0.75:
            # upper-right. NO SWITCHIES!!!!
            localParams = shifted_scaled_coords
            nearWhich = 2

    else:
        while (whichPatch == 0).all() or (whichPatch == 3).all():  # both are 1/4! we're in a corner! error
            raise Exception(
                'thingy thought we were in a corner when we weren"t, so shifting. in createLocalParamsExtraordinary.m')

    return localParams, nearWhich, whichPatch
