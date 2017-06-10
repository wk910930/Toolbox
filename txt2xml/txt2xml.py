#!/usr/bin/env python

import os
import sys
import xml.etree.cElementTree as ET

def indent(elem, level=0):
    '''
    Copy and modified from http://effbot.org/zone/element-lib.htm#prettyprint
    it basically walks your tree and adds spaces and newlines so the tree is
    printed in a nice way
    '''
    i = '\n' + level * '  '
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def write_xml(item, ind_to_class, output_filename=None):
    '''
    Write to xml file with the PASCAL VOC style
    '''
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = item['folder']
    ET.SubElement(annotation, "filename").text = item['filename']

    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = item['database']

    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(item['width'])
    ET.SubElement(size, "height").text = str(item['height'])
    ET.SubElement(size, "depth").text = str(item['depth'])

    objects = item['objects']
    for i in xrange(len(objects)):
        cur_object = ET.SubElement(annotation, "object")
        ET.SubElement(cur_object, "name").text = ind_to_class[objects[i]['class_index']]
        ET.SubElement(cur_object, "difficult").text = str(1)

        bndbox = ET.SubElement(cur_object, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(objects[i]['xmin'])
        ET.SubElement(bndbox, "ymin").text = str(objects[i]['ymin'])
        ET.SubElement(bndbox, "xmax").text = str(objects[i]['xmax'])
        ET.SubElement(bndbox, "ymax").text = str(objects[i]['ymax'])

    # Write to disk if output_filename is given
    if output_filename is not None:
        indent(annotation)
        tree = ET.ElementTree(annotation)
        tree.write(output_filename)

if __name__ == "__main__":
    src_txt = sys.argv[1]
    output_dir = sys.argv[2]
    ind_to_class = {1:'car', 2:'nonMotorVehicle', 3:'human'}

    print 'Convert [{}] and write to [{}]'.format(src_txt, output_dir)

    # Notice: The following parsing code is just for one kind of txt file format.
    # Modify it according to your own txt file format.
    with open(src_txt) as file:
       while True:
            line = file.next().rstrip()
            # Set EOF manually. There should be a better implementation.
            if line == 'EOF':
                break
            else:
                # Find a new annotation
                if '#' in line:
                    # filename: sub-folder/filename.jpg
                    filename = file.next().split('/')
                    # meta_data: [channel, height, width]
                    meta_data = file.next().split()
                    num_windows = int(file.next())
                    # Create dict
                    item = {}
                    item['folder'] = filename[0]
                    item['filename'] = filename[1].rstrip()
                    item['database'] = 'AutoPilot_SenseTime_HongKong'
                    item['depth'] = int(meta_data[0])
                    item['height'] = int(meta_data[1])
                    item['width'] = int(meta_data[2])
                    # Iterate bounding boxes (i.e. objects)
                    if num_windows < 1:
                        print '[WARNING] No bounding box found in {}'.format(item['filename'])
                    objects = []
                    for i in xrange(num_windows):
                        bndbox = {}
                        bndbox_meta = file.next().split()
                        bndbox['class_index'] = int(bndbox_meta[0])
                        bndbox['xmin'] = int(float(bndbox_meta[1]))
                        bndbox['ymin'] = int(float(bndbox_meta[2]))
                        bndbox['xmax'] = int(float(bndbox_meta[3]))
                        bndbox['ymax'] = int(float(bndbox_meta[4]))
                        objects.append(bndbox)
                    assert num_windows == len(objects), 'num_windows should be equal to len(objects)'
                    item['objects'] = objects
                    # Write to xml
                    path = os.path.join(output_dir, item['folder'])
                    if not os.path.isdir(path):
                        os.makedirs(path)
                    output_filename = os.path.join(path, os.path.splitext(item['filename'])[0] + '.xml')
                    write_xml(item, ind_to_class, output_filename)
                    print 'Processed {}'.format(item['filename'])
