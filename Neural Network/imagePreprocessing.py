# Import Modules
import numpy as np
import math
from scipy import ndimage
import matplotlib.pyplot as plt
from scipy.cluster.vq import whiten

# Downsampel Resolution
def downsample(myimage, factor, estimator=np.nanmean):
    ys, xs = myimage.shape
    crimage = myimage[:ys-(ys % int(factor)),:xs-(xs % int(factor))]
    dsimage = estimator( np.concatenate([[crimage[i::factor,j::factor]
        for i in range(factor)] 
        for j in range(factor)]), axis=0) 
    return dsimage

# Normalize image data
def normalize(image):
    # Threshold for pixels
    for row in range(len(image)):
        for col in range(len(image[row])):
            if image[row][col] < 50.0:  
                image[row][col] = 0.0    
            if image[row][col] > 200.0:  
                image[row][col] = 255.0
    # New datarange
    image = image / 255.0 
    image = whiten(image)
    return image

# Get the Numpy image from the Image
def get_image(DrawingFrame):
    p = DrawingFrame.grab()
    p.save('image', 'jpg')
    image = load_image('image').astype(np.float32)
    image = downsample(image, 4)
    image = normalize(image)
    return image

# Load saved image into binary numpy image
def load_image(infilename) :
    img = ndimage.imread(infilename, mode='L')
    for i in range(len(img)):
        for j in range(len(img[i])):
            if i != 0 and i != len(img) - 1 and j != 0 and j != len(img[i]) - 1:
                if img[i][j] > 125.0:
                    img[i][j] = 0.0
                else:
                    img[i][j] = 255.0    
            else:
                img[i][j] = 0.0
    return img