import requests

titles = [] # list of strings

for title in titles:
  response = requests.get(
    'https://bg.wikipedia.org/w/api.php',
    params={
      'action': 'query',
      'format': 'json',
      'titles': title,
      'prop': 'extracts',
      'explaintext': True,
    }
  ).json()

  page = next(iter(response['query']['pages'].values()))

  f = open('fetched-wiki.txt', 'a')
  f.write(page['extract'])
  f.close()