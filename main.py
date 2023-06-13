import os.path
from pathlib import Path
import time
import queue
from ctypes import c_wchar_p
from multiprocessing import Value, Manager
import pandas
import keyboard

from shuffle_thread import ShuffleThread
from camera_thread import CameraThread, SpinCamThread
import utils


def create_annot(path):
    label = []
    start = []
    stop = []

    for i in range(utils.MAXSIZE):
        label.append(utils.order_q.get_nowait())
        start.append(utils.start_q.get_nowait())
        stop.append(utils.stop_q.get_nowait())
    ID = utils.label2id(label)

    annotation = {
        'ID': ID,
        'label': label,
        'start': start,
        'stop': stop
    }
    df = pandas.DataFrame(annotation)
    print(df)
    df.to_csv(path)


if __name__ == '__main__':
    src = 0
    name = input('Enter subject name: ')
    toggle_var = Manager().Value(c_wchar_p, None)

    # Run threads
    utils.ButtonManager(
        toggle_var,
        utils.frame,
        utils.name_id,
        utils.start_q,
        utils.stop_q
    )
    ShuffleThread(toggle_var, utils.order_q).process.start()
    camera_thread = CameraThread(name=name, toggle_var=toggle_var, src=src)
    # SpinCamThread(name=name)

    while True:
        time.sleep(.1)
        if (utils.start_q.full() and
                utils.stop_q.full() and
                utils.order_q.full()):

            print('--- Name ID:', utils.name_id.value)
            Path('data/' + name).mkdir(parents=True, exist_ok=True)
            path = os.path.join('data', name, f'{name}_{str(utils.name_id.value)}' + '.csv')
            create_annot(path)

            for q in utils.queues:
                while not q.empty():
                    q.get_nowait()

            time.sleep(1)
            utils.name_id.value += 1

        if keyboard.is_pressed('q'):
            print('[EXIT MAIN]')
            break
