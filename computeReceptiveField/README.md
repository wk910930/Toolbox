# A guide to receptive field arithmetic for Convolutional Neural Networks

Check [here](https://medium.com/@nikasa1889/a-guide-to-receptive-field-arithmetic-for-convolutional-neural-networks-e0f514068807)
for details.

## Usage

Assume the two dimensions are the same. Each kernel requires the following parameters:

```shell
k_i: kernel size
s_i: stride
p_i: padding
```

Each layer *i* requires the following parameters to be fully represented: 

```shell
n_i: number of feature (data layer has n_1 = imagesize )
j_i: distance (projected to image pixel distance) between center of two adjacent features
r_i: receptive field of a feature in layer i
start_i: position of the first feature's receptive field in layer i (idx start from 0, negative means the center fall into padding)
```

## Acknowledgment

Many thanks to [Dang Ha The Hien](https://medium.com/@nikasa1889)'s great work.
