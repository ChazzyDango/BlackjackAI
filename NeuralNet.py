import tensorflow as tf
import matplotlib.pyplot as plt


class Neuralnet:
    def __init__(self):
        # 1 node for if Ace is in hand
        # 5 nodes for my card sum (Binary) (max = 2^5 = 31)
        # 5 nodes for dealer card sum (Binary) (max = 2^5 = 31)
        n_input = 11
        # eg. 1 00101 01010 is I have an Ace and a 2, dealer has a 10 showing

        # 5 hidden nodes because testing
        n_hidden = 5

        # Nodes for Hit, Stand, Double, or Split
        n_output = 4

        # Neural Network Variables
        self.learning_rate = 0.001
        self.n_iterations = 100
        self.dropout = 0.5

        # Setting the initial values for the connections/inputs for the neural network to each layer
        initial_w1 = 0.01
        initial_w2 = 0.01
        bias1 = 0.001
        bias2 = 0.001

        # Initializing the tensorflow variables for the inputs and outputs as placeholders
        self.X = tf.placeholder("float", [None, n_input])
        self.Y = tf.placeholder("float", [None, n_output])
        # Setting a variable placeholder for the dropout rate
        self.keep_prob = tf.placeholder(tf.float32)

        # sets the initial weights, w1 = input to hidden layer 1, out = hidden layer 1 to output
        weights = {
            'w1': tf.Variable(tf.truncated_normal([n_input, n_hidden], stddev=initial_w1)),
            'out': tf.Variable(tf.truncated_normal([n_hidden, n_output], stddev=initial_w2)),
        }

        # setting low biases as the inputs should not change TOO much
        biases = {
            'b1': tf.Variable(tf.constant(bias1, shape=[n_hidden])),
            'out': tf.Variable(tf.constant(bias2, shape=[n_output]))
        }

        # initializes the layers with the given weights, inputs, and biases
        # tf.add sums up the contents, as a layer should do (sum(weight * input))
        # tf.matmul = matrix multiplication (input vector x Weights vector)
        layer_1 = tf.add(tf.matmul(X, weights['w1']), biases['b1'])
        output_layer = tf.add(tf.matmul(layer_1, weights['out']), biases['out'])

        # Attempts to reduce the mean between the actual labels and output layer labels,
        # Y is like a variable name, the actual labels are assigned later when we call run
        self.cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=output_layer))
        # Optimizes the training process using the Adam optimization algorithm
        # attempts to minimize the cross entropy (difference between predicted label and actual label)
        self.train_step = tf.train.AdamOptimizer(self.learning_rate).minimize(self.cross_entropy)

        # Determines if the output layer's value is the same as the label value assigned to Y (the actual label during the run)
        # During the run it'll be true if correct, false if incorrect
        correct_pred = tf.equal(tf.argmax(output_layer, 1), tf.argmax(Y, 1))
        # Casts the predictions to a float and calculates the average accuracy overall during the run
        self.accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

        self.init_variables = tf.global_variables_initializer()
        # Initializes the neural network as an object
        self.neural_network = tf.Session()
        # Runs the neural network with the global variables required from tensorflow
        self.neural_network.run(tf.global_variables_initializer())

    def train(self,training_data, n_epochs = 100):
        # Training_data[0] = list of Input Values, Training_data[1] = List of labels (From CSV File)
        for j in range(n_epochs):
            # train on the entire set of training images and labels, with a dropout rate to avoid over fitting
            self.neural_network.run(self.train_step, feed_dict={self.X: training_data[0], self.Y: training_data[1], self.keep_prob: self.dropout})
            # Gets the Loss and Accuracy on the set as of the current epoch (this does not train it, just evaluates)
            # Runs using all neurons and uses ALL results from the layers for evaluation
            epoch_loss, epoch_accuracy = \
                self.neural_network.run([self.cross_entropy, self.accuracy],
                                   feed_dict={self.X: training_data[0], self.Y: training_data[1], self.keep_prob: 1.0})

    # TODO def evaluate(self, test_data):


