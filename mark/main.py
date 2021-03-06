import cv2;
import time;
import numpy;
import math;

if __name__ == '__main__':
    im = cv2.imread('IMG_0920.JPG');
    im_g = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);
    im_t = im_g[2500:2900, 1200:1600];
    height, width = im_t.shape[:2];

    im_r = cv2.matchTemplate(im_g, im_t, cv2.TM_SQDIFF_NORMED);
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(im_r);
    cv2.rectangle(im, min_loc, (min_loc[0] + width, min_loc[1] + height), (0,0,255), 2);
    cv2.imwrite('out.jpg', im);
    cv2.imshow('test', im_t);
    cv2.waitKey(0);
