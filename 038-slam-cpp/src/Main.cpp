#include <opencv2/opencv.hpp>
#include <stdlib.h>
#include "itertools/cppitertools/itertools.hpp"

using namespace std;
using namespace iter;

std::string depthToStr(int depth){
  if (depth == CV_8U) return "8-bit unsigned";
  else if (depth == CV_16U) return "16-bit unsigned";
  else if (depth == CV_32F) return "32-bit float";
  else return "unknown";
}

int main(int argc, char** argv){
  std::string pathVideo("media/video.mp4");
  cout << pathVideo << endl;
  cv::VideoCapture capture(pathVideo);

  bool hasReportedDim = false;

  cv::Mat frame, prev;
  std::vector<cv::Point2f> prevFeatures;

  while (capture.read(frame)){
    if (!hasReportedDim){
      int type = frame.type();
      int channels = CV_MAT_CN(type);
      auto depth = depthToStr(CV_MAT_DEPTH(type));
      cout << "channels : " << channels << endl;
      cout << "depth    : " << depth << endl;
    }

    cout << "processing frame ... " << endl;

    // convert RGB to grayscale
    float scaleFactor = 4;
    cv::Mat resized;
    cv::Mat gray;
    cv::resize(frame, resized, cv::Size(), 1/scaleFactor, 1/scaleFactor, cv::INTER_LINEAR);
    cv::extractChannel(resized, gray, 1); // take green channel

    if (!hasReportedDim){
      int type = gray.type();
      int channels = CV_MAT_CN(type);
      auto depth = depthToStr(CV_MAT_DEPTH(type));
      cout << "after conversion: " << endl;
      cout << "channels : " << channels << endl;
      cout << "depth    : " << depth << endl;
      cout << "size     : " << gray.size() << endl;
      hasReportedDim = true;
    }

    // Extract features from grayscale
    std::vector<cv::Point2f> features;
    std::vector<unsigned char> status;
    cv::goodFeaturesToTrack(gray, features, 500, 0.01, 10);

    // Track features
    if (!prevFeatures.empty()){
      cv::calcOpticalFlowPyrLK(
        prev, gray, 
        prevFeatures, features, 
        status, cv::noArray());

      // draw tracking lines if features are correlated
      for (auto [f, f0, s] : iter::zip(features, prevFeatures, status)){
        if (s){
          // red dot with line for trackable
          cv::arrowedLine(resized, f0, f, cv::Scalar(0, 0, 250), 1);
          cv::circle(resized, f, 2, cv::Scalar(0, 0, 250));
        }
        else
          // blue dot for untrackable
         cv::circle(resized, f, 2, cv::Scalar(250, 0, 0)); 
      }
    }

    cv::imshow("track", resized);

    // store prev state
    prevFeatures.assign(features.begin(), features.end());
    prev = gray;

    // Hit c to break
    if (cv::waitKey(1) == 'c')
      break;
  }
  cout << "[break]" << endl;

  capture.release();
  cout << "video capture released" << endl;
}
