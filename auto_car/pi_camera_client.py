import io
import socket
import struct
import time
import picamera

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
print 'PI Camera Client is connecting to computer server host 10.3.33.106...'
client_socket = socket.socket()
# client_socket.connect(('192.168.0.100', 8000))
# client_socket.connect(('192.168.0.103', 8000))
client_socket.connect(('192.168.43.66', 8000))  #GL home macbook ip
# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
print 'Connected.  Start sending out images to server.'

while True:
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (320, 240)      # pi camera resolution
            # camera.resolution = (1280,960)      # pi camera X4
            camera.framerate = 10               # 10 frames/sec
            # camera.framerate = 2               # 10 frames/sec
            time.sleep(2)                       # give 2 secs for camera to initilize
            start = time.time()
            stream = io.BytesIO()
            
            # send jpeg format video BytesIO stream
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                stream.seek(0)
                connection.write(stream.read())
                if time.time() - start > 600:
                    break
                stream.seek(0)
                stream.truncate()
        connection.write(struct.pack('<L', 0))
    finally:
        connection.close()
        client_socket.close()
