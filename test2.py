import time
from utils import gv
import test
from test import p, p1


if __name__ == '__main__':
    # p.start()
    p1.start()
    while True:
        time.sleep(1)
        print('From main:', gv.order_q.ptr.value)
