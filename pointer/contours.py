import cv2;

img = cv2.imread('2.png');
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV);
img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);
height, width = img.shape[:2];
i = 0;
for u in contours:
    [x, y, w, h] = cv2.boundingRect(u);
    cv2.imwrite('tests/' + str(i) + '.png', thresh[y : y + h, x : x + w]);
    i = i + 1;
cv2.imwrite('my.png', thresh);
