import os
from PIL import Image
from cp_viton.run import fashion_tools
import cv2
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # isort:skip
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def get_mask(cloth_name):
    #cloth.save('./data/test/cloth/' + cloth_name)
    mask = fashion_tools(cloth_name)
    image_ = mask.get_dress(True)
    image_.save('./data/test/cloth-mask/' + cloth_name)
#   return
