#!/home/pi/.virtualenvs/robot/bin/python3
# -*- coding: utf-8 -*-
import rospy
from pocketsphinx import LiveSpeech, get_model_path
import rospy
from std_msgs.msg import String
model_path = "/home/pi/catkin_ws/src/audio/src/en-us/"
rospy.init_node('kws')
pub = rospy.Publisher('/keyPhrases', String, queue_size=10)
rate = rospy.Rate(1)
speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    # hmm='/home/pi/catkin_ws/src/3krug/model/en-us/en_us',
    # lm='/home/pi/catkin_ws/src/3krug/model/en-us/en-us.lm.bin',
    # dic='/../model/en-us/myDict.dict'
    hmm=rospy.get_param("~hmm"),
    lm=rospy.get_param("~lm"),
    dic=rospy.get_param("~dict")

)

while not rospy.is_shutdown():
    for phrase in speech:
        pub.publish(str(phrase))
        rate.sleep()
del speech
