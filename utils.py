import os
import time
from queue import Queue
import keyboard

MAXSIZE = 5z
start_time = time.perf_counter()

order_q = Queue(maxsize=MAXSIZE)
start_q = Queue(maxsize=MAXSIZE)
stop_q = Queue(maxsize=MAXSIZE)
queues = [order_q, start_q, stop_q]

toggle_var = None
name_id = 1
frame = 0


class ButtonManager:
    def __init__(self):
        self.keys = []
        self.pre_space = False
        self.bind_key()

    @staticmethod
    def on_press_a():
        if not start_q.full():
            start_q.put(frame)

    @staticmethod
    def on_press_b():
        if not stop_q.full():
            stop_q.put(frame)

    def on_press_space(self):
        global toggle_var, start_time
        self.pre_space = not self.pre_space
        if self.pre_space:
            toggle_var = 'start'

        elif not self.pre_space:
            toggle_var = 'stop'

        print('-'*20)

    def bind_key(self):
        keyboard.add_hotkey('a', self.on_press_a)
        keyboard.add_hotkey('b', self.on_press_b)
        keyboard.add_hotkey('space', self.on_press_space)


def make_dir(name):
    _dir = os.path.join('data', str(name))
    if not os.path.exists(_dir):
        os.makedirs(_dir)

