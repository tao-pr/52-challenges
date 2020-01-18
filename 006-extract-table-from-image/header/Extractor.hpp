#ifndef EXTRACT_HPP
#define EXTRACT_HPP

#include <string>
#include <vector>

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

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
};

#endif