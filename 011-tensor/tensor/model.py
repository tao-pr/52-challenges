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
    # 256x256x1
    tf.keras.layers.Conv2D(filters=8, kernel_size=(3,3), input_shape=(w,w,1)),
    tf.keras.layers.MaxPool2D(pool_size=(2,2)),
    # 127x127
    tf.keras.layers.Conv2D(filters=4, kernel_size=(3,3), activation='relu'),
    tf.keras.layers.MaxPool2D(pool_size=(4,4)),
    tf.keras.layers.SpatialDropout2D(rate=0.1),
    # 31x31
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(2, activation='relu')
  ])
  model.summary()
  opt = tf.keras.optimizers.RMSprop(0.001)

  model.compile(
    loss='mse',
    optimizer=opt,
    metrics=['mae', 'mse'])

  return model

if __name__ == '__main__':
  # Test building and inspect the model structure
  m = build(256)

