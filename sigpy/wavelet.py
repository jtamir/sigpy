import numpy as np
import pywt
from sigpy import util


def get_wavelet_shape(shape, wave_name, axes, level):
    zshape = [((i + 1) // 2) * 2 for i in shape]

    tmp = pywt.wavedecn(
        np.zeros(zshape), wave_name, mode='zero', axes=axes, level=level)
    tmp, coeff_slices = pywt.coeffs_to_array(tmp, axes=axes)
    oshape = tmp.shape

    return oshape, coeff_slices


def fwt(input, wave_name='db4', axes=None, level=None):
    """Forward wavelet transform.

    Args:
        input (array): Input array.
        axes (None or tuple of int): Axes to perform wavelet transform.
        wave_name (str): Wavelet name.
        level (None or int): Number of wavelet levels.
    """
    device = util.get_device(input)
    input = util.move(input)

    zshape = [((i + 1) // 2) * 2 for i in input.shape]
    zinput = util.resize(input, zshape)

    coeffs = pywt.wavedecn(zinput, wave_name, mode='zero', axes=axes, level=level)
    output, _ = pywt.coeffs_to_array(coeffs, axes=axes)

    output = util.move(output, device)
    return output


def iwt(input, oshape, coeff_slices, wave_name='db4', axes=None, level=None):
    """Inverse wavelet transform.

    Args:
        input (array): Input array.
        oshape (tuple of ints): Output shape.
        coeff_slices (list of slice): Slices to split coefficients.
        axes (None or tuple of int): Axes to perform wavelet transform.
        wave_name (str): Wavelet name.
        level (None or int): Number of wavelet levels.
    """
    device = util.get_device(input)
    input = util.move(input)

    input = pywt.array_to_coeffs(input, coeff_slices, output_format='wavedecn')
    output = pywt.waverecn(input, wave_name, mode='zero', axes=axes)
    output = util.resize(output, oshape)

    output = util.move(output, device)
    return output
