import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

def display_digit(data, label=None, pred_label=None):
    image = data.reshape([len(data), len(data[0])])
    label = np.argmax(label, axis=0)
    if pred_label is None and label is not None:
        plt.title('Label: %d' % (label))
    elif label is not None:
        plt.title('Label: %d, Pred: %d' % (label, pred_label))
    plt.imshow(image, cmap=plt.get_cmap('gray_r'))
    plt.show()

def display_convergence(error):
    if isinstance(error, list):
        plt.plot(error)
        plt.title('Error of the NN')
        plt.xlabel('Epoch')
        plt.ylabel('Error')
        plt.show()
        plt.savefig('error.png')