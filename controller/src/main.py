import sys, requests

sys.path.insert(0, "../lib")
import Leap
import sendkeys
import win32api

def send_cmd(cmd):
    r = requests.get("http://192.168.78.1:3000/?cmd="+cmd)
    print r.content

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    flag = {"direction": -1, "count": 0, "swipe_starttime": 0, "swipe_lastendtime": 0, "last_direction": -1}
    volume_flag = {"volume": 0, "volume_lastendtime": 0, "volume_starttime": 0, "last_diretion": -1}
    min_during_time = 1330000
    min_same_direction_time = 200000
    swipe_min_frames = 2
    swipe_volume_min_frames = 4
    swipe_min_delta_y = 0.3

    mouse_draw_speed_x_multiply = 14.872727
    mouse_draw_speed_y_multiply = 20.266666
    mouse_speed_x_multiply = 85.4
    mouse_speed_y_multiply = 40.4

    is_mouse_controlled = False
    mousebegin = True
    width = 0
    height = 0
    xpos = 0
    ypos = 0

    is_pen_valid = -1

    def on_init(self, controller):
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        #controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.config.set("Gesture.Swipe.MinLength", 100.0)
        controller.config.set("Gesture.Swipe.MinVelocity", 160.0)

        #controller.config.set("Gesture.KeyTap.MinDownVelocity", 1.0)
        #controller.config.set("Gesture.KeyTap.HistorySeconds", 1.0)
        #controller.config.set("Gesture.KeyTap.MinDistance", 0.1)

        controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
        controller.config.save()

        self.width = win32api.GetMonitorInfo(win32api.EnumDisplayMonitors(None, None)[0][0])["Monitor"][2]
        self.height = win32api.GetMonitorInfo(win32api.EnumDisplayMonitors(None, None)[0][0])["Monitor"][3]
        print self.width, self.height
        self.xpos = int(self.width / 2)
        self.ypos = int(self.height / 2)


        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
              #frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        gestures = frame.gestures()
        righthand = frame.hands.rightmost
        pinky_position = righthand.fingers[4].bone(Leap.Bone.TYPE_DISTAL).center
        ring_position = righthand.fingers[3].bone(Leap.Bone.TYPE_DISTAL).center
        finger_position = righthand.fingers[1].bone(Leap.Bone.TYPE_DISTAL).center
        hand_position = righthand.palm_position

        is_fisting = (0.0 < point_distance(ring_position, hand_position) < 45.0 and 0.0 < point_distance(pinky_position,
                                                                                              hand_position) < 45.0)


        for gesture in gestures:
            if not self.is_mouse_controlled:
                if gesture.type is Leap.Gesture.TYPE_SWIPE:
                    swipe = Leap.SwipeGesture(gesture)
                    swipe_direction = swipe.direction
                    swipe_pointable = swipe.pointable
                    swipe_speed = swipe.speed
                    if swipe_direction.x > 0 and abs(swipe_direction.y) < self.swipe_min_delta_y:
                        self.flag["direction"] = 0
                        self.flag["count"] += 1
                        if self.flag["swipe_starttime"] == 0: self.flag["swipe_starttime"] = frame.timestamp
                    elif swipe_direction.x < 0 and abs(swipe_direction.y) < self.swipe_min_delta_y:
                        self.flag["direction"] = 1
                        self.flag["count"] += 1
                        if self.flag["swipe_starttime"] == 0: self.flag["swipe_starttime"] = frame.timestamp


        if len(gestures) == 0:
            if self.flag["direction"] == 1 and (self.flag["swipe_starttime"] - self.flag["swipe_lastendtime"] > self.min_during_time or (self.flag["last_direction"] == 1 and self.flag["swipe_starttime"] - self.flag["swipe_lastendtime"] > self.min_same_direction_time)):
                send_cmd("c0_01")
                self.flag["swipe_lastendtime"] = frame.timestamp
                self.flag["last_direction"] = 1
            elif self.flag["direction"] == 0 and (self.flag["swipe_starttime"] - self.flag["swipe_lastendtime"] > self.min_during_time or (self.flag["last_direction"] == 0 and self.flag["swipe_starttime"] - self.flag["swipe_lastendtime"] > self.min_same_direction_time)):
                send_cmd("c0_02")
                self.flag["swipe_lastendtime"] = frame.timestamp
                self.flag["last_direction"] = 0

            self.flag["count"] = 0
            self.flag["direction"] = -1
            self.flag["swipe_starttime"] = 0

def point_distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2) ** 0.5

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
