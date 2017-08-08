#!/usr/bin/env python

"""
Transfer net parameters between Caffe versions

This (URL: https://groups.google.com/forum/#!topic/caffe-users/aeqqtyTXogY)
discussion might be helpful.
Modified from https://gist.github.com/shelhamer/ec8f96517fed5a430635

How to Use?

Let's say, we would like to transplant the caffemodel trained with Caffe of version A to Caffe of version B.
Usually, you should put this file under the caffe/python, where the caffemodel is trained with. Here it is A.

Author: Kun Wang
"""

from __future__ import division
from argparse import ArgumentParser
import sys
import os.path as osp
import numpy as np
pycaffe_dir = osp.dirname(__file__)
if osp.join(pycaffe_dir) not in sys.path:
    sys.path.insert(0, pycaffe_dir)
import caffe

def transplant(new_net, net):
    for p in net.params:
        if p not in new_net.params:
            print 'dropping', p
            continue
        for i in range(len(net.params[p])):
            if net.params[p][i].data.shape != new_net.params[p][i].data.shape:
                print 'coercing', p, i, 'from', net.params[p][i].data.shape, 'to', new_net.params[p][i].data.shape
            else:
                print 'copying', p, i
            new_net.params[p][i].data.flat = net.params[p][i].data.flat

def main(args):
    # Set default output file names
    if args.target_model is None:
        file_name = osp.splitext(args.model)[0]
        args.target_model = file_name + '_converted.prototxt'
    if args.target_weights is None:
        file_name = osp.splitext(args.weights)[0]
        args.target_weights = file_name + '_converted.caffemodel'

    # Load source weights
    source_weights = caffe.Net(args.model, args.weights, caffe.TEST)
    target_weights = caffe.Net(args.target_model, caffe.TEST)
    transplant(target_weights, source_weights)
    # Save the caffemodel
    target_weights.save(args.target_weights)

if __name__ == '__main__':
    parser = ArgumentParser(description="Transfer net parameters between Caffe versions")
    parser.add_argument('model', help="The source net definition prototxt")
    parser.add_argument('weights', help="The source weights caffemodel")
    parser.add_argument('--target_model')
    parser.add_argument('--target_weights')
    args = parser.parse_args()
    # Transplanting
    main(args)
