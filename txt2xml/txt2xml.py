#!/usr/bin/env python

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

def write_xml(output_filename):
    '''
    Write to xml file with the PASCAL VOC style
    '''
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = 'VOC2007'
    ET.SubElement(annotation, "filename").text = '000006.jpg'

    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = 'The VOC2007 Database'

    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(256)
    ET.SubElement(size, "height").text = str(256)
    ET.SubElement(size, "depth").text = str(3)

    object_01 = ET.SubElement(annotation, "object")
    ET.SubElement(object_01, "name").text = 'cat'
    ET.SubElement(object_01, "difficult").text = str(0)

    bndbox = ET.SubElement(object_01, "bndbox")
    ET.SubElement(bndbox, "xmin").text = str(187)
    ET.SubElement(bndbox, "ymin").text = str(135)
    ET.SubElement(bndbox, "xmax").text = str(282)
    ET.SubElement(bndbox, "ymax").text = str(242)

    indent(annotation)
    tree = ET.ElementTree(annotation)
    tree.write(output_filename)

if __name__ == "__main__":
    output_filename = "output.xml"
    write_xml(output_filename)
