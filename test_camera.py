import cv2
from typing import TypeVar


T_VideoCapture = TypeVar('cv2.VideoCapture')


CAMERA = {
    'name'   : 'Logitech C920',
    'device' : '/dev/video0',
    'height' : 720,
    'width'  : 1080,
    'fps'    : 30
}


def configure_camera() -> T_VideoCapture:
    cap = cv2.VideoCapture(CAMERA['device'])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA['width'])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA['height'])
    cap.set(cv2.CAP_PROP_FPS, CAMERA['fps'])
    return cap


def capture(cap, filename : str) -> None:
    success, frame = cap.read()

    cv2.imwrite(filename, frame)


if __name__ == '__main__':
    cap = configure_camera()
    capture(cap, 'image.jpg')
