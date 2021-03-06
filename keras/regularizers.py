"""Built-in regularizers.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import six
from . import backend as K
from .utils.generic_utils import serialize_keras_object
from .utils.generic_utils import deserialize_keras_object

############################################
import tensorflow as tf
############################################


class Regularizer(object):
    """Regularizer base class.
    """

    def __call__(self, x):
        return 0.

    @classmethod
    def from_config(cls, config):
        return cls(**config)


class L1L2(Regularizer):
    """Regularizer for L1 and L2 regularization.

    # Arguments
        l1: Float; L1 regularization factor.
        l2: Float; L2 regularization factor.
    """

    def __init__(self, l1=0., l2=0.):
        self.l1 = K.cast_to_floatx(l1)
        self.l2 = K.cast_to_floatx(l2)

    def __call__(self, x):
        regularization = 0.
        if self.l1:
            regularization += K.sum(self.l1 * K.abs(x))
        if self.l2:
            regularization += K.sum(self.l2 * K.square(x))
        return regularization

    def get_config(self):
        return {'l1': float(self.l1),
                'l2': float(self.l2)}


# Aliases.


def l1(l=0.01):
    return L1L2(l1=l)


def l2(l=0.01):
    return L1L2(l2=l)


def l1_l2(l1=0.01, l2=0.01):
    return L1L2(l1=l1, l2=l2)


def serialize(regularizer):
    return serialize_keras_object(regularizer)


def deserialize(config, custom_objects=None):
    return deserialize_keras_object(config,
                                    module_objects=globals(),
                                    custom_objects=custom_objects,
                                    printable_module_name='regularizer')


def get(identifier):
    if identifier is None:
        return None
    if isinstance(identifier, dict):
        return deserialize(identifier)
    elif isinstance(identifier, six.string_types):
        config = {'class_name': str(identifier), 'config': {}}
        return deserialize(config)
    elif callable(identifier):
        return identifier
    else:
        raise ValueError('Could not interpret regularizer identifier: ' +
                         str(identifier))

####################################################################################################################################

# class Memoire_Regularizer(Regularizer):
#     def __init__(self, lambd, C_red, C_green, C_blue):
#         self.lambd = lambd
#         self.C_red = K.variable(C_red, dtype= 'float32')
#         self.C_green = K.variable(C_green, dtype= 'float32')
#         self.C_blue = K.variable(C_blue, dtype= 'float32')

#     def __call__(self, x):
#         A = (self.C_red + self.C_green + self.C_blue)/3
#         B = K.dot(K.transpose(K.square(x)), A)
#         C = self.lambd * B
#         D = tf.diag_part(C)
#         E = K.sum(D)
#         return E
# #         return K.sum(tf.diag_part(self.lambd * K.dot(K.transpose(K.square(x)), (self.C_red + self.C_green + self.C_blue)/3)))
    

#     def get_config(self):
#         return {'lambd': float(self.lambd),
#                 'C_red': K.eval(self.C_red),
#                 'C_green': K.eval(self.C_green),
#                 'C_blue': K.eval(self.C_blue)
#                }

####################################################################################################################################

class Memoire_Regularizer(Regularizer):
    def __init__(self, lambd, C_avg):
        self.lambd = lambd
        self.C_avg = K.variable(C_avg, dtype= 'float32')

    def __call__(self, W):
        dot_product = K.dot(K.transpose(K.square(W)), self.C_avg)
        lambd_mult = self.lambd * dot_product
        diag_matrix = tf.diag_part(lambd_mult)
        regularization = K.sum(diag_matrix)
        return regularization
    
#         regularization = return K.sum(tf.diag_part(self.lambd * K.dot(K.transpose(K.square(W)), self.C_avg)))
#         return regularization
    

    def get_config(self):
        return {'lambd': float(self.lambd),
                'C_avg': K.eval(self.C_avg)
               }
