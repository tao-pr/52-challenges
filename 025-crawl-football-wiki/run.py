from crawler.lib import *


if __name__ == '__main__':
  teams = ['Real_Madrid_CF']
  year = range(5,21)
  year = list(zip(year, year[1:]))

  # Download wikis
  all_matches = {}
  for t in teams:
    print(f'Downloading team : {t}')
    for a,b in year:
      page = f'https://en.wikipedia.org/wiki/20{a:02d}–{b:02d}_{t}_season'
      print(f'... Downloading page : {page}')
      matches = download_team_page(page)
      for home, score, away in matches:
        if home not in all_matches:
          all_matches[home] = {}
        if away not in all_matches[home]:
          all_matches[home][away] = []
        all_matches[home][away].append((f'20{a:02d}', home, score, away))

  # REPL
  N = len(all_matches)
  print(f'{N} matches collected!')
  
  while True:
    print('----------------------')  
    print('Lets query matches!')
    home = input('Home : ')
    away = input('Away : ')
    
    if not home in all_matches or not away in all_matches[home]:
      print('NOT FOUND!')
      continue

    for y, h, score, a in all_matches[home][away]:
      print(f'   {y} : {h} {score} {a}')