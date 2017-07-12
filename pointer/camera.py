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

def process_image(im):
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
            print(val);
    return im;

class ProcessThread(threading.Thread):
    def __init__(self, q):
        super(ProcessThread, self).__init__();
        self.q = q;
    def run(self):
        while True:
            if q.empty() == False:
                im = self.q.get();
                process_image(im);
                

cp = cv2.VideoCapture(0);
if not cp.isOpened():
    sys.exit();
fps = cp.get(cv2.CAP_PROP_FPS) if cv2.__version__ >= '3' else 30;
q = Queue(1);

worker = ProcessThread(q);
worker.start();
while True:
    ret, im = cp.read();
    cv2.imshow('Video', im);
    if q.empty():
        q.put(im);
    cv2.waitKey(int(1000 / fps));
