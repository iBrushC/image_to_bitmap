# All code written by Andrew Michael Combs

import numpy as np

# Matrix for error-diffusion dithering
class DiffuseMatrix(object):
    def __init__(self, r1 : np.ndarray, r2 : np.ndarray, r3 : np.ndarray, multiplier : float):
        self.r1 = (r1 * multiplier)
        self.r2 = (r2 * multiplier)
        self.r3 = (r3 * multiplier)

# Matrix for error-diffusion dithering
class LinearMatrix(object):
    def __init__(self, mat : np.ndarray, multiplier : float):
        self.matrix = mat * multiplier * 255

# Nearest Palette
def round_to_palette():
    return

def clip(x, minimum, maximum):
    return max(min(x, maximum), minimum)

# Linear dithering
def linear_dither(image : np.ndarray, matrix : LinearMatrix) -> np.ndarray:
    _img = image.copy()
    dim = image.shape

    xfact = int(dim[1]/matrix.matrix.shape[1])
    yfact = int(dim[0]/matrix.matrix.shape[0])
    pattern = np.tile(matrix.matrix, (yfact+1, xfact+1))
    pattern = pattern[0:dim[0], 0:dim[1]]

    try:
        chanels = dim[2]
        out = _img
        for i in range(chanels):
            out[:, :, i] = np.where(out[:, :, i] > pattern, 255, 0)
    except IndexError:
        out = np.where(image > pattern, 255, 0)
    
    return out

# Error diffusion / matrix dithering
def diffuse_dither(image : np.ndarray, matrix : DiffuseMatrix) -> np.ndarray:
    _img = image.copy().astype(np.float32)
    out = image.copy()
    dim = image.shape

    dt = _img.dtype

    r1, r1s, r1o = matrix.r1, len(matrix.r1), int(len(matrix.r2)/2)
    r2, r2s, r2o = matrix.r2, len(matrix.r2), int(len(matrix.r2)/2)
    r3, r3s, r3o = matrix.r3, len(matrix.r3), int(len(matrix.r3)/2)

    if len(image.shape) == 2:
        for i in range(dim[0]):
            for j in range(dim[1]):
                opx = _img[i][j]
                npx = (np.floor(opx/128)*255).astype(np.uint8)
                error = opx-npx

                indr1 = clip(j+r1s+1, 0, dim[1])
                _img[i, j+1:indr1] += (r1 * error).astype(dt)[0:len(_img[i, j+1:indr1])]

                indr2 = [clip(i+1, 0, dim[0]-1), clip(j-r2o, 0, dim[1]), clip(j+r2s-r2o, 0, dim[1])]
                _img[indr2[0], indr2[1]:indr2[2]] += (r2 * error).astype(dt)[0:len(_img[indr2[0], indr2[1]:indr2[2]])]

                indr3 = [clip(i+2, 0, dim[0]-1), clip(j-r3o, 0, dim[1]), clip(j+r3s-r3o, 0, dim[1])]
                _img[indr3[0], indr3[1]:indr3[2]] += (r3 * error).astype(dt)[0:len(_img[indr3[0], indr3[1]:indr3[2]])]
                

                out[i][j] = npx
    
    elif len(image.shape) == 3:
        for i in range(dim[0]):
            for j in range(dim[1]):
                opx = _img[i][j]
                npx = (np.floor(opx/128)*255).astype(np.uint8)
                error = np.average(opx-npx)

                indr1 = clip(j+r1s+1, 0, dim[1])
                _img[i, j+1:indr1, 0] += (r1 * error).astype(dt)[0:len(_img[i, j+1:indr1, 0])]

                indr2 = [clip(i+1, 0, dim[0]-1), clip(j-r2o, 0, dim[1]), clip(j+r2s-r2o, 0, dim[1])]
                _img[indr2[0], indr2[1]:indr2[2], 0] += (r2 * error).astype(dt)[0:len(_img[indr2[0], indr2[1]:indr2[2], 0])]

                indr3 = [clip(i+2, 0, dim[0]-1), clip(j-r3o, 0, dim[1]), clip(j+r3s-r3o, 0, dim[1])]
                _img[indr3[0], indr3[1]:indr3[2], 0] += (r3 * error).astype(dt)[0:len(_img[indr3[0], indr3[1]:indr3[2], 0])]
                

                out[i][j] = npx

    return out

def floyd_steinberg(image : np.ndarray) -> np.ndarray:
    _img = image.copy()
    _img = np.where(_img, )

# Constants

# Bayer Matrices
_ = np.array([
    [0, 2], 
    [3, 1]])
BAYER_MATRIX_2X2 = LinearMatrix(_, (1/4))
_ = np.array([
    [0, 8, 2, 10], 
    [12, 4, 14, 6], 
    [3, 11, 1, 9], 
    [15, 7, 13, 5]])
BAYER_MATRIX_4X4 = LinearMatrix(_, (1/16))
_ = np.array([
    [0, 34, 8, 40, 2, 34, 10, 42], 
    [42, 16, 56, 24, 50, 18, 58, 26],
    [12, 44, 4, 36, 14, 46, 6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [3, 35, 11, 43, 1, 33, 9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21]])
BAYER_MATRIX_8X8 = LinearMatrix(_, (1/64))
# Halftone Matrices
_ = np.array([
    [2, 5, 2],
    [5, 8, 5],
    [2, 5, 2]])
HALFTONE_MATRIX_3X3 = LinearMatrix(_, (1/9))
_ = np.array([
    [4, 9, 14, 9, 4],
    [9, 14, 19, 14, 9],
    [14, 19, 24, 19, 14],
    [9, 14, 19, 14, 9],
    [4, 9, 14, 9, 4]])
HALFTONE_MATRIX_5X5 = LinearMatrix(_, (1/25))
_ = np.array([
    [6, 13, 20, 27, 20, 13, 6],
    [13, 20, 27, 34, 27, 20, 13],
    [20, 27, 34, 41, 34, 27, 20],
    [27, 34, 41, 48, 41, 34, 27],
    [20, 27, 34, 41, 34, 27, 20],
    [13, 20, 27, 34, 27, 20, 13],
    [6, 13, 20, 27, 20, 13, 6]])
HALFTONE_MATRIX_7X7 = LinearMatrix(_, (1/49))
# Hatch Matrices
_ = np.array([
    [2, 5, 8],
    [5, 8, 5],
    [8, 5, 2]])
HATCH_MATRIX_3X3 = LinearMatrix(_, (1/9))
_ = np.array([
    [4, 9, 14, 19, 24],
    [9, 14, 19, 24, 19],
    [14, 19, 24, 19, 14],
    [19, 24, 19, 14, 9],
    [24, 19, 14, 9, 4]])
HATCH_MATRIX_5X5 = LinearMatrix(_, (1/25))
_ = np.array([
    [6, 13, 20, 27, 34, 41, 48],
    [13, 20, 27, 34, 41, 48, 41],
    [20, 27, 34, 41, 48, 41, 34],
    [27, 34, 41, 48, 41, 34, 27],
    [34, 41, 48, 41, 34, 27, 20],
    [41, 48, 41, 34, 27, 20, 13],
    [48, 41, 34, 27, 20, 13, 6]])
HATCH_MATRIX_7X7 = LinearMatrix(_, (1/49))
# Floyd–Steinberg Matrix
FLOYD_STEINBERG = DiffuseMatrix(
    np.array([7]),
    np.array([3, 5, 1]),
    np.array([0, 0, 0]),
    (1/16))
# Sierra Matrix
SIERRA = DiffuseMatrix(
    np.array([4, 3]),
    np.array([1, 2, 3, 2, 1]),
    np.array([0, 0, 0]),
    (1/16))