#include <opencv/cv.hpp>
using namespace cv;

int main() {
    Mat im = imread("identity.jpg");
    Mat gray;
    cvtColor(im, gray, CV_RGB2GRAY);
    imwrite("gray.png", gray);
    int brushSize = 2;
    int coarseness = 10;
    double contrast = 0.6;

    int l = coarseness + 1;

    int* countIntensity = new int[l];
    uint* redAvg = new uint[l];
    uint* greenAvg = new uint[l];
    uint* blueAvg = new uint[l];

    Mat out = Mat::zeros(im.size(), im.type());

    int h = im.rows;
    int w = im.cols;

    for (int y = 0; y < h; y++) {
        int top = y - brushSize;
        int bottom = y + brushSize + 1;

        if (top < 0) {
            top = 0;
        }
        if (bottom >= h) {
            bottom = h - 1;
        }

        for (int x = 0; x < w; x++) {
            int left = x - brushSize;
            int right = x + brushSize + 1;

            if (left < 0) {
                left = 0;
            }
            if (right >= w) {
                right = w - 1;
            }

            for (int i = 0; i < l; i++) {
                countIntensity[i] = 0;
                redAvg[i] = 0;
                greenAvg[i] = 0;
                blueAvg[i] = 0;
            }

            for (int i = top; i < bottom; i++) {
                for (int j = left; j < right; j++) {
                    uchar intensity = (coarseness * gray.at<uchar>(i, j)) / 255;

                    countIntensity[intensity] += 1;
                    redAvg[intensity] += im.at<Vec3b>(i, j)[2];
                    greenAvg[intensity] += im.at<Vec3b>(i, j)[1];
                    blueAvg[intensity] += im.at<Vec3b>(i, j)[0];
                }
            }

            int chosenIntensity = 0;
            int maxInstance = countIntensity[0];

            for (int i = 1; i < l; i++) {
                if (countIntensity[i] > maxInstance) {
                    chosenIntensity = i;
                    maxInstance = countIntensity[i];
                }
            }

            out.at<Vec3b>(y, x)[2] = redAvg[chosenIntensity] / (float) maxInstance;
            out.at<Vec3b>(y, x)[1] = greenAvg[chosenIntensity] / (float) maxInstance;
            out.at<Vec3b>(y, x)[0] = blueAvg[chosenIntensity] / (float) maxInstance;

            for (int i = 0; i < 3; i++) {
                out.at<Vec3b>(y, x)[i] = (int) (out.at<Vec3b>(y, x)[i] * contrast + (1 - contrast) * 125);
            }
        }
    }
    imwrite("out.png", out);
    return 0;
}
