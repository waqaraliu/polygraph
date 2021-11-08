import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import time
from imutil import FPS
from imutil import HdmiVideoStream
import socket
from helpers import getInterface

stream = None
fps = None


class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header(
                'Content-type',
                'multipart/x-mixed-replace; boundary=--jpgboundary'
            )
            self.end_headers()
            while True:
                try:
                    rc, img = stream.read()
                    if not rc:
                        continue

                    img_str = cv2.imencode('.jpg', img)[1].tostring()

                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', len(img_str))
                    self.end_headers()

                    self.wfile.write(img_str)
                    self.wfile.write(b"\r\n--jpgboundary\r\n")
                    time.sleep(1/5)
                except KeyboardInterrupt:
                    self.wfile.write(b"\r\n--jpgboundary--\r\n")
                    break
                except BrokenPipeError:
                    continue
            return

        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><head></head><body>')
            self.wfile.write(b'<img src="http://192.168.1.9:5050/cam.mjpg"/>')
            self.wfile.write(b'</body></html>')
            return


class StreamServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def checkConnection():
    try:
        ipAddr = socket.gethostbyname(socket.gethostname())
        if ipAddr == '127.0.0.1':
            print('not connected to network')
            return False
        else:
            print('connected to network')
            return True
    except socket.herror:
        print('socket Error')
        return False

def main():
    global fps
    global stream
    #first check network connection, if not connected then connect to available network
    #getInterface()
    if not checkConnection:
        print('please connect to network, save ssid in config')
        return
    stream = HdmiVideoStream(src=0)
    # ~ fps = FPS().start()
    time.sleep(1)
    
    try:
        status = stream.status
        if not status:
            print("Stream Closed")
            return
        stream.start()
        server = StreamServer(('192.168.1.9', 5050), HttpHandler)
        print("server started at http://192.168.1.9:5050/cam.html")
        server.serve_forever()
    except KeyboardInterrupt:
        # ~ fps.stop()
        stream.stop()
        cv2.destroyAllWindows()
        server.socket.close()
    except e:
        print("General Exception Handled :" + str(e))
        stream.stop()
        cv2.destroyAllWindows()

