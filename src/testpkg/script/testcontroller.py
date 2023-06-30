#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

moveBindings = {
        'w':(1,0,0),
        'e':(0,0,-1),
        'a':(0,1,0),
        'd':(0,-1,0),
        'q':(0,0,1),
        's':(-1,0,0),
           }

speedBindings={
        'u':(1.1,1),
        'n':(0.9,1),
        'i':(1,1.1),
        'm':(1,0.9)
          }

startstr="""
Controller:          linespeed   anguspped
        q w e           u(+)        i(+)
        a s d           n(-)        m(-)
exit: 0
"""


def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node("my_control")
    param = rospy.get_param('~id', '1')
    print("turtleid:",param)
    pub=rospy.Publisher(f"/turtle{param}/cmd_vel",Twist,queue_size=10)
    rate=rospy.Rate(1)
    linespeed=1
    anguspped=1
    
    print(startstr)
    while not rospy.is_shutdown():
        tw=Twist()
        
        key=getKey()
        if key in moveBindings.keys():
            # print(key)
            tw.linear.x=moveBindings[key][0]*linespeed
            tw.linear.y=moveBindings[key][1]*linespeed
            tw.angular.z=moveBindings[key][2]*anguspped
            # tw.angular.z = (lambda x: 0 if x == 0 else x + anguspped)(moveBindings[key][2])
        if key in speedBindings.keys():
            linespeed=linespeed*speedBindings[key][0]
            anguspped=anguspped*speedBindings[key][1]
            print("linespped:",linespeed,"-- anguspped:",anguspped)

        if key=="0":
            rospy.signal_shutdown('User requested node shutdown.')
        pub.publish(tw)
        # rate.sleep()

        