
import numpy as np
import cv2
import pygame
from pygame.locals import *
import socket
import time
import struct
import io


class CollectTrainingData(object):
    
    def __init__(self):
        # Computer Client to send out RC Cart control signals 
        # self.broadcastIP = '192.168.0.104'           # IP address to send to, 255 in one or more positions is a broadcast / wild-card
        self.broadcastIP = '192.168.0.100'           # IP address to send to, 255 in one or more positions is a broadcast / wild-card
        self.broadcastIP = '10.3.34.215'             #PI IP. Galvanize's education ip, 255 in one or more positions is a broadcast / wild-card
        self.broadcastIP = '192.168.1.12'            # PI IP. Gordon's house IP address to send to
        self.broadcastIP = '192.168.43.103'
        self.broadcastPort = 9038                    # What message number to send with (LEDB on an LCD)
        self.interval = 0.1                          # Time between keyboard updates in seconds, smaller responds faster but uses more processor time
        self.regularUpdate = True                    # If True we send a command at a regular interval, if False we only send commands when keys are pressed or released

        # Setup the connection for sending on
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)       # Create the socket
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)                        # Enable broadcasting (sending to many IPs based on wild-cards)
        self.sender.bind(('0.0.0.0', 0))                                                         # Set the IP and port number to use locally, IP 0.0.0.0 means all connections and port 0 means assign a number for us (do not care)
        print 'Connected to RC Car Control...'

        # Computer Server to receive PI Image Stream
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8000))
        self.server_socket.listen(0)
        self.connection = self.server_socket.accept()[0].makefile('rb')
        self.send_inst = True
        print 'Received PI Image Stream...'

        # Create labels -> k[0] = Left, k[1] = Right, k[2] = Up, k[3] = Down, k[4] = k[]
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')
        # self.k = np.zeros((6, 6), 'float')
        # for i in range(6):
        #     self.k[i, i] = 1
        # self.temp_label = np.zeros((1, 6), 'float')

        # Initialized pygame module, control car from the pop up window and start collecting images
        pygame.init()
        screen = pygame.display.set_mode([300,300])
        pygame.display.set_caption("RemoteKeyController - Press [ESC] to quit")
        self.collect_image()

    def collect_image(self):

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print 'Start collecting images...'
        e1 = cv2.getTickCount()
        # image_array = 360*240/2  -> Lowerver half of images..

        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 4), 'float')

        # stream video frames one by one
        try:
            stream_bytes = ' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
                    # image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_UNCHANGED)
                    
                    # select lower half of the image
                    roi = image[120:240, :]
                    
                    # save streamed images
                    cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)
                    
                    #cv2.imshow('roi_image', roi)
                    # cv2.imshow('image', image)
                    
                    # reshape the roi image into one row array
                    temp_array = roi.reshape(1, 38400).astype(np.float32)
                    # temp_array = np.zeros((1,38400))
                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:    
                            send_inst = False
                            command = 'x'
                            self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))
                            exit()
                            break

                        elif event.type == KEYDOWN:
                            key_input = pygame.key.get_pressed()
                            # complex orders
                            if (key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]) or (key_input[pygame.K_w] and key_input[pygame.K_d]):
                                print("Forward Right")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                command = 'wd'
                                self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))

                            elif (key_input[pygame.K_UP] and key_input[pygame.K_LEFT]) or (key_input[pygame.K_w] and key_input[pygame.K_a]):
                                print("Forward Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                command = 'wa'
                                self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))

                            elif (key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]) or (key_input[pygame.K_s] and key_input[pygame.K_d]):
                                print("Reverse Right")
                                command = 'sd'
                                self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))
                            
                            elif (key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]) or (key_input[pygame.K_s] and key_input[pygame.K_a]):
                                print("Reverse Left")
                                command = 'sa'
                                self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))

                            # simple orders
                            elif key_input[pygame.K_UP] or key_input[pygame.K_w]:
                                print("Forward")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[2]))
                                command = 'w'
                                self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))

                            elif key_input[pygame.K_DOWN] or key_input[pygame.K_s]:
                                print("Reverse")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[3]))
                                command = 's'
                                self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))
                            
                            elif key_input[pygame.K_RIGHT] or key_input[pygame.K_d]:
                                print("Right")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                command = 'r'
                                self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))

                            elif key_input[pygame.K_LEFT] or key_input[pygame.K_a]:
                                print("Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                command = 'l'
                                self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))

                            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                                print 'exit'
                                self.send_inst = False
                                command = 'x'
                                self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))
                                break
                                    
                        elif event.type == pygame.KEYUP:
                            # key_input = pygame.key.get_pressed()
                            # if (key_input[pygame.K_UP]) or  (key_input[pygame.K_w]):
                            #     print("FR or FL to Forward")
                            #     saved_frame += 1
                            #     image_array = np.vstack((image_array, temp_array))
                            #     label_array = np.vstack((label_array, self.k[2]))
                            #     command = 'w0'
                            #     self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))
                            # elif (key_input[pygame.K_DOWN]) or  (key_input[pygame.K_s]):
                            #     print("RR or RL to Reverse")
                            #     saved_frame += 1
                            #     image_array = np.vstack((image_array, temp_array))
                            #     label_array = np.vstack((label_array, self.k[3]))
                            #     command = 's0'
                            #     self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))
                            # if (not key_input[pygame.K_DOWN] and not key_input[pygame.K_UP]) and \
                            #     (not key_input[pygame.K_w] and not key_input[pygame.K_s]):
                            #     print 'no foward/backward key pressed'
                            command = '0'
                            self.sender.sendto(command, (self.broadcastIP, self.broadcastPort))

            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # save training data as a numpy file
            np.savez('training_data_temp/lvtest06.npz', train=train, train_labels=train_labels)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print 'Streaming duration:', time0

            print(train.shape)
            print(train_labels.shape)
            print 'Total frame:', total_frame
            print 'Saved frame:', saved_frame
            print 'Dropped frame', total_frame - saved_frame

        finally:
            self.connection.close()
            self.server_socket.close()

if __name__ == '__main__':
    CollectTrainingData()