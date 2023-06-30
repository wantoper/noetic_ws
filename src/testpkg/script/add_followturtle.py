#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import tf,sys, select, termios, tty
import turtlesim.srv,turtlesim.msg
import math

class my_follow():
    
    def __init__(self):
        self.turtle2pose = None
        rospy.Subscriber("/turtle2/pose",
                        turtlesim.msg.Pose,
                        self.handle_turtle2_pose,
                        "turtle2")
        self.pub=rospy.Publisher(f"/turtle2/cmd_vel",Twist,queue_size=10)
        rospy.Subscriber("/turtle1/pose",
                        turtlesim.msg.Pose,
                        self.handle_turtle_pose,
                        "turtle1")
        
        spawner=rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
        spawner(4,2,0,"turtle2")
    
    def handle_turtle_pose(self,msg, turtlename):
        # br=tf.TransformBroadcaster()
        # br.sendTransform((msg.x,msg.y,0),
        #                  tf.transformations.quaternion_from_euler(0, 0, msg.theta),
        #                  rospy.Time.now(),
        #                  turtlename,
        #                  "word")
        if self.turtle2pose is not None:
            dx = msg.x - self.turtle2pose.x
            dy = msg.y - self.turtle2pose.y
            
            angular = 4 * (math.atan2(dy,dx) - self.turtle2pose.theta)
            linear = 0.5 * math.sqrt(dy ** 2 + dx ** 2)
            tw = Twist()
            tw.angular.z = angular
            tw.linear.x = linear
            # print(round(dx, 0.2),round(dy, 0.2),round(angular, 0.2),round(linear, 0.2))
            print(dx,dy,angular,linear)
            self.pub.publish(tw)
        
    def handle_turtle2_pose(self,msg, turtlename):
        self.turtle2pose=msg


if __name__ =="__main__":
    rospy.init_node("follow_turtle")
    my_follow()
    rospy.spin()