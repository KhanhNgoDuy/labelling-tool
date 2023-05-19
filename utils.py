import os
import time
from queue import Queue
import keyboard
from datetime import datetime
import json


with open('config.json', 'r') as f:
    json_data = json.load(f)
    name_id = json_data['name_id']
    MAXSIZE = json_data['MAXSIZE']

toggle_var = None
frame = 0
start_time = time.perf_counter()

order_q = Queue(maxsize=MAXSIZE)
start_q = Queue(maxsize=MAXSIZE)
stop_q = Queue(maxsize=MAXSIZE)
start_time_q = Queue(maxsize=MAXSIZE)
stop_time_q = Queue(maxsize=MAXSIZE)
queues = [order_q, start_q, stop_q, start_time_q, stop_time_q]


class ButtonManager:
    def __init__(self):
        self.keys = []
        self.pre_space = False
        self.bind_key()

    def on_press_a(self):
        if not start_q.full():
            start_q.put(frame)
            start_time_q.put(datetime.now())

    def on_press_b(self):
        if not stop_q.full():
            stop_q.put(frame)
            stop_time_q.put(datetime.now())

    def on_press_space(self):
        global toggle_var, start_time, name_id
        self.pre_space = not self.pre_space

        if self.pre_space:
            toggle_var = 'start'
            start_time = time.perf_counter()

        elif not self.pre_space:
            toggle_var = 'stop'
            # print('utils - frame ', frame)

        print('-'*20)

    def bind_key(self):
        keyboard.add_hotkey('a', self.on_press_a)
        keyboard.add_hotkey('b', self.on_press_b)
        keyboard.add_hotkey('space', self.on_press_space)


def make_dir(name_id):
    _dir = os.path.join('data', str(name_id))
    if not os.path.exists(_dir):
        os.makedirs(_dir)

