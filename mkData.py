import fileinput
import json
import html
import urllib.parse

NUTRI_INFO = '<span class="cw-type__h2 Ingredients-title">Ingredients</span>'
CALORIC = '<span class="cw-type__h2 Caloric Content-title">Caloric Content</span>'

translateTable = str.maketrans({
    '\u00a0': ' ',
    '\u00e9': 'e',
    '\u00ac': '',
    '"': '',
})


class Foods:
  def __init__(self):
    self.result = []
    self.parse()
    print(json.dumps(self.result, indent=2))

  def processWord(self, word: str):
    if '(' in word:
      word = word.split('(')[1]
    if ')' in word:
      word = word.split(')')[0]
    return word

  def getIngredients(self, line: str):
    return [
        self.processWord(x.strip())
        for x in line.strip().split('.')[0].split(':')[-1].split(',')
    ]

  def getCalories(self, line: str):
    return line.split('<')[0].strip()

  def name2url(self, name: str):
    return name[name.find('http'):].translate(str.maketrans('_', '/'))

  def decode(self, line: str):
    return html.unescape(
        line.encode('latin-1', errors='ignore').decode('unicode_escape')
    ).translate(translateTable)

  def parse(self):
    skip = -1
    skipping = None
    title = None
    brand = ''
    ingredients = None
    calories = None
    filename = ''

    for line in fileinput.input():
      if fileinput.isfirstline():
        if title:
          self.result.append({
              'name': self.decode(title),
              'url': urllib.parse.unquote(self.name2url(filename)),
              'brand': self.decode(brand),
              'calories': calories,
              'ingredients': ingredients,
          })
        title = None
        brand = ''
        ingredients = None
        filename = fileinput.filename()
      if title is None and '<title>' in line:
        title = line.split('>')[1].split(',')[0]
      if not brand and 'brand:' in line:
        brand = line.split("'")[1]
      if skip > 0:
        skip -= 1
      elif skip == 0:
        skip = -1
        if skipping == 'nutri':
          ingredients = self.getIngredients(self.decode(line))
        elif skipping == 'caloric':
          calories = self.getCalories(self.decode(line))
          fileinput.nextfile()
      elif NUTRI_INFO in line:
        skip = 1
        skipping = 'nutri'
      elif CALORIC in line:
        skip = 1
        skipping = 'caloric'


Foods()