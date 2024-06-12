import cv2 as cv
import numpy as np
from picamera2 import Picamera2


class ColorPicker:
    def __init__(self, camera_resolution) -> None:
        self.camera = Picamera2()
        self.camera.preview_configuration.main.size=(camera_resolution)
        self.width = camera_resolution[0]
        self.height = camera_resolution[1]

    @staticmethod
    def empty(x):
        pass

    def run(self) -> None:
        cv.namedWindow('panel')
        cv.resizeWindow('panel', 320, 240)
        cv.createTrackbar('lower_hue', 'panel', 0, 179, self.empty)
        cv.createTrackbar('upper_hue', 'panel', 255, 255, self.empty)
        cv.createTrackbar('lower_sat', 'panel', 0, 255, self.empty)
        cv.createTrackbar('upper_sat', 'panel', 255, 255, self.empty)
        cv.createTrackbar('lower_val', 'panel', 0, 255, self.empty)
        cv.createTrackbar('upper_val', 'panel', 255, 255, self.empty)
        self.camera.start()

        while True:
            frame = self.camera.capture_array()

            lower_hue = cv.getTrackbarPos('lower_hue', 'panel')
            upper_hue = cv.getTrackbarPos('upper_hue', 'panel')
            lower_sat = cv.getTrackbarPos('lower_sat', 'panel')
            upper_sat = cv.getTrackbarPos('upper_sat', 'panel')
            lower_val = cv.getTrackbarPos('lower_val', 'panel')
            upper_val = cv.getTrackbarPos('upper_val', 'panel')
            lower_value = np.array([lower_hue, lower_sat, lower_val])
            upper_value = np.array([upper_hue, upper_sat, upper_val])

            frame_hsv = cv.cvtColor(frame, cv.COLOR_RGB2HSV)
            masking = cv.inRange(frame_hsv, lower_value, upper_value)
            output = cv.bitwise_and(frame, frame, mask=masking)

            print(f"""
Lower:({lower_hue}, {lower_sat}, {lower_val})
Upper:({upper_hue}, {upper_sat}, {upper_val})
    """)

            cv.imshow('color', output)
            if cv.waitKey(1) & 0xFF == 27:
                break

        self.camera.stop()
        cv.destroyAllWindows()


if __name__ == '__main__':
    picker = ColorPicker((640, 480))
    picker.run()