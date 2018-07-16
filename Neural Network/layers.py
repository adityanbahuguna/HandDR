# Imports
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import numpy as np
import os

from plotting import *

activation_functions = {"relu": tf.nn.relu, "sigmoid": tf.nn.sigmoid, "lrelu": tf.nn.leaky_relu,
                        "tanh": tf.nn.tanh, "relu6": tf.nn.relu6}
weight_initializers = {"truncated_normal": tf.truncated_normal}
 
# Conv Layer
def conv2d(x, W):
    return tf.nn.conv2d(x, W,
                        strides=[1,1,1,1],
                        padding="SAME")

# Max Pool
def max_pool(x):
    return tf.nn.max_pool(x,
                        ksize=[1,2,2,1],
                        strides=[1,2,2,1],
                        padding="SAME")

# Avg Pool
def avg_pool(x):
    return tf.nn.average_pool(x,
                        ksize=[1,2,2,1],
                        strides=[1,2,2,1],
                        padding="SAME")

# Dropout
def dropout(x, keep_prob=1.0):
    return tf.nn.dropout(x, keep_prob=keep_prob)

# Define a conv layer
def conv_layer(x, size_in, size_out, stddev, bias_init, k_size=5, name="conv", act="relu", weight_init="truncated_normal"):
    with tf.name_scope(name):
        initializer = weight_initializers[weight_init]
        W = tf.Variable(initializer(stddev=stddev, shape=[k_size, k_size, size_in, size_out]), name="W")
        b = tf.Variable(tf.constant(value=bias_init, shape=[size_out]), name="b")
        tf.summary.histogram("W", W)
        tf.summary.histogram("b", b)
        val = conv2d(x, W)
        val = tf.add(val, b)
        activation_func = activation_functions[act]
        val = activation_func(val)
        return val

# Define a fc layer
def fc_layer(x, size_in, size_out, stddev, bias_init, name="fc", act="relu", weight_init="truncated_normal", last_layer=False):
    with tf.name_scope(name):
        initializer = weight_initializers[weight_init]
        W = tf.Variable(initializer(stddev=stddev, shape=[size_in, size_out]), name="W")
        b = tf.Variable(tf.constant(value=bias_init, shape=[size_out]), name="b")
        tf.summary.histogram("W", W)
        tf.summary.histogram("b", b)
        val = tf.matmul(x, W)
        val = tf.add(val, b)
        if not last_layer:
            activation_func = activation_functions[act]
            val = activation_func(val)
        return val

# Transform to flattened layer
def flatten(x):
    shape = tf.shape(x)
    new_shape = shape[1] * shape[2] * shape[3]
    return tf.reshape(x, shape=[-1, new_shape])