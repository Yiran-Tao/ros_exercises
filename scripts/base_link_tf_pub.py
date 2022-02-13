#!/usr/bin/env python  
import rospy

import math
import tf2_ros
import geometry_msgs.msg
import turtlesim.srv
import numpy as np
from tf.transformations import quaternion_matrix, quaternion_from_matrix


if __name__ == '__main__':
    rospy.init_node('base_link_tf_pub')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    #rospy.loginfo(rospy.is_shutdown())
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('left_cam', 'world', rospy.Time())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):     
            rate.sleep()
            continue
        #rospy.loginfo(trans)
        # trans = tfBuffer.lookup_transform('left_cam', 'world', rospy.Time())
        translation = trans.transform.translation
        rotation = trans.transform.rotation
        
        matrix = quaternion_matrix([rotation.x, rotation.y, rotation.z, rotation.w])
        matrix[0,3] = translation.x
        matrix[1,3] = translation.y
        matrix[2,3] = translation.z
        
        left_base = np.array([[1,0,0,-0.05],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
        base_left = np.linalg.inv(left_base)
        
        base_world = np.matmul(matrix,base_left)
        
        br = tf2_ros.TransformBroadcaster()
        t1 = geometry_msgs.msg.TransformStamped()
    
        t1.header.stamp = rospy.Time.now()
        t1.header.frame_id = "world"
        t1.child_frame_id = 'base_link_gt_2'
        
        t1.transform.translation.x = base_world[0,3]
        t1.transform.translation.y = base_world[1,3]
        t1.transform.translation.z = base_world[2,3]   
        
        t1.transform.rotation.x = quaternion_from_matrix(base_world)[0]
        t1.transform.rotation.y = quaternion_from_matrix(base_world)[1]
        t1.transform.rotation.z = quaternion_from_matrix(base_world)[2]
        t1.transform.rotation.w = quaternion_from_matrix(base_world)[3]
    
        br.sendTransform(t1)

        
 