import threading
from threading import Thread

import keyboard
import cv2
import time
import os
import numbers

from random_video import VideoRandomizer
import utils


VIDEO_PATH = './clipped/'
DEFAULT_DELAY = 0


def shuffle_clips():
    playlist = VideoRandomizer().cls
    print(playlist)

    for video in playlist:
        if isinstance(video, str):
            time.sleep(DEFAULT_DELAY)
            path = os.path.join(VIDEO_PATH, video+'.mp4')
            cap = cv2.VideoCapture(path)

            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    cv2.imshow('Clip', frame)
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        cap.release()
                        cv2.destroyWindow('Clip')
                        break
                else:
                    cap.release()
                    break
        elif isinstance(video, numbers.Complex):
            try:
                cv2.destroyWindow('Clip')
            except cv2.error:
                pass
            time.sleep(video)


class ShuffleThread:
    def __init__(self):
        self.thread = Thread(target=self.shuffle, daemon=True, name='Shuffle Thread')
        self.thread.start()

    @staticmethod
    def shuffle():
        while True:
            keyboard.wait('space')
            if utils.toggle_var == 'start' \
                    or __name__ == '__main__':
                shuffle_clips()
                print('**** Finished ****')


