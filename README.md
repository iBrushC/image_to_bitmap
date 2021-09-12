# Image To Bitmap in Python
A simple image-to-bitmap converter made in python. Several types of dithering are included to make images usable in color-restrained displays such as mono color TFT or E-Paper displays.

This was a quick weekend project to learn about error diffusion dithering and actually making a usable piece of software. This is by no means a perfect program and has its list of issues, but for about 12-15 hours of work I'm happy with it. While the software is limited in the dithering that it allows, `ditherer.py` has the capabilities to run almost any linear or error diffusion dithering (Floyd-Steinberg and Sierra are included).

The code is likely not as optimized as it could be, but I do not think I will be updating it further as it's in a place I'm currently happy with. In the future I'll be using either C/C++ or Rust for image processing, as Python is horribly inefficient for this kind of stuff. 
