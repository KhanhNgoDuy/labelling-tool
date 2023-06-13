import os.path
from pathlib import Path

import cv2
import keyboard
import utils
import time
from threading import Thread
from multiprocessing import Queue

import PySpin


class CameraThread:
    def __init__(self, name, toggle_var, src=0):

        self.cap = cv2.VideoCapture(src)
        print('================== READY ==================')
        self.name_id = name
        self.toggle_var = toggle_var

        Path('data/' + self.name_id).mkdir(parents=True, exist_ok=True)
        self.path = os.path.join('data', self.name_id, f'{self.name_id}_{str(utils.name_id.value)}' + '.mp4')

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(self.path, self.fourcc, 25.0,
                                      (int(self.cap.get(3)), int(self.cap.get(4)) - 40))

        self.cam_thread = Thread(target=self.run, daemon=True, name='Cam_Thread')
        self.cam_thread.start()
        keyboard.add_hotkey('space', self.toggle)
        self.is_running = False

    def run(self):

        start_time = time.time()
        frame_count = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print('[ERROR] Missing frames ...')
                continue
            annotated_frame = frame.copy()

            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            annotated_frame = cv2.putText(annotated_frame, str(utils.frame.value), (250, 70), font,
                                          fontScale, color, thickness, cv2.LINE_AA)

            height, width, _ = frame[40:, :].shape
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time
            frame_count += 1

            # Hiển thị FPS trên khung hình
            cv2.putText(annotated_frame, f"FPS: {round(fps, 2)}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('frame', annotated_frame)

            try:
                if self.toggle_var.value == 'start':
                    utils.frame.value += 1
                    self.writer.write(frame[40:, :])

                elif self.toggle_var.value == 'stop':
                    utils.frame.value = 0
                    self.writer.release()
            except Exception as e:
                pass

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print('stop camera')
                self.cap.release()
                self.writer.release()
                cv2.destroyWindow('frame')
                break

    def toggle(self):
        self.is_running = not self.is_running
        if self.is_running:
            Path('data/' + self.name_id).mkdir(parents=True, exist_ok=True)
            self.path = os.path.join('data', self.name_id, f'{self.name_id}_{utils.name_id.value}' + '.mp4')
            self.writer = cv2.VideoWriter(self.path, self.fourcc, 25.0,
                                          (int(self.cap.get(3)), int(self.cap.get(4)) - 40))


class SpinCamThread:
    def __init__(self, name, toggle_var):

        # Set up thread variables
        self.toggle_var = toggle_var.value
        self.name_id = name
        utils.make_dir(name=self.name_id)
        self.path = os.path.join('data', self.name_id, f'{self.name_id}_{str(utils.name_id.value)}' + '.mp4')
        self.is_running = False

        self.fps = 30
        self.resolution = (1440, 1080)

        # Set up camera
        self.system = PySpin.System.GetInstance()
        self.cam_list = self.system.GetCameras()
        self.cam = self.cam_list[0]

        self.nodemap_tldevice = self.cam.GetTLDeviceNodeMap()
        self.cam.Init()
        self.nodemap = self.cam.GetNodeMap()

        # Set up
        w, h = self.resolution
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(self.path, self.fourcc, self.fps,
                                      (w, h))

        # Initialize thread
        self._config()
        self.cam_process = Thread(target=self._run, daemon=True, name='Cam_Thread')
        self.cam_thread.start()
        keyboard.add_hotkey('space', self.toggle)

    def _run(self):

        self.cam.BeginAcquisition()
        frame = 0
        start_time = time.perf_counter()
        while True:
            image_result = self.cam.GetNextImage(1000)

            if image_result.IsIncomplete():
                print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
            else:
                frame += 1
                duration = time.perf_counter() - start_time
                fps = frame / duration
                image_data = image_result.GetNDArray()
                image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)

                show_data = cv2.resize(image_data, (720, 480))
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                cv2.putText(show_data, str(fps), (50, 50), font,
                            fontScale, color, thickness, cv2.LINE_AA)

                winname = 'Flir Camera'
                cv2.namedWindow(winname)  # Create a named window
                cv2.moveWindow(winname, 40, 30)  # Move it to (40,30)
                cv2.imshow(winname, show_data)

                if self.toggle_var == 'start':
                    utils.frame.value += 1
                    self.writer.write(image_data)

                elif self.toggle_var == 'stop':
                    utils.frame.value = 0
                    self.writer.release()

            image_result.Release()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self._end()

    def toggle(self):
        self.is_running = not self.is_running
        if self.is_running:
            utils.make_dir(name=self.name_id)
            self.path = os.path.join('data', self.name_id, f'{self.name_id}_{utils.name_id.value}' + '.mp4')
            w, h = self.resolution
            self.writer = cv2.VideoWriter(self.path, self.fourcc, self.fps,
                                          (w, h))

    def _config(self):
        sNodemap = self.cam.GetTLStreamNodeMap()

        node_bufferhandling_mode = PySpin.CEnumerationPtr(sNodemap.GetNode('StreamBufferHandlingMode'))
        node_newestonly = node_bufferhandling_mode.GetEntryByName('NewestOnly')
        node_newestonly_mode = node_newestonly.GetValue()
        node_bufferhandling_mode.SetIntValue(node_newestonly_mode)
        node_acquisition_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('AcquisitionMode'))
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)

    def _end(self):
        self.cam.EndAcquisition()
        cv2.destroyWindow('Flir Camera')
        self.cam.DeInit()
        del self.cam
        self.cam_list.Clear()
        self.system.ReleaseInstance()
