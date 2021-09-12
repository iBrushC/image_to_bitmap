# All code written by Andrew Michael Combs

import cv2
import numpy as np
from imagehandler import convert_colorspace
import os


class FileHandler():
    def __init__(self, read_path, write_path, tmp_path):
        self.read_path = read_path
        self.write_path = write_path
        self.tmp_path = tmp_path
        self.tmp_path = "C:/tmp"
    
    def read_image(self) -> np.ndarray:
        img = cv2.imread(self.read_path, 1)
        return convert_colorspace(img, 2)

    def write_tmp_image(self, image : np.ndarray):
        cv2.imwrite(os.path.join(self.tmp_path, "tmp.png"), image)
        return

    def write_bitmap_txt(self, image : np.ndarray, scan : int):
        # Bitmap write
        print("Initial bitmap testing")
        xy = image.shape
        if len(xy) > 2 or np.max(image) > 255:
            return
        
        print("Testing completed")

        h1 = "// Width: {}, Height: {}\n".format(xy[1], xy[0])
        h2 = "PROGMEM const uint8_t {}[{}] = ".format("SAMPLE_IMAGE_NAME", int(xy[1]*xy[0]/8)) + "{\n    "
        end = "\n};"

        print("Writing bit array")
        bit_array = ""
        if scan == 0:
            for x in range(xy[1]):
                for y in range(xy[0]):
                    bit_array += str(int(image[y, x]>0))
        else:
            for x in range(xy[0]-1):
                for y in range(xy[1]-1):
                    bit_array += str(int(image[x, y]>0))
        print("Bit array writing successful")
        print("Converting to hex array")
        hex_array = []
        for i in range(int(xy[1]*xy[0]/8)):
            hex_i = hex(int('0b' + bit_array[i:i+8], 2))
            hex_s = (str(hex_i) + ',')
            hex_array.append((hex_s + ' ') if len(hex_s) == 5 else (hex_s + '  '))

        print("Hex array conversion complete")
        # Rows are currently 16 bytes long but thats just stylistic preference
        rowlen = 16

        print("Formatting hex array to string")
        # Formatting
        out = h1+h2
        for i in range(len(hex_array)):
            # hex_array[i] = str(i) + ' '
            if i+1 == len(hex_array):
                out += hex_array[i]
                break
            if (i+1)%rowlen==0 and i > 1:
                out += hex_array[i] + '\n    '
            else:
                out += hex_array[i]
            
        print("Finished formatting hex array")
        out += end
        
        print("Image has been successfully written")
        with open(self.write_path, 'w') as f:
            f.write(out)
        
        return


    def write_bitmap_png(self, image : np.ndarray):
        cv2.imwrite(self.write_path, image)
        return
