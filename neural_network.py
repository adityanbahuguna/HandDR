import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('/tmp/data/', one_hot=True)
# 2 => [0, 0, 1, 0, 0, 0, 0, 0, 0, 0] => es wurde die 2 erkannt

# Neuronen in den Layern
hidden_layer_1_nodes = 300
hidden_layer_2_nodes = 100

classes = 10
batch_size = 150

X = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

def nn_model(X):
    pass

def nn_train(X):
    pass

nn_train(X)