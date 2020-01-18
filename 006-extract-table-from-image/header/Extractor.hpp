#ifndef EXTRACT_HPP
#define EXTRACT_HPP

#include <string>
#include <vector>

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

struct Table {
  Rect region;
  vector<Table> children;
};

class Extract
{
public:
  Extract();
  ~Extract();

  vector<Table> extract(Mat& im) const;
};

#endif