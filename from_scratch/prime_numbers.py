from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.callbacks import TensorBoard
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import time

tf.enable_eager_execution()
class PrimeNumbersClassifier:
    def __init__(self): 
        self.createData()

    def createData(self):
        # csv_file = tf.keras.utils.get_file('heart.csv', '/media/user/Transcend/AI/Datasets/primes1.txt')
        # raw_train_data = get_dataset(train_file_path)
        # raw_test_data = get_dataset(test_file_path)
        prime_numbers = pd.read_csv('/media/user/Transcend/AI/Datasets/primes1.txt', header=None, delim_whitespace=True)
        prime_numbers = prime_numbers.values.flatten()
        prime_numbers = pd.Series(prime_numbers.transpose())
        prime_numbers_and_not = pd.DataFrame({
            'PM': prime_numbers,
            'is_prime': pd.Series(1, dtype='int64')
        })
        datas_to_save = pd.DataFrame({
            'Number': range(0, prime_numbers_and_not['PM'].iloc[-1]+1)
        })
        datas_to_save['is_prime'] = datas_to_save['Number'].isin(prime_numbers_and_not['PM'])
        print(datas_to_save)
        training_dataset = (
        tf.data.Dataset.from_tensor_slices(
            (
                tf.cast(datas_to_save['Number'].values, tf.int64),
                tf.cast(datas_to_save['is_prime'].values, tf.int64)
            )
        )
        )
        return training_dataset
        
    def saveData(self, datas):
        datas.to_csv('/media/user/Transcend/AI/Datasets/primes.csv')

    def startTrain(self):
        # we will load 1 number
        x = tf.placeholder(tf.int64, [None, 1])
        # each number can have 1 of 2 classes
        W = tf.Variable(tf.zeros([1, 2]))
        b = tf.Variable(tf.zeros([2]))
        y = tf.nn.softmax(tf.matmul(x, W) + b)
        y_ = tf.placeholder(tf.int64, [None, 2])
        cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
        train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
        init = tf.initialize_global_variables()
        sess = tf.Session()
        sess.run(init)
        for i in range(1000):
            batch_xs, batch_ys = mnist.train.next_batch(100)
            sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
    