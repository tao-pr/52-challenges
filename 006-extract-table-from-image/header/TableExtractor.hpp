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
    vector<Table> vt;

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

    // Extract horizontal boundary of each table (in case of multiple tables per image)
    Table tb;
    int x0 = im.cols;
    int x1 = 0;
    int y0 = im.rows;
    int y1 = 0;

    for (auto y : profileRow)
    {
#ifdef DEBUG
      cout << "Processing profile y = " << y << endl;
#endif

      if (y0 == im.rows)
      {
        // Identify the beginning of a new table (y)
        y0 = y;
#ifdef DEBUG
        cout << "Beginning table @ y = " << y << endl;
#endif
        int numVerticalLines = 0;
        for (auto l : vert)
        {
          // List all vertical lines beginning from the beginning y position
          if (l.y == y0)
          {
            tb.verticals.insert(l.x);
            numVerticalLines++;
            y1 = max((int)(l.y + l.height), (int)y1); // We'll also identify the ending of the table (y position)
            x0 = min((int)l.x, (int)x0);
            x1 = max((int)l.x, (int)x1);
#ifdef DEBUG
            cout << "added vertical line @ x = " << l.x << ", which stretches to y1 = " << y1 << endl;
#endif
          }
        }

        // If there is no vertical lines (or even just only one) starting from this line,
        // then ignore this
        if (numVerticalLines <= 1)
        {
          // Reset!
          // Throw away the beginning of the table we marked earlier
          // This will look for another candidate
#ifdef DEBUG
          cout << "Skipping horizontal line @ y = " << y << endl;
#endif
          x0 = im.cols;
          x1 = 0;
          y0 = im.rows;
          y1 = 0;
          tb.verticals.clear();
          tb.horizontals.clear();
        }
      }
      else if (y == y1 && y1 != 0) // Reach the end of the table
      {
        // To be a table, at least 2 vertical lines are required.
        if (tb.verticals.size() >= 2)
        {
          tb.region = Rect(x0, y0, x1-x0, y1-y0);
          vt.push_back(tb);
#ifdef DEBUG
          cout << "End of table @ y = " << y << endl;
#endif
          // Reset!
#ifdef DEBUG
          cout << "Dropping table candidate" << endl;
          cout << "  vertical lines   : " << tb.verticals.size() << endl;
          cout << "  horizontal lines : " << tb.horizontals.size() << endl;
#endif

          x0 = im.cols;
          x1 = 0;
          y0 = im.rows;
          y1 = 0;
          tb.verticals.clear();
          tb.horizontals.clear();

        }
        else
        {
          // Reset!
          // Throw away the beginning of the table we marked earlier
          // This will look for another candidate
#ifdef DEBUG
          cout << "Dropping table candidate" << endl;
          cout << "  vertical lines   : " << tb.verticals.size() << endl;
          cout << "  horizontal lines : " << tb.horizontals.size() << endl;
#endif

          x0 = im.cols;
          x1 = 0;
          y0 = im.rows;
          y1 = 0;
          tb.verticals.clear();
          tb.horizontals.clear();
        }
      }
      else
      {
        // Reach another row, not yet the last horizontal line
        // Also list another vertical row starting from this point (if any)
        for (auto l : vert)
        {
          if (l.y == y)
          {
            tb.verticals.insert(l.x);
          }
        }

        // Identify horizontal line at this y position
        for (auto l : horz)
        {
          if (l.y == y)
          {
            tb.horizontals.insert(l.y);
            break;
          }
        }
      }
    }


#ifdef DEBUG
    Mat canvas = Mat::ones(im.rows, im.cols, CV_8UC3);
    canvas = Scalar(255, 255, 255);

    // Draw tables
    for (auto tb : vt)
      tb.drawTo(canvas);

    // Draw projections of all lines
    for (auto x : profileCol)
      line(canvas, Point2d(x,0), Point2d(x,im.rows-1), Scalar(110,110,110));

    for (auto y : profileRow)
      line(canvas, Point2d(0,y), Point2d(im.cols-1,y), Scalar(110,110,110));

    for (auto h : horz)
      rectangle(canvas, h.tl(), h.br(), Scalar(0,130,0), 1);
    
    for (auto v : vert)
      rectangle(canvas, v.tl(), v.br(), Scalar(0,0,130), 1);

    imshow("extended", canvas);
    imwrite("./bin/lines-extended.jpg", canvas);
#endif

    return vt;
  };
};

#endif