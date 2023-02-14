#!/usr/bin/python3
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
from wheelSpeeds import transformation
import numpy as np

rospy.init_node('speed_publisher')
pub = rospy.Publisher('/speed_publisher', Float32MultiArray, queue_size=1)
rate = rospy.Rate(1)
array = Float32MultiArray()
#C:\Users\Арина Лузгина\AppData\Local\Programs\Arduino IDE


def main(msg):
    vels = [msg.linear.x, msg.linear.y, msg.angular.z]
    radius = 0.11
    vels = list(map(float, vels))
    info = transformation(vels[0], vels[1], vels[2], radius)

    speeds = np.zeros(6, dtype=float)
    for i in range(3):
        if info[i] > 0:
            speeds[i * 2] = info[i]
            speeds[i * 2 + 1] = 1.0
        else:
            speeds[i * 2] = -info[i]
            speeds[i * 2 + 1] = 0.0

    array.data = speeds
    pub.publish(array)
    rate.sleep()



def callback(msg):
    main(msg)

sub = rospy.Subscriber('cmd_vel', Twist, callback)
rospy.loginfo("Ready!")
rospy.spin()
