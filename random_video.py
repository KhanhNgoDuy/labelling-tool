import queue
import random
import numpy as np
import utils


MIN_INSERTION = 5
MAX_INSERTION = 10
MIN_DURATION = 2
MAX_DURATION = 5


class VideoRandomizer:
    def __init__(self, order_q):
        self.cls = self.get_video_list()
        self.random_indexing()

        for cls in self.cls:
            order_q.put_nowait(cls)
        # self.mini_insertion()
        self.random_insertion()

    @staticmethod
    def get_video_list():
        cls = []
        with open(utils.CLS_PATH, 'r') as f:
            for line in f:
                cls.append(line.split()[1])
        cls = cls[:utils.MAXSIZE]
        return cls

    def random_indexing(self):
        np.random.shuffle(self.cls)

    def random_insertion(self):
        num_insertion = np.random.randint(MIN_INSERTION, MAX_INSERTION)
        idx = random.sample(range(0, utils.MAXSIZE), num_insertion)
        idx = sorted(idx, reverse=True)
        sleep_arr = np.random.randint(low=MIN_DURATION, high=MAX_DURATION, size=num_insertion)

        for i in range(num_insertion):
            self.cls.insert(idx[i], sleep_arr[i])

    def mini_insertion(self):
        for i in range(len(self.cls)):
            self.cls.insert(len(self.cls)-i, self.mini_delay)

    @property
    def random_delay(self):
        return np.random.randint(1, MAX_DURATION)

    @property
    def mini_delay(self):
        return np.random.rand()


if __name__ == '__main__':
    cls = VideoRandomizer().cls
    while not utils.order_q.empty():
        print(utils.order_q.get())
