import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
import sys
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
import os
from PIL import Image
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

class fashion_tools(object):
    def __init__(self,imageid,model,version=1.1):
        self.imageid = imageid
        self.model   = model
        self.version = version
        
    def get_dress(self,stack=False):
        """limited to top wear and full body dresses (wild and studio working)"""
        """takes input rgb----> return PNG"""
        name =  self.imageid
        file = cv2.imread(name)
        file = tf.image.resize_with_pad(file,target_height=512,target_width=384)
        rgb  = file.numpy()
        file = np.expand_dims(file,axis=0)/ 255.
        seq = self.model.predict(file)
        seq = seq[3][0,:,:,0]
        seq = seq*255
        for i in range(512):
            for j in range(384):
                if seq[i][j] <= 256/2:
                    seq[i][j] = 0
                else:
                    seq[i][j] = 255
        image = Image.fromarray(seq).convert('L')
        image.save(os.path.abspath('data/test/cloth-mask') + '/' + name)
        return image
    
###running code
def get_cloth_mask(cloth_name):
    saved = load_model("save_ckp_frozen.h5")
    mask    = fashion_tools(cloth_name, saved)
    return