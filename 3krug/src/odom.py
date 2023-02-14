#!/usr/bin/python3
# coding: utf-8

import rospy
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import Odometry


def callback(msg):
    ticks = msg.data
    ticksPerMeter = 7719
    radious = 0.11
    dxT = (ticks[0] + ticks[1]) / 2
    dyT = (ticks[0] - ticks[2]) / 2
    dwT = (ticks[0] + ticks[1] + ticks[2]) / 3
    dx = dxT / ticksPerMeter
    dy = dxY / ticksPerMeter
    dalpha = dwT / ticksPerMeter / radious
    now = rospy.Time.now()
    odom.header.stamp = now
    dt = 50 * 10 **(-3)
    dvx = dx / dt
    dvy = dy / dt
    dW = dalpha / dt
    

rospy.init_node("odom3")
sub = rospy.Subscriber('tiks', Float32MultiArray, callback)
pub = rospy.Publisher('odom', Odometry, queue_size=1)
rate = rospy.Rate(1)
odom = Odometry()

rospy.loginfo("Odom calculator ready!")
rospy.spin()

