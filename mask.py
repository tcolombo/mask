import cv2
from typing import TypeVar
import numpy
import requests
import sys
from PyInquirer import prompt


T_VideoCapture = TypeVar('cv2.VideoCapture')
T_ndarray = TypeVar('numpy.ndarray')


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


def get_mask(frame : T_ndarray, bodypix_service : str = 'http://localhost:9000') -> T_ndarray:
    _, data = cv2.imencode('.jpg', frame)
    req = requests.post(
        url = bodypix_service,
        data = data.tobytes(),
        headers = {'Content-Type' : 'application/octet-stream'}
    )

    mask = numpy.frombuffer(req.content, dtype=numpy.uint8)
    mask = mask.reshape((frame.shape[0], frame.shape[1]))

    return mask


def capture(cap, filename : str) -> None:
    success, frame = cap.read()
    mask = get_mask(frame)

    width, height = 960, 720

    inv_mask = 1 - mask
    for c in range(frame.shape[2]):
        frame[:, :, c] = frame[:, :, c] * mask

    cv2.imwrite(filename, frame)


if __name__ == '__main__':
    cap = configure_camera()
    capture(cap, 'image.jpg')
