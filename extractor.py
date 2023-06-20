import replacer
import typing
from bs4 import BeautifulSoup

_Clue = typing.Tuple[str | None, typing.Dict[str, str]]


class _Extractor:
    def __init__(
        self,
        identifier: _Clue,
        recipe_name: _Clue,
        ingredients: _Clue,
        instructions: _Clue,
        nutrition: _Clue,
    ):
        self.identifier = identifier
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.instructions = instructions
        self.nutrition = nutrition

    def can_extract(self, soup: BeautifulSoup) -> bool:
        return soup.find(*self.identifier) is not None

    def extract_recipe_name(self, soup: BeautifulSoup) -> str:
        recipe_name = soup.find(*self.recipe_name)
        if recipe_name is None:
            return ""

        return recipe_name.text.strip()

    def extract_ingredients(self, soup: BeautifulSoup) -> str:
        ingredients = soup.find_all(*self.ingredients)
        if len(ingredients) <= 0:
            return ""

        return "\n".join(
            [f"* {replacer.replace_all(i.text)}" for i in ingredients]
        ).strip()

    def extract_instructions(self, soup: BeautifulSoup) -> str:
        instructions = soup.find_all(*self.instructions)
        if len(instructions) <= 0:
            return ""

        print("## Instructions")
        return "\n".join(
            [
                f"{e+1}. {replacer.replace_all(i.text)}"
                for e, i in enumerate(instructions)
            ]
        ).strip()


_extractors = [
    # WordPress Recipe Manager
    _Extractor(
        identifier=(None, {"class": "wprm-recipe-container"}),
        recipe_name=(None, {"class": "wprm-recipe-name"}),
        ingredients=("li", {"class": "wprm-recipe-ingredient"}),
        instructions=("li", {"class": "wprm-recipe-instruction"}),
        nutrition=("span", {"class": "wprm-nutrition-label-text-nutrition-container"}),
    ),
]


def extract(soup: BeautifulSoup):
    """
    Extract the recipe from a WordPress Recipe Manager page.

    TODO: This is really brittle and based on me literally looking at the DOM.
    Next iteration should make this more flexible by utilizing more DOM queries.
    """

    extractor = None
    for n, x in enumerate(_extractors):
        if x.can_extract(soup):
            extractor = x
            break
        if n == len(_extractors) - 1:
            print("cannot extract recipe from this page; layout may not be supported")
            return None

    if extractor is None:
        raise Exception("something went terribly wrong")

    recipe_name = extractor.extract_recipe_name(soup)
    ingredients = extractor.extract_ingredients(soup)
    instructions = extractor.extract_instructions(soup)

    print(
        f"# {recipe_name}\n"
        "\n"
        "## Ingredients\n"
        "\n"
        f"{ingredients}\n"
        "\n"
        "## Instructions\n"
        "\n"
        f"{instructions}"
    )