import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import time
from imutil import FPS
from imutil import HdmiVideoStream
import socket
from helpers import getInterface
from zeroconf import ServiceInfo, Zeroconf
import logging
import threading
from io import StringIO,BytesIO
from PIL import Image
from flask import Flask, request, Response, jsonify, make_response
import requests
import queue
import subprocess as sp
import ffmpeg
import sys
import numpy

from capture import Capture

# stream = None
# fps = None
# zeroconf = None
# info = None
# serviceName = None
# servicePort = None
# capture = None
# pic = []
# cap = None
# app_not_done = True
# width = 640
# height = 480
# im = []
# vcap = None
# vimg =None


app = Flask(__name__)


    
# class CameraThread(threading.Thread):
#     def __init__(self, name):
#         threading.Thread.__init__(self)
#         self.name = name
#         
#     def run(self):
#         global pic
#         global app_not_done
#         global im
# 
#         print("+++++++++ SETTING UP CAMERA ++++++++")
# #         cap = cv2.VideoCapture(0)
# #         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# #         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#         cnt = 0
#         while(app_not_done):
#             # Capture frame-by-frame
#             ret, frame = cap.read()
#             if ret:
#                 print('getting frame')
#                 pic = frame
#                 im = pic
#             else:
#                 cnt += 1
#                 print('could not')
#                 if cnt < 4:
#                     print("Could not read camera")
#             time.sleep(1/2)
# 
#         # When everything done, release the capture
#         print("RELEASING CAMERA *******************")
#         cap.release()
#
#reads after 5 fps
# class VideoCapture:
# 
#   def __init__(self, name):
#     self.capa = cv2.VideoCapture(name)
#     self.capa.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
#     self.capa.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
#     self.q = queue.Queue()
#     t = threading.Thread(target=self._reader)
#     t.daemon = True
#     t.start()
#   # read frames as soon as they are available, keeping only most recent one
#   def _reader(self):
#     while True:
# #       time.sleep(1/5)
#       print('reading')
#       ret, frame = self.capa.read()
#       if not ret:
#         break
#       if not self.q.empty():
#         try:
#           self.q.get_nowait()
#           # discard previous (unprocessed) frame
#         except queue.Empty:
#           pass
#       self.q.put(frame)
#       time.sleep(1/5)
# 
#   def read(self):
#       return self.q.get()
    
#check different capture process efficiency. Stop usb device lock, and get frames
# vCapture = VideoCapture('this')
@app.route("/")
def home_page():
    print('in home page')
    #http://<IP>:1881/vgabroadcaster.jpg
#     cap2 = cv2.VideoCapture(0)
#     cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#     ret, frame = cap2.read()
#     while True:
#         if not ret:
#             print('no image')
#         else:
#             print('image success')
#             return
    retval, buffer = cv2.imencode('.jpg', im)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}
    #response = requests.post('http://192.168.8.141:1881/vgabroadcaster.jpg', data=buffer.tostring(), headers=headers)
    print('sending response')
#     cap2.release()
    return response
    
@app.route("/vgabroadcaster.jpg")
def send_jpg():
    
    print('sending jpg response')
#     cap2 = cv2.VideoCapture(0)
    #http://<IP>:1881/vgabroadcaster.jpg
#     cap2 = cv2.VideoCapture(0)
#     cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# # #     cap2.set(cv2.CAP_PROP_FPS, 2)
#     while True:    
#       ret, frame = cap2.read()
#         if ret:
#             print('got img')
#             break
#         else:
#             print('unabke to get img')
#     while True:
        
#             print('no image')
#         else:
#             print('image success')
#             break
#     time.sleep(0.2)
#     fra = VideoCapture.read(vcap)
    
#     #response = requests.post('http://192.168.8.141:1881/vgabroadcaster.jpg', data=buffer.tostring(), headers=headers)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#ffmpeg -f video4linux2 -i /dev/v4l/by-id/usb-0c45_USB_camera-video-index0 -vframes 1 test.jpeg
#     out, _ = (
#         ffmpeg
#         .input('/dev/video0')
#         .filter('select', 'gte(n,{})'.format(1))
#         .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
#         .run(capture_stdout=True)
#     )
#     sys.stdout.buffer.write(out)
#     command = ["ffmpeg", "-f", "video4linux2", "-i", "dev/video0", "-vframes", "1", "-s", "1024x768", "-f", "image2pipe", "-"]
#     p = sp.Popen(command, stdout=sp.PIPE, bufsize = 10**8)
#     raw_image = p.stdout.read(1024*768*3)
#     image =  numpy.frombuffer(raw_image, dtype='uint8')
# #     image = image.reshape((height,width,3))
#     p.communicate()
# #     p.stdout.flush()
#     print('encoding')
#     retval, buffer = cv2.imencode('.jpg', image)
    capture = Capture()
    frame = capture.read()
    print('sending to client')
    raw_image = cv2.imencode('.jpg', frame)[1].tobytes()
    response = make_response(raw_image)
    response.headers['Content-Type'] = 'image/jpeg'
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}
    print('sending response')
    capture.closeDevice()
#     cap2.release()
    return response
# 
# def make_server(self, w, h):
#     global width, height
#     width = w
#     height = h
#     thrd = CameraThread('V4l2 Capture Thread')
#     thrd.daemon = True
#     thrd.start()
#     app.run(host='0.0.0.0', port=1881, debug=True)
#     app_not_done = False
#     thrd.join()

if __name__ == "__main__":
#     global vimg
#     global vcap
#     vcap = VideoCapture(0)
#     thrd = CameraThread('V4l2 Capture Thread')
#     thrd.daemon = True
#     thrd.start()
#     while True:
#         if cap2.isOpened():
#             break
#         else:
#             print('device not open')
    app.run(host='0.0.0.0', port=1881, debug=True)
    app_not_done = False
#     cv2.destroyAllWindows()
#     thrd.join()


