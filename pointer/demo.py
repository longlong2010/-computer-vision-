# -*- coding:utf-8 -*-
import cv2;
import numpy;
import math;

#竖直向上方向的读数
v0 = 15.0;
#每度对应的读数变化
dv = 30.0 / 90.0;

#读取图片，计算宽高
im = cv2.imread('test2.jpg');
h = numpy.size(im, 0);
w = numpy.size(im, 1);
#灰度处理
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY);
edges = cv2.Canny(gray, 10, 140, 3);
#识别圆和直线
circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 2, w / 4);
lines = cv2.HoughLinesP(edges, 1, numpy.pi / 180, 10, 100, 50);

#取整个都在图片内的最大的一个圆
circle_list = [];
for x in circles[0]:
    if x[0] + x[2] < w and x[0] - x[2] > 0 and x[1] + x[2] < h and x[1] - x[2] > 0:
        circle_list.append(x);
c = circle_list[0];
for x in circle_list:
    if x[2] > c[2]:
        c = x;
cv2.circle(im, (c[0], c[1]), c[2], (255, 0, 0), 4);

cv2.imwrite('out.jpg', im);
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

cv2.imwrite('out.jpg', im);
