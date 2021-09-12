# All code written by Andrew Michael Combs

import cv2
import numpy as np

# Converts image bitdepth
def convert_bitdepth(image : np.ndarray, bitdepth : int, threshold=128) -> np.ndarray:
    _img = image.copy()

    # A switch statement would be really useful here
    if bitdepth == 1: 
        img = _img.astype(np.uint8)
        out = np.where(img > threshold, 0, 255)
    elif bitdepth == 8: out = _img.astype(np.uint8)
    elif bitdepth == 16: out = _img.astype(np.uint16)
    elif bitdepth == 32: out = _img.astype(np.uint32)
    else: return image
    
    return out

# Converts image colorspace (0 -> RGB, 1 -> BGR, 2 -> Grayscale)
def convert_colorspace(image : np.ndarray, colorspace : int) -> np.ndarray:
    _img = image.copy()

    # A switch statement would be really useful here
    if colorspace == 0: _img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif colorspace == 1: _img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif colorspace == 2: _img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    return _img

# Resizes image
def resize_image(image : np.ndarray, x : float, y : float):
    dim = image.shape
    return cv2.resize(image, (int(dim[1]*x), int(dim[0]*y)))