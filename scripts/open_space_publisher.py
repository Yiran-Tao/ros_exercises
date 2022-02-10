#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
import math
import operator
from sensor_msgs.msg import LaserScan
from ros_exercises.msg import OpenSpace

    
def callback(data):
    # pub1 = rospy.Publisher('open_space/distance', Float32, queue_size=10)
    # pub2 = rospy.Publisher('open_space/angle', Float32, queue_size=10)
    pub = rospy.Publisher('open_space', OpenSpace, queue_size=10)
    rate = rospy.Rate(20) 
   
    ranges = data.ranges
    angle_min = data.angle_min
    angle_max = data.angle_max
    angle_increment = data.angle_increment
    max_index, max_range = max(enumerate(ranges), key=operator.itemgetter(1))
    max_angle = angle_min + (angle_increment * max_index)
    
    ops = OpenSpace()
    ops.angle = max_angle
    ops.distance = max_range
    # rospy.loginfo(max_range)
    # pub1.publish(max_range)
    # rospy.loginfo(max_angle)
    # pub2.publish(max_angle)
    rospy.loginfo(ops)
    pub.publish(ops)
    rate.sleep()
        
    
def listener():

    rospy.init_node('open_space_publisher', anonymous=True)

    rospy.Subscriber("fake_scan", LaserScan, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
