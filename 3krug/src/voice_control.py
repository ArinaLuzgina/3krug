#!/usr/bin/python3
# coding: utf-8
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import time

rospy.init_node('goals')
pub1 = rospy.Publisher('patrol_control', String, queue_size=10)
pub2 = rospy.Publisher('/light', String, queue_size=10)
pub3 = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rate = rospy.Rate(1)
speeds = Twist()
startNavigation = False
def callback(msg):
    global startNavigation
    phrase = msg.data
    point = (0, 0, 0)
    points = ["one", "two", "three"]
    if not 'robot' in phrase:
        return
    
    if 'navigation' in phrase:
        startNavigation = True
    
    for point in points:
        if point in phrase:
            print(point)
            #startNavigation = False
            point = points.index(point)
            pub1.publish(str(point + 1))
            rate.sleep()
    if 'go' in phrase:
        vx = 0
        vy = 0
        vz = 0 
        if 'north' in phrase:
            vx = 0.5
        if 'south' in phrase:
            vx = -0.5
        if 'west' in phrase:
            vy = -0.5
        if 'east' in phrase:
            vy = 0.5
        speeds.linear.x, speeds.linear.y, speeds.angular.z = vx, vy, vz
        pub3.publish(speeds)
        time.sleep(5)
        speeds.linear.x, speeds.linear.y, speeds.angular.z = 0, 0, 0
        pub3.publish(speeds)
    if 'rotate' in phrase:
        vx = 0
        vy = 0
        vz = 0 
        if 'clockwise' in phrase:
            vz = 0.5
        if 'counterclockwise' in phrase:
            vz = -0.5
        
        speeds.linear.x, speeds.linear.y, speeds.angular.z = vx, vy, vz
        pub3.publish(speeds)
        time.sleep(3)
        speeds.linear.x, speeds.linear.y, speeds.angular.z = 0, 0, 0
        pub3.publish(speeds)


    

sub = rospy.Subscriber('keyPhrases', String, callback)
rospy.loginfo("Voice Controler ready!")
rospy.spin()