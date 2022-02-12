#!/usr/bin/env python
# license removed for brevity
from __future__ import division
import rospy
import random
from sensor_msgs.msg import LaserScan
import math

 
def publisher():    
    rospy.init_node('fake_scan_publisher')   
    
    publish_topic = rospy.get_param('publish topic', 'fake_scan')   
    publish_rate = rospy.get_param('publish rate', 20)
    angle_min = rospy.get_param('angle_min', -(2/3)*math.pi)
    angle_max = rospy.get_param('angle_max', (2/3)*math.pi)
    range_min = rospy.get_param('range_min', 1.0)
    range_max = rospy.get_param('range_max', 10.0)
    angle_increment = rospy.get_param('angle_increment', (1/300)*math.pi)
    
    pub = rospy.Publisher(publish_topic, LaserScan, queue_size=10)
    rate = rospy.Rate(publish_rate) 
    
    
    while not rospy.is_shutdown():
        ls = LaserScan()
        ls.header.stamp = rospy.Time.now()
        ls.header.frame_id = 'base_link'
        ls.angle_min = angle_min
        ls.angle_max = angle_max
        ls.angle_increment = angle_increment
        ls.scan_time = 1/20
        ls.range_min = range_min
        ls.range_max = range_max
        #length 401
        ranges = []
        length = (ls.angle_max - ls.angle_min)/ls.angle_increment+1
        length = int(length+0.1)
        #rospy.loginfo(rospy.has_param('publish_topic'))
        for i in range(length):            
            random_number = random.uniform(ls.range_min,ls.range_max)
            ranges.append(random_number)
        assert len(ranges)==length
        ls.ranges = ranges
        pub.publish(ls)
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
