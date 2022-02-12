#!/usr/bin/env python
# license removed for brevity
from __future__ import division
import rospy
import random
from sensor_msgs.msg import LaserScan
import math

 
def publisher():
    pub = rospy.Publisher('fake_scan', LaserScan, queue_size=10)
    rospy.init_node('fake_scan_publisher', anonymous=True)
    rate = rospy.Rate(20) 
    while not rospy.is_shutdown():
        ls = LaserScan()
        ls.header.stamp = rospy.Time.now()
        ls.header.frame_id = 'base_link'
        ls.angle_min = -(2/3)*math.pi
        ls.angle_max = (2/3)*math.pi
        ls.angle_increment = (1/300)*math.pi
        ls.scan_time = 1/20
        ls.range_min = 1.0
        ls.range_max = 10.0
        #length 401
        ranges = []
        for i in range(401):            
            random_number = random.uniform(1.0,10.0)
            ranges.append(random_number)
        assert len(ranges)==401
        ls.ranges = ranges
        pub.publish(ls)
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
