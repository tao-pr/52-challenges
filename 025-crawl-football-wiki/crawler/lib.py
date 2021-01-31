from lxml import html
import requests

def crawl_pages_by_pattern(url_template, arange):
  """
  Crawl multiple pages by varying the params
  """
  pass

def download_team_page(url):
  """
  Download structured content from the URL
  eg. https://en.wikipedia.org/wiki/2007%E2%80%9308_Real_Madrid_CF_season#Matches
  """
  page = requests.get(url)
  tree = html.fromstring(page.content)

  matches = tree.xpath('//div[@class="vevent"]/table/tbody')

  # TAOTODO query from XPATH

  pass