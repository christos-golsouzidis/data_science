# -*- coding: utf-8 -*-
# Written by Christos Golsouzidis

import numpy as np
import os
import matplotlib.pyplot as plt
import keras
from keras.preprocessing.image import image_utils as iu
import cv2
import sys

src  = sys.argv[1]
dest = sys.argv[2]
try:
    original_image = iu.load_img(src)
except:
    raise Exception('ERROR: File not found')
original_imgarr = iu.img_to_array(original_image)/255
original_shape = original_imgarr.shape
x,y,z = original_shape
original_size = (y,x)

resized_imgarr = cv2.resize(original_imgarr, (412,412), interpolation = cv2.INTER_AREA)
try:
    model = keras.models.load_model('./model_final.h5')
except:
    raise Exception('ERROR: Model must be located on the same directory')
denoised_imgarr = model.predict(resized_imgarr.reshape(-1,412,412,3))
denoised_image = cv2.resize(denoised_imgarr.reshape(412,412,3),original_size,interpolation=cv2.INTER_AREA)
denoised_image = iu.array_to_img(denoised_image)
try:
    iu.save_img(dest, denoised_image)
except:
    raise Exception('ERROR: Cannot write file')





