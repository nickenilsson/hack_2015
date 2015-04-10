import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import sys
sys.path.insert(0, "lib")
import Leap

import time

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture, Vector



y_strumming_line = 200

class SampleListener(Leap.Listener):
    def on_connect(self, controller):
        print "Connected"


    def on_frame(self, controller):
    	current_frame = controller.frame()
    	hands = current_frame.hands

        right_hand = hands.rightmost

        previous_frame = controller.frame(1)
        previous_y = previous_frame.hands.rightmost.palm_position.y
        if ((previous_y > y_strumming_line) and (right_hand.palm_position.y < y_strumming_line)) or ((previous_y < y_strumming_line) and (right_hand.palm_position.y > y_strumming_line)):
            print "STRUM"
            print "Force: %s" % right_hand.palm_velocity.y
            time.sleep(.1)

        left_hand = hands.leftmost
        pitch = left_hand.palm_position.x
        print "Tone : %s" % pitch
        print "Frame available"

def main():

     # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)

    controller.config.set("Gesture.Swipe.MinVelocity", 500)


    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
	main()