import tensorflow as tf
import numpy as np
import joblib

def build(imsize: int):
  """
  Build the model for training
  """
  model = tf.keras.models.Sequential([
    # Normalise each image independently 
    tf.keras.layers.LayerNormalization(epsilon=0.005, scale=False),
    tf.keras.layers.Conv2D(filters=5, kernel_size=(3,3)),
  ])
  return model

