#!/usr/bin/python3

# coding: utf-8
import rospy
from actionlib_msgs.msg import GoalStatusArray

def callback(msg):
    pass

rospy.init_node('voice_control')
sub = rospy.Subscriber('move_base/status', GoalStatusArray, callback)
rospy.loginfo("Voice Controler ready!")
rospy.spin()