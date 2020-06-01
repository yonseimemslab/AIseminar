from keras.layers import Lambda
import keras.backend as K

def l2_norm(x):
    x = x ** 2
    x = K.sum(x, axis=1)
    x = K.sqrt(x)
    return x
global_l2 = Lambda(lambda x: l2_norm(x))(previous_layer)