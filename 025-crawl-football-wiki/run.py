from crawler.lib import *

if __name__ == '__main__':
  matches = download_team_page('https://en.wikipedia.org/wiki/2014–15_Real_Madrid_CF_season')
  print(matches)