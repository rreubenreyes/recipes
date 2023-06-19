import argparse
import requests
import validators
import re
from bs4 import BeautifulSoup

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

  ingredients = soup.find_all("li",{"class": "wprm-recipe-ingredient" })
  if len(ingredients) > 0:
    print("## Ingredients")
    for i in ingredients:
      match = re.search(r"([\w]+[\w\s\.]+)", i.text)
      if match:
        ingredient = match.group(0)
        print(f"* {ingredient}")

  print("")

  instructions = soup.find_all("li",{"class": "wprm-recipe-instruction" })
  if len(instructions) > 0:
    print("## Instructions")
    for e, i in enumerate(instructions):
      print(f"{e + 1}. {i.text.strip()}")

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
