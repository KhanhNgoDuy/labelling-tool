import os.path
import time
import keyboard
import pandas

from shuffle_thread import ShuffleThread
from camera_thread import CameraThread
import utils


def create_annot(path):
    annot = {
        'label': utils.order_q.queue,
        'start': utils.start_q.queue,
        'end': utils.stop_q.queue
    }

    pandas.DataFrame(annot).to_csv(path)

    # with open(path, 'w') as f:
    #     for cls, start, stop, start_t, stop_t in zip(utils.order_q.queue, utils.start_q.queue, utils.stop_q.queue,
    #                                                  utils.start_time_q.queue, utils.stop_time_q.queue):
    #         print(f'{cls},{start},{stop},{start_t},{stop_t}')
    #         f.writelines(f'{cls},{start}\t{stop}\t{start_t}\t{stop_t}\n')


if __name__ == '__main__':
    # Đổi "src" thành ID của camera (tương tự cv2.VideoCapture(src))
    src = "rtsp://admin:comvis123@192.168.100.125:554/Streaming/Channels/102/"
    # src = "test_vid.mp4"
    # src = 1

    # Run threads
    utils.ButtonManager()
    ShuffleThread()
    CameraThread(src)

    name = str(input())

    while True:
        time.sleep(.01)

        if len(utils.start_q.queue) == utils.MAXSIZE and \
                len(utils.stop_q.queue) == utils.MAXSIZE and \
                len(utils.order_q.queue) == utils.MAXSIZE and \
                utils.toggle_var == 'stop':

            print('----- Name ID:', utils.name_id)
            name_id = name + utils.name_id
            utils.make_dir(name_id=name)
            path = os.path.join('data', str(name), str(name_id) + '.csv')
            create_annot(path)

            for q in utils.queues:
                q.queue.clear()

            time.sleep(0.5)
            utils.name_id += 1

        if keyboard.is_pressed('q'):
            print('[EXIT MAIN]')
            break
