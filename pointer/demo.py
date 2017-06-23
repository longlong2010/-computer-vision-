import cv2;
import numpy;
import math;

im = cv2.imread('1-resize.jpg');
h = numpy.size(im, 0);
w = numpy.size(im, 1);
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY);
edges = cv2.Canny(gray, 10, 140, 3);
cv2.imwrite('out.jpg', edges);
lines = cv2.HoughLinesP(edges, 1, numpy.pi / 180, 100, 100, 30);
circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 2, w / 4);
circle_list = [];
for x in circles[0]:
    if x[0] + x[2] < w and x[0] - x[2] > 0 and x[1] + x[2] < h and x[1] - x[2] > 0:
        circle_list.append(x);

c = circle_list[0];
for x in circle_list:
    if x[2] > c[2]:
        c = x;

cv2.circle(im, (c[0], c[1]), c[2], (255, 0, 0), 4);
line_list = [];
for x in lines:
    x1, y1, x2, y2 = x[0];
    v = numpy.array([c[0] - x1, c[1] - y1]);
    n = numpy.array([y1 - y2, x2 - x1]);
    if abs(numpy.dot(v, n) / numpy.linalg.norm(n)) < 30:
        cv2.line(im, (x1, y1), (x2, y2),(0, 255, 0), 4);
        t = numpy.array([x2 - x1, y2 - y1]);
        print(math.acos(numpy.dot(t, numpy.array([1, 0]) / numpy.linalg.norm(t))) * 180 / numpy.pi);

cv2.imwrite('out.jpg', im);
