import numpy as np
import math
import scipy.io as sio


def scaleAwayParameters(unscaled_params, datapoints):
    '''
    :param unscaled_params:
    :param datapoints:
    :return:
    '''
    assert type(unscaled_params) is np.ndarray
    assert unscaled_params.ndim == 2
    assert unscaled_params.shape[1] == 3
    quad_ids = np.unique(unscaled_params[:, 0])

    scaledParams = unscaled_params[
                   (unscaled_params[:, 2] >= 0) * (unscaled_params[:, 1] >= 0) * (unscaled_params[:, 1] <= 1) * (
                       unscaled_params[:, 2] <= 1), :]
    throwndata = datapoints[(unscaled_params[:, 2] >= 0) * (unscaled_params[:, 1] >= 0) * (
        unscaled_params[:, 1] <= 1) * (unscaled_params[:, 2] <= 1), :]

    for i in range(len(quad_ids)):
        if not (scaledParams[:,0] == quad_ids[i]).any():
            print "++++++++++++++++++++coarse quad without fine verts detected+++++++++++++++++++++++++++++"
            continue
        print "quad %d of %d" % (i,len(quad_ids))
        umax = np.max(scaledParams[(scaledParams[:, 0] == quad_ids[i]), 1])
        umin = np.min(scaledParams[(scaledParams[:, 0] == quad_ids[i]), 1])
        vmax = np.max(scaledParams[(scaledParams[:, 0] == quad_ids[i]), 2])
        vmin = np.min(scaledParams[(scaledParams[:, 0] == quad_ids[i]), 2])

        uscale = umax - umin
        vscale = vmax - vmin

        if (uscale):
            scaledParams[(scaledParams[:, 0] == quad_ids[i]), 1] = (scaledParams[(
                                                                                     scaledParams[:, 0] == quad_ids[
                                                                                         i]), 1] - umin) / uscale

        if (vscale):
            scaledParams[(scaledParams[:, 0] == quad_ids[i]), 2] = (scaledParams[(
                                                                                     scaledParams[:, 0] == quad_ids[
                                                                                         i]), 2] - vmin) / vscale

    return scaledParams, throwndata


