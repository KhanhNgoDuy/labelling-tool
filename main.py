import os.path
import time
import keyboard

from shuffle_thread import ShuffleThread
from camera_thread import CameraThread
import utils


def create_annot(path):
    with open(path, 'w') as f:
        for cls, start, stop, start_t, stop_t in zip(utils.order_q.queue, utils.start_q.queue, utils.stop_q.queue,
                                                     utils.start_time_q.queue, utils.stop_time_q.queue):
            print(f'{cls}\t{start}\t{stop}\t{start_t}\t{stop_t}')
            f.writelines(f'{cls}\t{start}\t{stop}\t{start_t}\t{stop_t}\n')


if __name__ == '__main__':
    # Đổi "src" thành ID của camera (tương tự cv2.VideoCapture(src))
    # src = "rtsp://admin:comvis123@192.168.100.125:554/Streaming/Channels/101/"
    src = "test_vid.mp4"
    # src = 0

    # Run threads
    utils.ButtonManager()
    ShuffleThread()
    CameraThread(src)

    while True:
        time.sleep(.01)

        if len(utils.start_q.queue) == utils.MAXSIZE and \
                len(utils.stop_q.queue) == utils.MAXSIZE and \
                len(utils.order_q.queue) == utils.MAXSIZE and \
                utils.toggle_var == 'stop':

            print('----- Name ID:', utils.name_id)
            utils.make_dir(name_id=utils.name_id)
            path = os.path.join('data', str(utils.name_id), str(utils.name_id) + '.txt')
            create_annot(path)

            for q in utils.queues:
                q.queue.clear()

            time.sleep(0.5)
            utils.name_id += 1

        if keyboard.is_pressed('q'):
            print('[EXIT MAIN]')
            break
