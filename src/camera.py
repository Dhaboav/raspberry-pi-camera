import cv2
import numpy as np
from picamera2 import Picamera2


def main():
    camera = Picamera2()
    camera.preview_configuration.main.size=(640,480)
    camera.preview_configuration.main.format='RGB888'
    camera.start()

    lower_value = np.array([85, 109, 0])
    upper_value = np.array([118, 255, 255])

    while True:
        frame = camera.capture_array()
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        masking = cv2.inRange(frame_hsv, lower_value, upper_value)
        output = cv2.bitwise_and(frame, frame, mask=masking)
        cv2.imshow('Test', output)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    camera.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()