#!/usr/bin/python3
# -*- coding: utf-8 -*-
from geometry_msgs.msg import Twist
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import os
import rospy
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.gpio_slowdown = 4
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'
options.disable_hardware_pulsing = 1
matrix = RGBMatrix(options = options)

def callback(msg):
    vx, vy, vz = msg.linear.x, msg.linear.y, msg.angular.z
    
    if vx > 0 and vy > 0:
        name = "/home/pi/catkin_ws/src/3krug/images/red_arrow_north_east.png"
    elif vx > 0 and vy < 0:
        name = "/home/pi/catkin_ws/src/3krug/images/red_arrow_north_west.png"
    elif vx > 0 and vy == 0:
        name = "/home/pi/catkin_ws/src/3krug/images/red_arrow_nort.png"
    elif vx == 0 and vy > 0:
        name = "/home/pi/catkin_ws/src/3krug/images/red_arrow_east.png"
    elif vx == 0 and vy < 0:
        name = "/home/pi/catkin_ws/src/3krug/images/red_arrow_west.png"
    elif vx < 0 and vy == 0:
        name = "/home/pi/catkin_ws/src/3krug/images/red_arrow_south.png"
    elif vx < 0 and vy < 0:
        name = "/home/pi/catkin_ws/src/3krug/images/red_arrow_south_west.png"
    elif vx < 0 and vy > 0:
        name = "/home/pi/catkin_ws/src/3krug/images/red_arrow_south_east.png"
    elif vz > 0:
        name = "/home/pi/catkin_ws/src/3krug/images/red_arrow_clockwise.png"
    elif vz < 0:
        name = "/home/pi/catkin_ws/src/3krug/images/red_arrow_counterclockwise.png"
    else:
        name = "/home/pi/catkin_ws/src/3krug/images/stop.png"
    #image_file = "/home/pi/catkin_ws/src/3krug/images/red_arrow_clockwise.png"
    image = Image.open(name)
    # Make image fit our screen.
    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    # Configuration for the matrix

    matrix.SetImage(image.convert('RGB'))
    time.sleep(4)
    name = "/home/pi/catkin_ws/src/3krug/images/logo.png"
    image = Image.open(name)
    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    # Configuration for the matrix

    matrix.SetImage(image.convert('RGB'))

rospy.init_node('viz')
sub = rospy.Subscriber('/cmd_vel', Twist, callback)
rospy.spin()

