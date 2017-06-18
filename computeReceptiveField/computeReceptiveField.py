#!/usr/bin/env python

"""
A small python program that calculates the receptive field information for all layers
in a given CNN architecture.

Author: Dang Ha The Hien
"""
# [kernel_size, stride, padding]
#Assume the two dimensions are the same
#Each kernel requires the following parameters:
# - kernel_size
# - stride
# - padding (if padding is uneven, right padding will higher than left padding)
#
#Each layer i requires the following parameters to be fully represented:
# - n_i: number of feature (data layer has n_0 = im_size)
# - step_i: distance (projected to image pixel distance) between center of two adjacent features
# - r_i: receptive field of a feature in layer i
# - start_i: position of the first feature's receptive field in layer i (idx start from 0,
#       negative means the center fall into padding)

import math

def outFromIn(conv, input_layer):
    """Receptive Field Arithmetic
    Args:
           conv (list): [kernel_size, stride, padding]
           input_layer (list): [num, step, receptive_field, start_idx]
    Returns:
           num_out, step_out, receptive_field_out, start_out
    """

    # Extract layer information
    num_in = input_layer[0]
    step_in = input_layer[1]
    receptive_field_in = input_layer[2]
    start_in = input_layer[3]
    # Extract kernel (filter) information
    kernel_size = conv[0]
    stride = conv[1]
    padding = conv[2]
    if len(conv) == 4:
        dilation = conv[3]
        kernel_size = dilation * (kernel_size - 1) + 1
    assert kernel_size > 0
    assert stride > 0

    num_out = math.floor((num_in - kernel_size + 2 * padding) / stride) + 1
    actualP = (num_out - 1) * stride - num_in + kernel_size
    pR = math.ceil(actualP / 2)
    pL = math.floor(actualP / 2)

    step_out = step_in * stride
    receptive_field_out = receptive_field_in + (kernel_size - 1) * step_in
    start_out = start_in + ((kernel_size - 1) / 2 - pL) * step_in

    return num_out, step_out, receptive_field_out, start_out

def printLayer(layer, layer_name):
    """A helper function to print layer information"""
    print layer_name + ':'
    print '\t n features: %s \n \t step: %s \n \t receptive size: %s \t start: %s ' % (
        layer[0], layer[1], layer[2], layer[3])

def create_nn(name):
    """Create pre-defined networks"""
    # convnet[i] = [kernel_size, stride, padding]
    if name == 'AlexNet':
        convnet = [[11, 4, 0], [3, 2, 0], [5, 1, 2], [3, 2, 0], [3, 1, 1], [3, 1, 1], [3, 1, 1],
                   [3, 2, 0], [6, 1, 0], [1, 1, 0]]
        layer_names = ['conv1', 'pool1', 'conv2', 'pool2', 'conv3', 'conv4', 'conv5',
                       'pool5', 'fc6-conv', 'fc7-conv']
        im_size = 227
    elif name == 'NINNet':
        convnet = [[11, 4, 0], [1, 1, 0], [1, 1, 0], [3, 2, 0],
                   [5, 1, 2], [1, 1, 0], [1, 1, 0], [3, 2, 0],
                   [3, 1, 1], [1, 1, 0], [1, 1, 0], [3, 2, 0],
                   [3, 1, 1], [1, 1, 0], [1, 1, 0], [5, 1, 0]]
        layer_names = ['conv1', 'cccp1', 'cccp2', 'pool0',
                       'conv2', 'cccp3', 'cccp4', 'pool2',
                       'conv3', 'cccp5', 'cccp6', 'pool3',
                       'conv4-1024', 'cccp7-1024', 'cccp8-1024', 'pool4']
        im_size = 224
    elif name == 'VGGNet':
        convnet = [[3, 1, 1], [3, 1, 1], [2, 2, 0], [3, 1, 1], [3, 1, 1], [2, 2, 0],
                   [3, 1, 1], [3, 1, 1], [3, 1, 1], [2, 2, 0],
                   [3, 1, 1], [3, 1, 1], [3, 1, 1], [2, 2, 0],
                   [3, 1, 1], [3, 1, 1], [3, 1, 1], [2, 2, 0],
                   [7, 1, 0], [1, 1, 0]]
        layer_names = ['conv1_1', 'conv1_2', 'pool1', 'conv2_1', 'conv2_2', 'pool2',
                       'conv3_1', 'conv3_2', 'conv3_3', 'pool3',
                       'conv4_1', 'conv4_2', 'conv4_3', 'pool4',
                       'conv5_1', 'conv5_2', 'conv5_3', 'pool5',
                       'fc6-conv', 'fc7-conv']
        im_size = 224
    else:
        print '[WARNING] {}: Unknown network!'.format(name)
        convnet = []
        layer_names = []

    return convnet, layer_names, im_size

if __name__ == '__main__':
    name = 'AlexNet'
    convnet, layer_names, im_size = create_nn(name)
    layerInfos = []

    print '------- {} Summary ------'.format(name)
    # The first layer is the data (input image) layer with
    # - num_0 = im_size
    # - step_0 = 1
    # - receptive_field_0 = 1
    # - start_0 = 0.5
    current_layer = [im_size, 1, 1, 0.5]
    printLayer(current_layer, "input image")

    for i in xrange(len(convnet)):
        current_layer = outFromIn(convnet[i], current_layer)
        layerInfos.append(current_layer)
        printLayer(current_layer, layer_names[i])
    print '------------------------'

    layer_name = raw_input("Layer name where the feature in: ")
    layer_idx = layer_names.index(layer_name)
    idx_x = int(raw_input("index of the feature in x dimension (from 0): "))
    idx_y = int(raw_input("index of the feature in y dimension (from 0): "))

    n = layerInfos[layer_idx][0]
    j = layerInfos[layer_idx][1]
    r = layerInfos[layer_idx][2]
    start = layerInfos[layer_idx][3]
    assert idx_x < n
    assert idx_y < n

    print 'receptive field: (%s, %s)' % (r, r)
    print 'center: (%s, %s)' % (start + idx_x * j, start + idx_y * j)
