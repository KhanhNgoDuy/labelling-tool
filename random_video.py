import numpy as np

MIN_INSERTION = 5
MAX_INSERTION = 10
MIN_DURATION = 2
MAX_DURATION = 5


class RandomVideo:
    def __init__(self):
        with open('classes.txt', 'r') as f:
            self.cls = f.read().split()
            self.random_indexing()
            # self.mini_insertion()
            self.random_insertion()

    def random_indexing(self):
        np.random.shuffle(self.cls)

    def mini_insertion(self):
        length = len(self.cls)
        for i in range(length):
            self.cls.insert(length-i, self.mini_delay)

    def random_insertion(self):
        num_insertion = np.random.randint(1, MAX_INSERTION)

        idx = np.arange(len(self.cls))
        np.random.shuffle(idx)
        idx = idx[: num_insertion]

        for i in idx:
            self.cls.insert(i, self.random_delay)

    @property
    def random_delay(self):
        return np.random.randint(1, MAX_DURATION)

    @property
    def mini_delay(self):
        return np.random.rand()


if __name__ == '__main__':
    cls = RandomVideo().cls
    print(cls)