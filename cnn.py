# -*- coding: utf-8 -*-
"""fer2013-cnn.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11Iy0Qh8E0JdTHyyyJvYkFKm3A2GsT9OC
"""

# Taken from https://www.kaggle.com/code/lxyuan0420/facial-expression-recognition-using-cnn

import numpy as np
import pandas as pd
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import binary_crossentropy
import cv2
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras import layers, models
from keras.models import Model
from tensorflow.keras.layers import Input

# %cd '/content/drive/MyDrive/JSCHack2024'
df = pd.read_csv('fer2013.csv')

def preprocess_image(image, width=48, height=48):
    pixels = np.array(image.split(), dtype=np.uint8)

    image = pixels.reshape((48, 48))

    image = cv2.equalizeHist(image)

    image = cv2.resize(image, (width, height))

    image = image / 255.0

    image = np.expand_dims(image, axis=-1)

    return image

x = np.array([preprocess_image(image) for image in df['pixels']])
y = df['emotion']

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)

height = 48
width = 48

model = models.Sequential([
    Input(shape=(height, width, 1)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(7, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(xtrain, ytrain, epochs=10, batch_size=32, validation_split=0.2)

test_loss, test_accuracy = model.evaluate(xtest, ytest)

probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

predictions = probability_model.predict(xtest)

def plot_sample_predictions(images, labels_true, predictions, emotions, accuracy,num_samples=5):
    plt.figure(figsize=(15, 6))
    for i in range(num_samples):
        plt.subplot(1, num_samples, i+1)
        plt.imshow(images[i].reshape(48, 48), cmap='gray')
        true_label = emotions[i]
        predicted_label = emotions[np.argmax(predictions[i])]
        plt.title(f"Predicted: {predicted_label}\nTrue: {true_label}\nAccuracy: {accuracy*100:.2f}%")
        plt.axis('off')
    plt.show()