from lxml import html
import unidecode
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

  def is_score(a):
    w = a.replace(' ', '').replace('–','-')
    if len(w) != 3:
      return False
    return all(['0'<=i<='9' for i in w.split('-')])

  def to_score(a):
    return a.replace(' ', '').replace('–','-')

  def iterate_and_clean(scores):
    ss = [s.strip() for s in scores]
    pp = []
    is_skipping = False
    for s in scores:
      if s.strip()=='(':
        is_skipping = True
      if s.strip()==')':
        is_skipping = False
      if not is_skipping and is_score(s):
        pp.append(to_score(s))
    return pp

  def cleanse(a):
    return unidecode.unidecode(a.strip().replace('\xa0', ' '))

  PATH_TEAMS = '//td[@class="vcard attendee"]//text()'
  PATH_SCORES = '//td[@class="vcard attendee"]/following-sibling::td//text()'

  teams = [cleanse(a) for a in tree.xpath(PATH_TEAMS) if len(a) > 3]
  teams = list(zip(teams[::2], teams[1:][::2]))
  scores = iterate_and_clean([a for a in tree.xpath(PATH_SCORES) if len(a)<10])

  return [(a[0],b,a[1]) for a,b in zip(teams,scores)]