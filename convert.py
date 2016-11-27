import numpy;
import cv2;

im = cv2.imread('test.jpg');
h, w, _ = im.shape;
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY);
cv2.imwrite('gray.jpg', gray);
brushSize = 2;
coarseness = 10;
contrast = 0.6;

l = coarseness + 1;

countIntensity = numpy.ndarray(shape=(l, 1), dtype = int);
redAvg = numpy.ndarray(shape=(l, 1), dtype = int);
greenAvg = numpy.ndarray(shape=(l, 1), dtype = int);
blueAvg = numpy.ndarray(shape=(l, 1), dtype = int);

out = numpy.ndarray(shape=(h, w, 3), dtype = int);

for y in range(0, h):
	top = y - brushSize;
	bottom = y + brushSize + 1;

	if top < 0:
		top = 0;
	if bottom >= h:
		bottom = h - 1;
	
	for x in range(0, w):
		left = x - brushSize;
		right = x + brushSize + 1;

		if left < 0:
			left = 0;
		if right >= w:
			right = w - 1;

		for i in range(0, l):
			countIntensity[i] = 0;
			redAvg[i] = 0;
			greenAvg[i] = 0;
			blueAvg[i] = 0;

		for i in range(top, bottom):
			for j in range(left, right):
				intensity = int(coarseness * gray[i][j] / 255.0);

				countIntensity[intensity] += 1;
				redAvg[intensity] += im[i][j][2];
				greenAvg[intensity] += im[i][j][1];
				blueAvg[intensity] += im[i][j][0];

		chosenIntensity = 0;
		maxInstance = countIntensity[0];

		for i in range(1, l):
			if countIntensity[i] > maxInstance:
				chosenIntensity = i;
				maxInstance = countIntensity[i];

		out[y][x][2] = redAvg[chosenIntensity] / float(maxInstance);
		out[y][x][1] = greenAvg[chosenIntensity] / float(maxInstance);
		out[y][x][0] = blueAvg[chosenIntensity] / float(maxInstance);

		for i in range(0, 3):
			out[y][x][i] = int(out[y][x][i] * contrast + (1 - contrast) * 125);

cv2.imwrite('out.jpg', out);
