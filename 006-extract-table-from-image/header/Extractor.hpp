#ifndef EXTRACT_HPP
#define EXTRACT_HPP

#include <string>
#include <vector>
#include <tuple>

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

typedef Rect2d Boundary;

struct Line 
{
  tuple<Point2d, Point2d> p; // End points
  inline void drawTo(Mat& im)
  {
    Point2d a,b;
    tie(a, b) = p;
    line(im, a, b, Scalar(255,0,0));
  }
};

/**
 * Generic extractor
 */
template <class A>
class Extract
{
public:
  inline Extract(){};
  virtual inline ~Extract() {};

  virtual vector<A> extract(Mat& im) const = 0;

  inline Mat binarise(Mat& im) const 
  {
    const int maxValue = 255;
    Mat out = Mat::zeros(im.rows, im.cols, CV_8UC1);
    Mat inv = Mat::zeros(im.rows, im.cols, CV_8UC1);

    threshold(im, out, 220, maxValue, THRESH_BINARY);
    bitwise_not(out, inv);

    // Dilate and erode so fragmented shapes are re-connected
    auto kernel = getStructuringElement(MORPH_RECT, Size(5,5));
    dilate(inv, inv, kernel);
    erode(inv, inv, kernel);

    return inv;
  }

  inline vector<Boundary> extractCC(Mat& im) const 
  {
    vector<Boundary> v;
    Mat contours, stats, centroids;
    const int connectivity = 8;

    int cnt = connectedComponentsWithStats(im, contours, stats, centroids, connectivity);
    for (int i=0; i<cnt; i++)
    {
      // TAOTODO
    }

    return v;
  }

  inline vector<Line> extractLines(Mat& im) const
  {
    vector<Line> v;

    Mat binImage = binarise(im);

    float hrzSize = im.cols / 30;
    float verSize = im.rows / 30;

    auto hrzKernel = getStructuringElement(MORPH_RECT, Size(int(hrzSize), 1));
    auto verKernel = getStructuringElement(MORPH_RECT, Size(1, int(verSize)));

    Mat lineHorz = Mat::zeros(im.rows, im.cols, CV_8UC1);
    Mat lineVert = Mat::zeros(im.rows, im.cols, CV_8UC1);
    Mat lineAll = Mat::zeros(im.rows, im.cols, CV_8UC1);

    erode(binImage, lineHorz, hrzKernel);
    erode(binImage, lineVert, verKernel);

#ifdef DEBUG
    imshow("binary", binImage);
    imshow("horz", lineHorz);
    imshow("vert", lineVert);
#endif

    bitwise_or(lineHorz, lineVert, lineAll);
#ifdef DEBUG
    imshow("lines", lineAll);
    imwrite("./bin/lines.jpg", lineAll);
    imwrite("./bin/horz.jpg", lineHorz);
    imwrite("./bin/vert.jpg", lineVert);
#endif

    // Identify all connected components in each alignment separately
    vector<Boundary> horz = extractCC(lineHorz);
    vector<Boundary> vert = extractCC(lineVert);

    // TAOTODO
    return v;
  }
};

#endif