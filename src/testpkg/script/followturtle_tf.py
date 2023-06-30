#! /usr/bin/env python3

import rospy,tf,math
import turtlesim.srv,turtlesim.msg,geometry_msgs,geometry_msgs.msg


class TF_Follow():
    def __init__(self) -> None:
        self.listener=tf.TransformListener()
    
        # spawner=rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
        # spawner(4,2,0,"turtle2")
        
        self.pub=rospy.Publisher("turtle2/cmd_vel",geometry_msgs.msg.Twist,queue_size=1)

        rate=rospy.Rate(10)
        while not rospy.is_shutdown():
            try:            
                (trans,rot) = self.listener.lookupTransform('/turtle2', '/turtle1', rospy.Time(0))
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
            angular = 4 * math.atan2(trans[1], trans[0])
            linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
            tw = geometry_msgs.msg.Twist()
            tw.linear.x = linear
            tw.angular.z = angular
            self.pub.publish(tw)
            rate.sleep()


if __name__ == "__main__":
    rospy.init_node("followturtle_tf")
    TF_Follow()
    rospy.spin()