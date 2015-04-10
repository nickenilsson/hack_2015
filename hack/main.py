import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import sys
sys.path.insert(0, "lib")
import Leap
import pyglet


import time

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture, Vector

x_chord_line_left = -50
x_chord_line_right = 50
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
            left_hand = hands.leftmost
            pitch = left_hand.palm_position.x

            if pitch > x_chord_line_right:
                file_path = "c.wav"
            elif pitch < x_chord_line_left:
                file_path = "d.wav"
            else:
                file_path = "e.wav"
            # print "Force: %s" % right_hand.palm_velocity.y
            music = pyglet.resource.media(file_path)
            music.play()
            pyglet.app.run()

        # print "Tone : %s" % pitch
        # print "Frame available"

def main():

     # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
	main()