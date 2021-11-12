import os
import cv2
from base_camera import BaseCamera
import queue
import threading
import time

class Capture():
    video_source = 0
    
    camera = None
    thread = None
    def __init__(self):
        if Capture.thread is None:
            Capture.set_video_source(0)
            Capture.camera = cv2.VideoCapture(Capture.video_source)
            Capture.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
            Capture.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
            self.q = queue.Queue()
            thread = threading.Thread(target=self._reader)
            thread.daemon = True
            thread.start()
            #init base module here
            print('Starting Base')
#         super(Capture, self).__init__()

    @staticmethod
    def set_video_source(source):
        Capture.video_source = source
        
    def closeDevice(self):
        print('close in main thread')
        
        Capture.camera.release()
#         Capture.thread.join()
        Capture.thread = None
#         self.camera.release()

    @staticmethod
    def frames():
        
        if not Capture.camera.isOpened():
            raise RuntimeError('Could not start camera.')
        print('reading frame')
        ret, data = Capture.camera.read()
        return data
    def _reader(self):
        i = 0
        while True:
              i = i + 1
    #       time.sleep(1/5)
              print('reading capture :' +str(i))
              ret, frame = Capture.camera.read()
#               cv2.waitKey()
              if not ret:
                  print('blank image')
#                   break
              else:
                  print('Vblank image')
                  #now here save frame, save every fifth frame to avoid blank
                  #get 4 frames
                  if not self.q.empty():
                    try:
                      self.q.get_nowait()
                      # discard previous (unprocessed) frame
                    except queue.Empty:
                      pass
                  self.q.put(frame)
#                   break
    #           if i == 4:
    #               break
              if i == 1:
                  break
              print('FPS :' + str(i))
              time.sleep(1/5)
          
    def read(self):
#             ret, frame = Capture.camera.read()
#             cv2.waitKey()
#             if not ret:
#                 print('blank image')
# #                 break
#             else:
#                 print('No Vblank image')
# #             return frame
          return self.q.get()
    
#         while True:
#             # read current frame
#             _, img = camera.read()
# 
# #             # encode as a jpeg image and return it
#             yield cv2.imencode('.jpg', img)[1].tobytes()
