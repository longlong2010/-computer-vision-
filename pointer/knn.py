import cv2;
import numpy;

model = cv2.ml.KNearest_create();
samples = [];
labels = [];
for i in range(0, 10):
    im = cv2.imread('samples/' + str(i) + '.png');
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = cv2.resize(im, (20, 40));
    im = im.reshape(1, 800) / 255;
    samples.append(im[0]);
    labels.append(i);
labels = numpy.array(labels, numpy.float32);
samples = numpy.array(samples, numpy.float32);
model.train(samples, cv2.ml.ROW_SAMPLE, labels);

tests = [];
for i in range(0, 10):
    im = cv2.imread('tests/' + str(i) + '.png');
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = cv2.resize(im, (20, 40));
    im = im.reshape(1, 800) / 255;
    tests.append(im[0]);

tests = numpy.array(tests, numpy.float32);
retval, results, neigh_resp, dists = model.findNearest(tests, 1)
string = results.ravel()

print(labels.reshape(1,len(labels))[0])
print(string)
