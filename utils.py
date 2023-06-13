import os
import time
import keyboard
# from queue import Queue
from multiprocessing import Queue, Value
from ctypes import c_wchar_p

import numpy as np

CLS_PATH = 'classes.txt'
MAXSIZE = 10

order_q = Queue(maxsize=MAXSIZE)
start_q = Queue(maxsize=MAXSIZE)
stop_q = Queue(maxsize=MAXSIZE)
queues = [order_q, start_q, stop_q]

name_id = Value('i', 1)
frame = Value('i', 0)


class ButtonManager:
    def __init__(self, toggle_var, frame, name_id, start_q, stop_q):
        self.toggle_var = toggle_var
        self.frame = frame
        self.name_id = name_id
        self.start_q = start_q
        self.stop_q = stop_q

        self.pre_space = False
        self.bind_key()

    def on_press_a(self):
        if not self.start_q.full():
            self.start_q.put(self.frame.value)

    def on_press_b(self):
        if not self.stop_q.full():
            self.stop_q.put(self.frame.value)

    def on_press_space(self):
        self.pre_space = not self.pre_space
        if self.pre_space:
            self.toggle_var.value = 'start'

        elif not self.pre_space:
            self.toggle_var.value = 'stop'
        print('From utils: ', self.toggle_var.value)
        print('-'*20)

    def bind_key(self):
        keyboard.add_hotkey('a', self.on_press_a)
        keyboard.add_hotkey('b', self.on_press_b)
        keyboard.add_hotkey('space', self.on_press_space)


def label2id(label_ls: list):
    d = {}
    id_ls = []
    with open(CLS_PATH, 'r') as f:
        for line in f:
            value, key = line.split()
            d.update({key: value})
    for label in label_ls:
        id_ls.append(d[label])
    return id_ls


if __name__ == '__main__':
    label_ls = []
    with open('classes.txt', 'r') as f:
        for line in f:
            label_ls.append(line.split()[1])
    np.random.shuffle(label_ls)
    id_ls = label2id(label_ls)
    for id, label in zip(id_ls, label_ls):
        print(f'{id}\t{label}')