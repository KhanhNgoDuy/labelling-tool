import os.path
import time
import queue
import pandas

import keyboard

from shuffle_thread import ShuffleThread
from camera_thread import CameraThread, SpinCamThread
import utils


def create_annot(path):
    annotation = {
        # 'ID': utils.ID,
        'label': utils.order_q.queue,
        'start': utils.start_q.queue,
        'stop': utils.stop_q.queue
    }

    df = pandas.DataFrame(annotation)
    print(df)
    df.to_csv(path)


if __name__ == '__main__':

    # Đổi "src" thành ID của camera (tương tự cv2.VideoCapture(src))
    # src = "rtsp://admin:comvis123@192.168.100.125/Streaming/Channels/102"
    src = 0

    name = input('Enter subject name: ')

    # Run threads
    utils.ButtonManager()
    ShuffleThread()
    # CameraThread(name=name, src=src)
    SpinCamThread(name=name)

    while True:
        time.sleep(.001)

        if (len(utils.start_q.queue) == utils.MAXSIZE and
                len(utils.stop_q.queue) == utils.MAXSIZE and
                len(utils.order_q.queue) == utils.MAXSIZE):

            print('--- Name ID:', utils.name_id)
            utils.make_dir(name=name)
            path = os.path.join('data', name, f'{name}_{str(utils.name_id)}' + '.csv')
            create_annot(path)

            for q in utils.queues:
                q.queue.clear()

            time.sleep(1)
            utils.name_id += 1

        if keyboard.is_pressed('q'):
            print('[EXIT MAIN]')
            break
