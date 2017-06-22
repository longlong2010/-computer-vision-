import cv2;
import numpy;
#im0 = cv2.imread('7c333c62cad2e7378d60b_b.jpg');
#im0 = cv2.imread('7c333c6bad1b917df71b_b.jpg');
im0 = cv2.imread('7c333c62bfd7077ba0c33_b.jpg');
#im0 = cv2.imread('test1.jpg');
im = cv2.cvtColor(im0, cv2.COLOR_RGB2GRAY);
th, im = cv2.threshold(im, 180, 255, cv2.THRESH_BINARY);
cv2.imwrite('gray.jpg', im);

_, contours, hierarchy = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);
im = cv2.drawContours(im0, contours, -1, (255, 0, 0), cv2.FILLED);
sky = cv2.imread('55efd8cdcd904.jpg');
h, w, _ = im.shape;
h1, w1, _ = sky.shape;
for y in range(0, h):
    for x in range(0, w):
        if im[y][x][0] == 255 and im[y][x][1] == 0 and im[y][x][2] == 0:
            if y >= h1 or x >= w1:
                continue;
            im[y][x] = sky[y][x];

cv2.imwrite('identity.jpg', im);
