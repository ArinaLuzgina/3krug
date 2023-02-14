#!/usr/bin/python3
# coding: utf-8
import rospy
from std_msgs.msg import String

def callback(msg):
    pass

rospy.init_node('voice_control')
sub = rospy.Subscriber('/abot/stt/kws_data', String, callback)
rospy.loginfo("Voice Controler ready!")
rospy.spin()