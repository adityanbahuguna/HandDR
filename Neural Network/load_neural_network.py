# Imports
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from plotting import *
from neural_network import *
import numpy as np
import os 
import random

# Path and Dataset
dir_path = os.path.dirname(os.path.realpath(__file__))
mnist = input_data.read_data_sets(dir_path + '/data/', one_hot=True)

# Variables
hidden_layer_1_nodes = 500
hidden_layer_2_nodes = 500
output_layer_nodes = 500
epochs = 10
learning_rate = 0.08
classes = 10
batch_size = 30
epoch_errors = []
test_size = len(mnist.test.labels)
examples = 20

# Graph reset
loaded_graph = tf.Graph()
with loaded_graph.as_default():
    # TF Placeholders
    X_b = tf.placeholder('float', [None, 784], name='X_b')
    y_b = tf.placeholder('float', name='y_b')
    # Weights Matrices
    W1_b = tf.Variable(tf.truncated_normal([784, hidden_layer_1_nodes], stddev=0.01), name='W1_b')
    W2_b = tf.Variable(tf.truncated_normal([hidden_layer_1_nodes, hidden_layer_2_nodes], stddev=0.01), name='W2_b')
    W3_b = tf.Variable(tf.truncated_normal([hidden_layer_2_nodes, output_layer_nodes], stddev=0.01), name='W3_b')
    W4_b = tf.Variable(tf.truncated_normal([output_layer_nodes, classes], stddev=0.01), name='W4_b')
    # Biases Vectors
    b1_b = tf.Variable(tf.truncated_normal([hidden_layer_1_nodes], stddev=0.01), name='b1_b')
    b2_b = tf.Variable(tf.truncated_normal([hidden_layer_2_nodes], stddev=0.01), name='b2_b')
    b3_b = tf.Variable(tf.truncated_normal([output_layer_nodes], stddev=0.01), name='b3_b')
    b4_b = tf.Variable(tf.truncated_normal([classes], stddev=0.01), name='b4_b')
    # Saver Object
    new_saver = tf.train.Saver({"W1": W1_b, "W2": W2_b, "W3": W3_b, "W4": W4_b,
                                "b1": b1_b, "b2": b2_b, "b3": b3_b, "b4": b4_b})

# Define the Neural Network
def nn_model(X_b):
    input_layer     =    {'weights': W1_b, 'biases': b1_b}
    hidden_layer_1  =    {'weights': W2_b, 'biases': b2_b}
    hidden_layer_2  =    {'weights': W3_b, 'biases': b3_b}
    output_layer    =    {'weights': W4_b, 'biases': b4_b}

    input_layer_sum = tf.add(tf.matmul(X_b, input_layer['weights']), 
                            input_layer['biases'])
    input_layer_sum = tf.nn.relu(input_layer_sum)

    hidden_layer_1_sum = tf.add(tf.matmul(input_layer_sum, hidden_layer_1['weights']), 
                            hidden_layer_1['biases'])
    hidden_layer_1_sum = tf.nn.relu(hidden_layer_1_sum)

    hidden_layer_2_sum = tf.add(tf.matmul(hidden_layer_1_sum, hidden_layer_2['weights']), 
                            hidden_layer_2['biases'])
    hidden_layer_2_sum = tf.nn.relu(hidden_layer_2_sum)

    output_layer_sum = tf.add(tf.matmul(hidden_layer_2_sum, output_layer['weights']), 
                            output_layer['biases'], name="op_to_restore")
    return output_layer_sum

# Train the Neural Network
def nn_test(X_b):
    with tf.Session(graph=loaded_graph) as sess:
        # Restore variables from disk.
        new_saver = tf.train.import_meta_graph(dir_path + "/data/model.ckpt.meta")
        new_saver.restore(sess, dir_path + "/data/model.ckpt")
        # Load Tensors
        X_b = loaded_graph.get_tensor_by_name('X:0')
        y_b = loaded_graph.get_tensor_by_name('y:0')

        # Test Code
        for i in range(examples):
            rand_index = random.randint(1, test_size)
            pred = nn_model(np.reshape(mnist.test.images[rand_index], (1, 784)))
            max_val = tf.argmax(pred, 1)
            display_digit(mnist.test.images[rand_index], mnist.test.labels[rand_index], sess.run(max_val))

if __name__ == "__main__":
    nn_test(X_b)