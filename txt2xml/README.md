# txt2xml

This tool is used to demonstrate how to covert a txt file to xml,
which is employed by [PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/) as the annotation format.
How to parse the input txt is not the focus of the tool, and you can use your own format by modification.

### PASCAL VOC Annotation

```xml
<annotation>
  <folder>VOC2007</folder>
  <filename>000006.jpg</filename>
  <source>
    <database>The VOC2007 Database</database>
  </source>
  <size>
    <width>500</width>
    <height>375</height>
    <depth>3</depth>
  </size>
  <object>
    <name>pottedplant</name>
    <difficult>0</difficult>
    <bndbox>
      <xmin>187</xmin>
      <ymin>135</ymin>
      <xmax>282</xmax>
      <ymax>242</ymax>
    </bndbox>
  </object>
  <object>
    <name>diningtable</name>
    <difficult>0</difficult>
    <bndbox>
      <xmin>154</xmin>
      <ymin>209</ymin>
      <xmax>369</xmax>
      <ymax>375</ymax>
    </bndbox>
  </object>
  <object>
    <name>chair</name>
    <difficult>0</difficult>
    <bndbox>
      <xmin>255</xmin>
      <ymin>207</ymin>
      <xmax>366</xmax>
      <ymax>375</ymax>
    </bndbox>
  </object>
</annotation>

```

### Input TXT File

The format is inspired by the
[window_data_layer](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/window_data_layer.cpp)
used in [Caffe](https://github.com/BVLC/caffe).

```shell
# txt format
#   repeated:
#     # image_index
#     channels
#     height
#     width
#     num_windows
#     class_index x1 y1 x2 y2

# 0
000005.jpg
3
375
500
3
9 262 210 323 338
9 164 263 252 371
9 240 193 294 298
# 1
000007.jpg
3
333
500
1
7 140 49 499 329
# 2
000009.jpg
3
375
500
4
13 68 171 269 329
15 149 140 228 283
15 284 200 326 330
15 257 197 296 328
# 3
000012.jpg
3
333
500
1
7 155 96 350 269
```

### Acknowledgements

Learnd from [Creating a simple XML file using python](https://stackoverflow.com/a/3605831) and [Pretty print XML trees in python](https://norwied.wordpress.com/2013/08/27/307/).
