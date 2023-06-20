import argparse
import requests
import validators
import unicodedata
from bs4 import BeautifulSoup

class Replacer:
  __unicode_fraction_descriptors = {
      "ZERO": 0,
      "ONE": 1,
      "TWO": 2,
      "THREE": 3,
      "FOUR": 4,
      "FIVE": 5,
      "SIX": 6,
      "SEVEN": 7,
      "EIGHT": 8,
      "NINE": 9,
      "HALF": 2,
      "HALVES": 2,
      "THIRD": 3,
      "THIRDS": 3,
      "QUARTER": 4,
      "QUARTERS": 4,
      "FIFTH": 5,
      "FIFTHS": 5,
      "SIXTH": 6,
      "SIXTHS": 6,
      "SEVENTH": 7,
      "SEVENTH": 7,
      "EIGHTH": 8,
      "EIGHTHS": 8,
      "NINTH": 9,
      "NINTHS": 9,
  }

  @classmethod
  def __replace_fraction(cls, unicode_name):
    fraction_parts = unicode_name.split("FRACTION")[1].strip().split(' ')

    return "/".join([str(cls.__unicode_fraction_descriptors[x]) for x in fraction_parts])

  @classmethod
  def __is_latin(cls, string: str):
    end_of_latin_unicode_space = int('0x1EFF', 16)
    return ord(string) <= end_of_latin_unicode_space

  @classmethod
  def replace(cls, string: str):
    if cls.__is_latin(string):
      un = unicodedata.name(string)
      if "FRACTION" in un:
        return cls.__replace_fraction(un)

      return string

    return ""

  @classmethod
  def replace_all(cls, string: str):
    return "".join([ cls.replace(char) for char in string ]).strip()

def extract_wprm(soup: BeautifulSoup):
  '''
  Extract the recipe from a WordPress Recipe Manager page.

  TODO: This is really brittle and based on me literally looking at the DOM.
        Next iteration should make this more flexible by utilizing more DOM queries.
  '''
  recipe_container = soup.find_all("div", {"class": "wprm-recipe-container"})
  if recipe_container is None:
    print("not a wprm recipe")
    return None

  [recipe_name] = soup.select(".wprm-recipe-name")
  print(f"# {recipe_name.text}")

  ingredients = soup.find_all("li", {"class": "wprm-recipe-ingredient" })
  if len(ingredients) > 0:
    print("## Ingredients")
    print('\n'.join([f"* {Replacer.replace_all(i.text)}" for i in ingredients]))

  print("")

  instructions = soup.find_all("li", {"class": "wprm-recipe-instruction" })
  if len(instructions) > 0:
    print("## Instructions")
    print('\n'.join([
      f"{e+1}. {Replacer.replace_all(i.text)}" for e, i in enumerate(instructions)
    ]))

def init_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
      usage="%(prog)s [URL]",
      description="save a recipe from the internet to a Markdown file"
  )
  parser.add_argument("url")
  return parser

def main() -> None:
  parser = init_parser()
  args = parser.parse_args()

  if not validators.url(args.url):
    raise Exception(f"'{args.url}' is not a valid url")

  data = requests.get(args.url, headers={"user-agent": "recipes/1.0.1"})
  soup = BeautifulSoup(data.text, features="html.parser")
  extract_wprm(soup)

if __name__ == "__main__":
  main()
