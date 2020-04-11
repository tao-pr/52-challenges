import tensorflow as tf
import numpy as np
import joblib

def build(w: int):
  """
  Build the model for training
  Args:
    w (int): Width of input image
  """
  model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(filters=5, kernel_size=(3,3), input_shape=(w,w,1)),
    tf.keras.layers.MaxPool2D(pool_size=(2,2)),
    tf.keras.layers.Conv2D(filters=5, kernel_size=(3,3), activation='relu'),
    tf.keras.layers.SpatialDropout2D(rate=0.1),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dense(2, activation='relu')
  ])
  model.summary()
  return model

