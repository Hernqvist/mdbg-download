from urllib.request import urlopen
from html.parser import HTMLParser
import urllib.parse
import re

def get_url(sign):
  url = "https://www.mdbg.net/chinese/dictionary?page=worddict&wdqb=" \
     + urllib.parse.quote(sign)
  return url

class Word():
  defs = []
  pinyin = ""
  pinyin_code = ""
  strokes = None
  sign = ""

  def get_sound(self):
    url = "https://www.mdbg.net/chinese/rsc/audio/voice_pinyin_pz/{}.mp3" \
        .format(self.pinyin_code.lower())

  def get_strokes(self):
    url = "https://www.mdbg.net/chinese/dictionary-ajax?c=cdqchi&i={}" \
        .format(urllib.parse.quote(self.sign))




class MyHTMLParser(HTMLParser):
  word_depth = 0
  depth = 1
  words = []
  in_defs = False
  defs = []

  def handle_starttag(self, tag, attrs):
    self.depth += 1

    if tag == "tr" and ("class", "row") in attrs:
      self.word_depth = self.depth
      self.words += [Word()]
      print("Encountered a new word")

    if self.word_depth != 0 and self.depth == self.word_depth + 3 and tag == "a":
      try:
        onclick = list(filter(lambda x: x[0] == "onclick", attrs))[0][1]
        result = re.compile('.\|.*[0-9]').search(onclick).group()
        if result:
          sign, pinyin_code = tuple(result.split('|'))
          self.words[-1].sign = sign
          self.words[-1].pinyin_code = pinyin_code
          print("* Found sign and sound", sign, pinyin_code)
      except:
        pass

    if self.word_depth != 0 and ("class", "defs") in attrs:
      self.in_defs = True


  def handle_endtag(self, tag):
    if self.depth == self.word_depth:
      self.word_depth = 0
      print()

    if self.in_defs and tag == "div":
      self.in_defs = False
      defs = [x.strip() for x in self.defs if x != "/"]
      self.defs = []

      self.words[-1].defs = defs
      print("* Found defs:", defs)

    self.depth -= 1

  def handle_data(self, data):
    if self.in_defs:
      self.defs += [data]
    pass #print("Encountered some data  :", data)


if __name__ == "__main__":
  print("Enter character")
  sign = "累" #input()
  print(sign)

  html = urlopen(get_url(sign)).read().decode('utf-8')
  parser = MyHTMLParser()
  parser.feed(html)