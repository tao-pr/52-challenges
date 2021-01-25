#ifndef EXTRACT_HPP
#define EXTRACT_HPP

#include <string>
#include <vector>
#include <tuple>
#include <cstdlib>
#include <set>

#include <fmt/format.h>

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

typedef Rect2d Boundary;

enum Orientation
{
  HORZ = 1,
  VERT = 5
};

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

struct LineSpatialMap
{
  Mat map;
  vector<Boundary> horz;
  vector<Boundary> vert;
  Size size;

  static LineSpatialMap createFromVector(vector<Boundary> horz, vector<Boundary> vert, Size imageSize)
  {
    LineSpatialMap m;
    m.map = Mat::zeros(imageSize.height, imageSize.width, CV_8UC1);
    m.horz = horz;
    m.vert = vert;
    m.size = imageSize;
    return m;
  }

  tuple<set<int>, set<int>> profile1D() const
  {
    set<int> px;
    set<int> py;

    for (auto h : horz)
      py.insert((int)h.y);
    for (auto v : vert)
      px.insert((int)v.x);

    return make_tuple(px, py);
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
    const int connectivity = 4;

#ifdef DEBUG
    Mat canvas = Mat::ones(im.rows, im.cols, CV_8UC3);
    canvas = Scalar(255, 255, 255);
#endif

    int cnt = connectedComponentsWithStats(im, contours, stats, centroids, connectivity);
    for (int i=1; i<cnt; i++) // Intentionally skip the first element
    {
      int x = stats.at<int>(i, CC_STAT_LEFT);
      int y = stats.at<int>(i, CC_STAT_TOP);
      int w = stats.at<int>(i, CC_STAT_WIDTH);
      int h = stats.at<int>(i, CC_STAT_HEIGHT);
      int area = stats.at<int>(i, CC_STAT_AREA);
      
#ifdef DEBUG
      rectangle(canvas, Point(x,y), Point(x+w,y+h), Scalar(0,70,0));
#endif
      v.push_back(Rect2d(x, y, w, h));
    }

#ifdef DEBUG
    imshow(fmt::format("extract-cc-{}", rand()), canvas);
#endif

    return v;
  }

  // Filter proper lines by orientation
  inline vector<Boundary> filterLine(
    vector<Boundary>& v, 
    Orientation how, 
    int pageWidth, int pageHeight,
    bool thinning=true) const 
  {
    vector<Boundary> vOut;
    for (auto b : v)
    {
      // Drop shape which does not look like a long thin line
      auto p = min(b.width, b.height);
      auto q = max(b.width, b.height);
      if (p/q >= 0.05)
        continue;

      if (how == HORZ)
      {
        // Width of the line has to be at least 30% of the page width
        if (b.width < pageWidth*0.3)
          continue;
        if (thinning)
          b.height = 1;
      }
      else 
      {
        // Height of the line has to be at least 6% of the page height
        if (b.height < pageHeight*0.06)
          continue;
        if (thinning)
          b.width = 1;
      }
      vOut.push_back(b);
    }
    return vOut;
  }

  inline LineSpatialMap extractLines(Mat& im) const
  {
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

    bitwise_or(lineHorz, lineVert, lineAll);
#ifdef DEBUG
    imshow("lines", lineAll);
    imwrite("./bin/bin.jpg", binImage);
    imwrite("./bin/lines.jpg", lineAll);
    imwrite("./bin/horz.jpg", lineHorz);
    imwrite("./bin/vert.jpg", lineVert);
#endif

    // Identify all connected components in each alignment separately
    vector<Boundary> horz = extractCC(lineHorz);
    vector<Boundary> vert = extractCC(lineVert);

    horz = filterLine(horz, HORZ, im.cols, im.rows);
    vert = filterLine(vert, VERT, im.cols, im.rows);

    auto lmap = LineSpatialMap::createFromVector(horz, vert, im.size());

    set<int> profileRow, profileCol;
    tie(profileCol, profileRow) = lmap.profile1D();

#ifdef DEBUG
    Mat filteredLine = Mat::ones(im.rows, im.cols, CV_8UC3);
    filteredLine = Scalar(255, 255, 255);

    for (auto x : profileCol)
      line(filteredLine, Point2d(x,0), Point2d(x,im.rows-1), Scalar(110,110,110));

    for (auto y : profileRow)
      line(filteredLine, Point2d(0,y), Point2d(im.cols-1,y), Scalar(110,110,110));

    for (auto h : horz)
      rectangle(filteredLine, h.tl(), h.br(), Scalar(0,130,0), 3);
    
    for (auto v : vert)
      rectangle(filteredLine, v.tl(), v.br(), Scalar(0,0,130), 3);

    imshow("filtered lines", filteredLine);
    imwrite("./bin/lines-filtered.jpg", filteredLine);
#endif

    return lmap;
  }
};

#endif