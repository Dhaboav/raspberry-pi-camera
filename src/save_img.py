import os
import cv2
from picamera2 import Picamera2


folder_path =  os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img_dataset')
capture_count = 0

def save_img(img):
    global capture_count
    file_name = f'img-{capture_count}.jpg'
    save_img = os.path.join(folder_path, file_name)
    cv2.imwrite(save_img, img)
    capture_count += 1

def main():
    camera = Picamera2()
    camera.preview_configuration.main.size=(640,480)
    camera.preview_configuration.main.format='RGB888'
    camera.start()

    while True:
        frame = camera.capture_array()
        show_frame = frame.copy()
        cv2.putText(show_frame, f'{capture_count}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
        cv2.imshow('Take Img', show_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 13:
            save_img(frame)
        if key == 27:
            break

    camera.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()