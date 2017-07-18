# -*- coding:utf-8 -*-
import cv2;
import sys;
import threading;
if sys.version_info[0] == 3:
    from queue import Queue;
else:
    from Queue import Queue;
import numpy;
import math;
import socket;
import pickle;
import struct;
import time;

class ProcessThread(threading.Thread):
    def __init__(self, q):
        super(ProcessThread, self).__init__();
        self.q = q;
        self.rs = "";
    def process_image(self, im):
        v0 = 10.0;
        dv = 30.0 / 90.0;
        h = numpy.size(im, 0);
        w = numpy.size(im, 1);
        #边缘处理
        edges = cv2.Canny(im, 10, 140, 3);
        #识别圆和直线
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT if cv2.__version__ >= '3' else cv2.cv.CV_HOUGH_GRADIENT, 2, w / 4);
        lines = cv2.HoughLinesP(edges, 1, numpy.pi / 180, 10, 100, 30);
        if isinstance(circles, numpy.ndarray) == False or isinstance(lines, numpy.ndarray) == False:
            return im;
        #取整个都在图片内的最大的一个圆
        circle_list = [];
        for x in circles[0]:
            if x[0] + x[2] < w and x[0] - x[2] > 0 and x[1] + x[2] < h and x[1] - x[2] > 0:
                circle_list.append(x);
        if len(circle_list) == 0:
            return im;
        c = circle_list[0];
        for x in circle_list:
            if x[2] > c[2]:
                c = x;
        cv2.circle(im, (c[0], c[1]), c[2], (255, 0, 0), 4);
        
        #取与找到的圆的距离小于阈值的直线
        line_list = [];
        for x in lines:
            x1, y1, x2, y2 = x[0];
            v = numpy.array([c[0] - x1, c[1] - y1]);
            n = numpy.array([y1 - y2, x2 - x1]);
            if abs(numpy.dot(v, n) / numpy.linalg.norm(n)) < 30:
                cv2.line(im, (x1, y1), (x2, y2),(0, 255, 0), 4);
                #指针确定方向
                t1 = numpy.array([x1 - c[0], y1 - c[1]]);
                t2 = numpy.array([x2 - c[0], y2 - c[1]]);
                t = t1 - t2 if numpy.linalg.norm(t1) > numpy.linalg.norm(t2) else t2 - t1;
                sgn = 1 if t[0] >= 0 else -1;
                #计算指针和竖直方向的夹角
                val = v0 + dv * math.acos(numpy.dot(t, numpy.array([0, -1]) / numpy.linalg.norm(t))) * 180 / numpy.pi * sgn;
                t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()));
                self.rs = "%s  %f" % (t, val);
                print(self.rs);
        return im;
    def run(self):
        while True:
            if not self.q.empty():
                im = self.q.get();
                self.process_image(im);
                
class StreamServer(threading.Thread):
    def __init__(self, q):
        super(StreamServer, self).__init__();
        self.q = q;
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        s.bind(('0.0.0.0', 1987));
        s.listen(1);
        conn, addr = s.accept();
        while True:
            if not self.q.empty():
                im = self.q.get();
                data = pickle.dumps(im);
                l = len(data);
                try:
                    conn.send(struct.pack('i', l));
                    conn.send(data);
                except:
                    conn, addr = s.accept();
                    

if __name__ == '__main__':
    cp = cv2.VideoCapture(1);
    if not cp.isOpened():
        sys.exit();
    fps = cp.get(cv2.CAP_PROP_FPS) if cv2.__version__ >= '3' else 30;
    
    q1 = Queue(1);
    worker = ProcessThread(q1);
    worker.start();
    
    q2 = Queue(1);
    server = StreamServer(q2);
    server.start();
    
    while True:
        ret, im = cp.read();
        if q1.empty():
            q1.put(im);

        if worker.rs != "":
            cv2.putText(im, worker.rs, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2);
        #cv2.imshow('Video', im);
        if q2.empty():
            q2.put(im);
        cv2.waitKey(int(1000 / fps));
