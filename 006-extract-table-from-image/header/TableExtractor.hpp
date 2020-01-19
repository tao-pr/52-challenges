#ifndef TABLE_EXTRACT_HPP
#define TABLE_EXTRACT_HPP

#include <string>
#include <vector>

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "Extractor.hpp"
#include "Table.hpp"

using namespace cv;
using namespace std;


template class Extract<Table>;

/**
 * Table extractor
 */
class TableExtract : Extract<Table>
{
public:
  inline TableExtract() {};
  inline ~TableExtract() {};

  inline vector<Table> extract(Mat& im) const 
  {
    // Extract potential horizontal & vertical lines
    LineSpatialMap lines = extractLines(im);

    // Expand each line until it reaches the closest profile line in the another orientation
    set<int> profileRow, profileCol;
    tie(profileCol, profileRow) = lines.profile1D();

    vector<Boundary> horz = lines.horz;
    vector<Boundary> vert = lines.vert;

    // Maximum extension is up to 10% of the image width
    const int perimeter = (int)(0.1 * im.cols);

    for (auto h : lines.horz)
    {
      int newMin = (int)h.x;
      int newMax = (int)(h.x + h.width);
      
      // Extend to the left
      for (int x=newMin; x>0 && x>newMin-perimeter; x--)
        if (profileCol.find(x) != profileCol.end())
        {
          newMin = x;
          break;
        }

      // Extend to the right
      for (int x=newMax; x<im.cols-1 && x<newMax+perimeter; x++)
        if (profileCol.find(x) != profileCol.end())
        {
          newMax = x;
          break;
        }

      Boundary b = h;
      b.x = newMin;
      b.width = newMax - newMin;
      horz.push_back(b);
    }

    for (auto v : lines.vert)
    {
      int newMin = (int)v.y;
      int newMax = (int)(v.y + v.height);
      
      // Extend to the top
      for (int y=newMin; y>0 && y>newMin-perimeter; y--)
        if (profileRow.find(y) != profileRow.end())
        {
          newMin = y;
          break;
        }

      // Extend to the bottom
      for (int y=newMax; y<im.rows-1 && y<newMax+perimeter; y++)
        if (profileRow.find(y) != profileRow.end())
        {
          newMax = y;
          break;
        }

      Boundary b = v;
      b.y = newMin;
      b.height = newMax - newMin;
      vert.push_back(b);
    }


#ifdef DEBUG
    Mat canvas = Mat::ones(im.rows, im.cols, CV_8UC3);
    canvas = Scalar(255, 255, 255);
    for (auto x : profileCol)
      line(canvas, Point2d(x,0), Point2d(x,im.rows-1), Scalar(110,110,110));

    for (auto y : profileRow)
      line(canvas, Point2d(0,y), Point2d(im.cols-1,y), Scalar(110,110,110));

    for (auto h : horz)
      rectangle(canvas, h.tl(), h.br(), Scalar(0,130,0), 3);
    
    for (auto v : vert)
      rectangle(canvas, v.tl(), v.br(), Scalar(0,0,130), 3);

    imshow("extended", canvas);
    imwrite("./bin/lines-extended.jpg", canvas);
#endif
    vector<Table> v;


    return v;
  };
};

#endif