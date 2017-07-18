# -*- coding:utf-8 -*-
import socket;
import struct;
import pickle;
import numpy;
import cv2;

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.connect(('127.0.0.1', 1987));
    while True:    
        l = struct.unpack('i', s.recv(4))[0];
        data = s.recv(l);
        while l > len(data):
            data += s.recv(l - len(data));
        im = pickle.loads(data);
        cv2.imshow('Client', im);
        cv2.waitKey(int(1000 / 30));
