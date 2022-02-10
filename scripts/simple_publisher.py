#!/usr/bin/env python
# license removed for brevity
import rospy
import random
from std_msgs.msg import Float32
 
def publisher():
    pub = rospy.Publisher('my_random_float', Float32, queue_size=10)
    rospy.init_node('simple_publisher', anonymous=True)
    rate = rospy.Rate(20) 
    while not rospy.is_shutdown():
        random_number = random.uniform(0,10)
        rospy.loginfo(random_number)
        pub.publish(random_number)
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
