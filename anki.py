import mdbg, genanki, argparse, random

list_file = "list.txt"

def update_list(word):
  with open(list_file, 'r') as file:
    lst = file.read().split()
  if not word in lst:
    lst += [word]
  with open(list_file, 'w') as file:
    file.write("\n".join(lst))

def add_word():
  word = mdbg.run()
  update_list(word.sign)

def build(name):
  deck = genanki.Deck(123454321, name)
  model = genanki.Model(
    1234321,
    'Chinese Generated',
    fields=[
      {'name': 'English'},
      {'name': 'Pinyin'},
      {'name': 'Hanzi'},
      {'name': 'Strokes'},
      {'name': 'Pronounce'},
    ],
    templates=[
      {
        'name': 'From English',
        'qfmt': '{{English}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Pinyin}}<br/>{{Strokes}}<br/>{{Pronounce}}',
      },
      {
        'name': 'From Sign',
        'qfmt': '{{Hanzi}}<br/>{{Strokes}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Pinyin}}<br/>{{English}}<br/>{{Pronounce}}',
      },
      {
        'name': 'From Pinyin',
        'qfmt': '{{Pinyin}}<br/>{{Pronounce}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{English}}<br/>{{Strokes}}',
      }
    ],
    css="""
      .card {
        font-family: arial;
        font-size: 20px;
        text-align: center;
        color: black;
        background-color: white;
      }"""
  )
  media_files = []

  with open(list_file, 'r') as file:
    words = file.read().split()
  for word in words:
    strokes, pronounce = word + '.gif', word + '.mp3',
    with open(word + '.txt', 'r') as file:
      sign, pinyin, definition = tuple(file.read().split('\n'))[:3]

    note = genanki.Note(
      model=model,
      fields=[definition, pinyin, sign, \
          '<img src="{}">'.format(strokes), \
          '[sound:{}]'.format(pronounce)])
    media_files += [strokes, pronounce]

    deck.add_note(note)

  package = genanki.Package(deck)
  package.media_files = media_files
  package.write_to_file(name + '.apkg')


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--build", default=None, type=str, help="build the deck")
  args = parser.parse_args()
  
  if args.build:
    build(args.build)
  else:
    while True:
      add_word()