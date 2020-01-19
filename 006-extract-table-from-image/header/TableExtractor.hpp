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


    // TAOTODO
    vector<Table> v;


    return v;
  };
};

#endif