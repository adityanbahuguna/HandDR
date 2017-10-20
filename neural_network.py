import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('/tmp/data/', one_hot=True)
# 2 => [0, 0, 1, 0, 0, 0, 0, 0, 0, 0] => es wurde die 2 erkannt

# Neuronen in den Layern
hidden_layer_1_nodes = 500
hidden_layer_2_nodes = 500
output_layer_nodes = 500

classes = 10
batch_size = 100

X = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

def nn_model(X):
    input_layer = {'weights': tf.Variable(tf.truncated_normal([784, hidden_layer_1_nodes], stddev=0.1)),
                    'biases': tf.Variable(tf.truncated_normal([hidden_layer_1_nodes], stddev=0.1))}

    hidden_layer_1 = {'weights': tf.Variable(tf.truncated_normal([hidden_layer_1_nodes, hidden_layer_2_nodes], stddev=0.1)),
                    'biases': tf.Variable(tf.truncated_normal([hidden_layer_2_nodes], stddev=0.1))}

    hidden_layer_2 = {'weights': tf.Variable(tf.truncated_normal([hidden_layer_2_nodes, output_layer_nodes], stddev=0.1)),
                    'biases': tf.Variable(tf.truncated_normal([output_layer_nodes], stddev=0.1))}

    output_layer = {'weights': tf.Variable(tf.truncated_normal([output_layer_nodes, classes], stddev=0.1)),
                    'biases': tf.Variable(tf.truncated_normal([classes], stddev=0.1))}

    input_layer_sum = tf.add(tf.matmul(X, input_layer['weights']), input_layer['biases'])
    input_layer_sum = tf.nn.relu(input_layer_sum)

    hidden_layer_1_sum = tf.add(tf.matmul(input_layer_sum, hidden_layer_1['weights']), hidden_layer_1['biases'])
    hidden_layer_1_sum = tf.nn.relu(hidden_layer_1_sum)

    hidden_layer_2_sum = tf.add(tf.matmul(hidden_layer_1_sum, hidden_layer_2['weights']), hidden_layer_2['biases'])
    hidden_layer_2_sum = tf.nn.relu(hidden_layer_2_sum)

    output_layer_sum = tf.add(tf.matmul(hidden_layer_2_sum, output_layer['weights']), output_layer['biases'])

    return output_layer_sum

def nn_train(X):
    pred = nn_model(X)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    epochs_list = 30

    for epochs in epochs_list:
    
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for epoch in range(epochs):
                epoch_loss = 0.0
                for _ in range(int(mnist.train.num_examples/batch_size)):
                    epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                    _, c = sess.run([optimizer, cost], feed_dict={X: epoch_x, y: epoch_y})
                    epoch_loss += c

                print('Epoch ', epoch, ' of ', epochs, ' with loss: ', epoch_loss)

            correct_result = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))

            accuracy = tf.reduce_mean(tf.cast(correct_result, 'float'))
            print('Acc: ', accuracy.eval({X:mnist.test.images, y:mnist.test.labels}))

nn_train(X)