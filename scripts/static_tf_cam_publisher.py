#!/usr/bin/env python
import rospy
import tf2_ros
import geometry_msgs.msg
import numpy as np
from tf.transformations import quaternion_from_matrix

if __name__ == '__main__':
 
        rospy.init_node('static_tf_cam_publisher')
        broadcaster = tf2_ros.StaticTransformBroadcaster()
        sts1 = geometry_msgs.msg.TransformStamped()
        sts2 = geometry_msgs.msg.TransformStamped()
        
        
        left_base = np.array([[1,0,0,-0.05],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
        right_base = np.array([[1,0,0,0.05],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

        sts1.header.stamp = rospy.Time.now()
        sts2.header.stamp = rospy.Time.now()
        sts1.header.frame_id = "base_link_gt"
        sts2.header.frame_id = "base_link_gt"
        sts1.child_frame_id = "left_cam"
        sts2.child_frame_id = "right_cam"

        sts1.transform.translation.x = left_base[0,3]
        sts1.transform.translation.y = left_base[1,3]
        sts1.transform.translation.z = left_base[2,3]
        sts2.transform.translation.x = right_base[0,3]
        sts2.transform.translation.y = right_base[1,3]
        sts2.transform.translation.z = right_base[2,3]

        
        sts1.transform.rotation.x = quaternion_from_matrix(left_base)[0]
        sts1.transform.rotation.y = quaternion_from_matrix(left_base)[1]
        sts1.transform.rotation.z = quaternion_from_matrix(left_base)[2]
        sts1.transform.rotation.w = quaternion_from_matrix(left_base)[3]
        sts2.transform.rotation.x = quaternion_from_matrix(right_base)[0]
        sts2.transform.rotation.y = quaternion_from_matrix(right_base)[1]
        sts2.transform.rotation.z = quaternion_from_matrix(right_base)[2]
        sts2.transform.rotation.w = quaternion_from_matrix(right_base)[3]

        broadcaster.sendTransform(sts1)
        broadcaster.sendTransform(sts2)
        
        
        rospy.spin()