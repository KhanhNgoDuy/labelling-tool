from multiprocessing import Process
# from threading import Thread

import keyboard
import cv2
import time
import os
import numbers

from random_video import VideoRandomizer
import utils


VIDEO_PATH = './clipped/'
DEFAULT_DELAY = 0


class ShuffleThread:
    def __init__(self, toggle_var, order_q):
        self.toggle_var = toggle_var
        self.order_q = order_q
        self.process = Process(target=self.shuffle, args=(), daemon=True)

    def shuffle(self):
        while True:
            time.sleep(0.5)
            if self.toggle_var.value == 'start':
                print('[Inside SHUFFLE]')
                self.shuffle_clips()
                print('**** Finished ****')
                keyboard.wait('space')

    def shuffle_clips(self):
        playlist = VideoRandomizer(self.order_q).cls
        print(playlist)

        for video in playlist:

            if isinstance(video, numbers.Complex):
                time.sleep(video)

            elif isinstance(video, str):
                time.sleep(DEFAULT_DELAY)
                path = os.path.join(VIDEO_PATH, video+'.mp4')
                cap = cv2.VideoCapture(path)

                while cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        cv2.imshow('Clip', frame)
                        cv2.waitKey(10)
                    else:
                        cv2.destroyWindow('Clip')
                        cap.release()
                        break