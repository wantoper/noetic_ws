#! /usr/bin/env python3

import rospy,tf
import turtlesim.srv,turtlesim.msg

class TF_Follow():
    def __init__(self) -> None:
        self.br=tf.TransformBroadcaster()
        
        # spawner=rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
        # spawner(4,2,0,"turtle2")
        
        rospy.Subscriber("/turtle1/pose",
                         turtlesim.msg.Pose,
                         self.turtlecallback,"turtle1")
        rospy.Subscriber("/turtle2/pose",
                         turtlesim.msg.Pose,
                         self.turtlecallback,"turtle2")
        
    def turtlecallback(self,pose,name):
        self.br.sendTransform((pose.x,pose.y,0),
                              tf.transformations.quaternion_from_euler(0, 0, pose.theta),
                              rospy.Time.now(),
                              name,
                              "world")


if __name__ == "__main__":
    rospy.init_node("turtle_tf")
    TF_Follow()
    rospy.spin()