import os
from PIL import Image
from tensorflow.compat.v1 import InteractiveSession
from tensorflow.compat.v1 import ConfigProto
import sys
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf

config = ConfigProto()
config.gpu_options.allow_growth = False
session = InteractiveSession(config=config)


saved = load_model("./cp_viton/save_ckp_frozen.h5")


class fashion_tools(object):
    def __init__(self, imageid, model=saved, version=1.1):
        self.imageid = imageid
        self.model = model
        self.version = version

    def get_dress(self, stack=False):
        name = './data/test/cloth/' + self.imageid
        file = cv2.imread(name)
        print(file)
        file = tf.image.resize_with_pad(file, 512, 384)
        file = np.expand_dims(file, axis=0) / 255.
        seq = self.model.predict(file)
        seq = seq[3][0, :, :, 0]
        seq = seq*255
        for i in range(512):
            for j in range(384):
                if seq[i][j] <= 256/2:
                    seq[i][j] = 0
                else:
                    seq[i][j] = 255
        image = Image.fromarray(seq).convert('L')
        return image
