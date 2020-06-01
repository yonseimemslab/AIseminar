import tensorflow as tf
#tf.logging.set_verbosity(tf.logging.ERROR)  # warning 출력 방지
from keras.applications.resnet50 import ResNet50, decode_predictions
resnet = ResNet50()
resnet.summary()