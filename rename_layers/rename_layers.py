#!/usr/bin/env python

"""
==== name_table ====
conv1 conv1_x
conv2 conv2_x
conv3 conv3_x
...
====================

Usually, you should put this file under the caffe/python.

Author: Kun Wang
"""

import numpy as np
import sys
import os.path as osp
import google.protobuf as pb
from argparse import ArgumentParser

pycaffe_dir = osp.dirname(__file__)
if osp.join(pycaffe_dir) not in sys.path:
    sys.path.insert(0, pycaffe_dir)
import caffe
from caffe.proto import caffe_pb2


def load_name_table(file):
    name_dict = {}
    with open(file) as f:
        for line in f:
            key, value = line.strip().split()
            name_dict[key] = value
    return name_dict


def check(old_net, new_net, input_name='data', mode='cpu'):
    """
    Verify the conversion.
    """
    if mode == 'cpu':
        caffe.set_mode_cpu()
    else:
        caffe.set_device(0)
        caffe.set_mode_gpu()
    inputs = np.random.rand(*old_net.blobs[input_name].data.shape)
    inputs = inputs.astype(np.float32)
    old_net.blobs[input_name].data[...] = inputs
    new_net.blobs[input_name].data[...] = inputs
    ans = old_net.forward()
    out = new_net.forward()
    for k in ans:
        assert np.allclose(ans[k], out[k]), "Conversion failed"


def parse_args():
    parser = ArgumentParser(description="Rename layer names in caffemodel")
    parser.add_argument('model', help="The net definition prototxt")
    parser.add_argument('weights', help="The weights caffemodel")
    parser.add_argument('name_table', help="Original-New name pair. Septate by space. One pair per line")
    parser.add_argument('--output_model', help="The renamed net definition prototxt")
    parser.add_argument('--output_weights', help="The renamed weights caffemodel")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()

    # Set default output file names
    if args.output_model is None:
        file_name = osp.splitext(args.model)[0]
        args.output_model = file_name + '_renamed.prototxt'
    if args.output_weights is None:
        file_name = osp.splitext(args.weights)[0]
        args.output_weights = file_name + '_renamed.caffemodel'

    name_dict = load_name_table(args.name_table)

    with open(args.model) as f:
        model = caffe_pb2.NetParameter()
        pb.text_format.Parse(f.read(), model)

        output_model = caffe_pb2.NetParameter()
        output_model.CopyFrom(model)

        weights = caffe.Net(args.model, args.weights, caffe.TEST)
        output_weights = caffe.Net(args.model, args.weights, caffe.TEST)

        for i, layer in enumerate(model.layer):
            ori_name = layer.name
            if ori_name in name_dict.keys():
                new_name = name_dict[ori_name]
                print '{} ===> {}'.format(ori_name, new_name)
                output_model.layer[i].name = new_name
                output_weights.params[ori_name] = new_name
            else:
                print ori_name

    # Check if the conversion is correct
    check(weights, output_weights)

    # Write prototxt
    with open(args.output_model, 'w') as f:
        f.write(pb.text_format.MessageToString(output_model))
        print 'Wrote to {}'.format(args.output_model)

    # Save caffemodel
    output_weights.save(args.output_weights)
    print 'Wrote to {}'.format(args.output_weights)

    print 'Done.'
