import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

def display_digit(data, label, pred_label=None):
    image = data.reshape([28,28])
    label = np.argmax(label, axis=0)
    if pred_label is None:
        plt.title('Label: %d' % (label))
    else:
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