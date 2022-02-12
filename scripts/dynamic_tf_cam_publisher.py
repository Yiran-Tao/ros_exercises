#!/usr/bin/env python  
import rospy

import math
import tf2_ros
import geometry_msgs.msg
import turtlesim.srv
import numpy as np
from tf.transformations import quaternion_matrix, quaternion_from_matrix


if __name__ == '__main__':
    rospy.init_node('listener')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    #rospy.loginfo(rospy.is_shutdown())
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('base_link_gt', 'world', rospy.Time(0))
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            continue
        translation = trans.transform.translation
        rotation = trans.transform.rotation
        
        matrix = quaternion_matrix([rotation.x, rotation.y, rotation.z, rotation.w])
        matrix[0,3] = translation.x
        matrix[1,3] = translation.y
        matrix[2,3] = translation.z
        
        left_base = np.array([[1,0,0,-0.05],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
        right_base = np.array([[1,0,0,0.05],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
        
        left_world = np.matmul(matrix,left_base)
        right_world = np.matmul(matrix,right_base)
        
        br = tf2_ros.TransformBroadcaster()
        t1 = geometry_msgs.msg.TransformStamped()
        t2 = geometry_msgs.msg.TransformStamped()
    
        t1.header.stamp = rospy.Time.now()
        t2.header.stamp = rospy.Time.now()
        t1.header.frame_id = "world"
        t2.header.frame_id = "world"
        t1.child_frame_id = 'left_cam'
        t2.child_frame_id = 'right_cam'
        
        t1.transform.translation.x = left_world[0,3]
        t1.transform.translation.y = left_world[1,3]
        t1.transform.translation.z = left_world[2,3]        
        t2.transform.translation.x = right_world[0,3]
        t2.transform.translation.y = right_world[1,3]
        t2.transform.translation.z = right_world[2,3]
        
        t1.transform.rotation.x = quaternion_from_matrix(left_world)[0]
        t1.transform.rotation.y = quaternion_from_matrix(left_world)[1]
        t1.transform.rotation.z = quaternion_from_matrix(left_world)[2]
        t1.transform.rotation.w = quaternion_from_matrix(left_world)[3]
        t2.transform.rotation.x = quaternion_from_matrix(right_world)[0]
        t2.transform.rotation.y = quaternion_from_matrix(right_world)[1]
        t2.transform.rotation.z = quaternion_from_matrix(right_world)[2]
        t2.transform.rotation.w = quaternion_from_matrix(right_world)[3]
    
        br.sendTransform(t2)
        br.sendTransform(t1)
        

        
        