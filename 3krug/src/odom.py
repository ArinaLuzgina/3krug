#!/usr/bin/python3
# coding: utf-8

import rospy
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import Odometry
import tf
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import time
import numpy as np

x, y, alpha = 0, 0, 0
vx, vy, vz = 0, 0, 0
rospy.init_node("odom3")
pub = rospy.Publisher("odom", Odometry, queue_size=50)

odom_broadcaster = tf.TransformBroadcaster()
current_time = rospy.Time.now()
last_time = rospy.Time.now()

r = rospy.Rate(1.0)

def changeVels(msg):
    global vx, vy, vz
    vels = []
    info = msg.data
    for i in range(0, 5, 2):
        if info[i + 1] == 1:
            vels.append(info[i])
        else:
            vels.append(info[i] * -1)
    vx, vy, vz = vels[0], vels[1], vels[2]
    print(vx, vy, vz)

    pass
def odomCalculator(vx, vy, vz, deltaT, x, y, alpha):
    dx, dy, dz = vx * deltaT, vy * deltaT, vz * deltaT
    v1 = (dy + dz) / 2
    v2 = (dx + dz) / 2
    v3 = (dy + dx) / 2
    O1 = np.pi/6
    x += (v1 - v2 * np.sin(O1) - v3 * np.sin(O1))
    y += (v2 - v3) * np.cos(O1)
    alpha += (dx + dy + dz) / 3

    odom_quat = tf.transformations.quaternion_from_euler(0, 0, alpha)
    odom_broadcaster.sendTransform(
        (x, y, 0.),
        odom_quat,
        current_time,
        "base_link",
        "odom"
    )

    # next, we'll publish the odometry message over ROS
    odom = Odometry()
    odom.header.stamp = current_time
    odom.header.frame_id = "odom"

    # set the position
    odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))

    # set the velocity
    odom.child_frame_id = "base_link"
    odom.twist.twist = Twist(Vector3(vx, vy, 0), Vector3(0, 0, vz))

    # publish the message
    pub.publish(odom)

    last_time = current_time
    r.sleep()
    return (x, y, alpha)

sub = rospy.Subscriber("speed_publisher", Float32MultiArray, changeVels)
odom = Odometry()

rospy.loginfo("Odom calculator ready!")
deltaT = 1
timeNow = time.time()

while not rospy.is_shutdown():
    if time.time() - timeNow >= deltaT:
        timePer = time.time() - timeNow
        timeNow = timePer + timeNow
        print(vx, vy, vz)
        x, y, alpha = odomCalculator(vx, vy, vz, timePer, x, y, alpha)
    r.sleep()
    pass




# def callback(msg):
    # global x, y, alpha
    # ticks = msg.data
    # rospy.loginfo(list(map(int, ticks)))
    # ticksPerMeter = 7719
    # radious = 0.11
    # dxT = (ticks[0] + ticks[1]) / 2
    # dyT = (ticks[0] - ticks[2]) / 2
    # dwT = (ticks[0] + ticks[1] + ticks[2]) / 3
    # dx = dxT / ticksPerMeter
    # dy = dyT / ticksPerMeter
    # dalpha = dwT / ticksPerMeter / radious

    # dt = 50 * 10 **(-3)
    # dvx = dx / dt
    # dvy = dy / dt
    # dW = dalpha / dt
    # x += dx
    # y += dy
    # alpha += dalpha
    # odom_quat = tf.transformations.quaternion_from_euler(0, 0, alpha)
    # odom_broadcaster.sendTransform(
    #     (x, y, 0.),
    #     odom_quat,
    #     current_time,
    #     "base_link",
    #     "odom"
    # )

    # # next, we'll publish the odometry message over ROS
    # odom = Odometry()
    # odom.header.stamp = current_time
    # odom.header.frame_id = "odom"

    # # set the position
    # odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))

    # # set the velocity
    # odom.child_frame_id = "base_link"
    # odom.twist.twist = Twist(Vector3(dvx, dvy, 0), Vector3(0, 0, dW))

    # # publish the message
    # pub.publish(odom)

    # last_time = current_time
    # r.sleep()
