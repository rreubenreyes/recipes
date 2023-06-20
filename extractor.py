import replacer
from bs4 import BeautifulSoup, Tag, NavigableString, PageElement

_Clue = tuple[str | None, dict[str, str]]


class _Extractor:
    def __init__(
        self,
        identifier: _Clue,
        recipe_name: _Clue,
        ingredients: _Clue,
        instructions: _Clue,
        nutrition: _Clue,
        notes: _Clue,
    ):
        self.identifier = identifier
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.instructions = instructions
        self.nutrition = nutrition
        self.notes = notes

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

        return "\n".join(
            [
                f"{e+1}. {replacer.replace_all(i.text)}"
                for e, i in enumerate(instructions)
            ]
        ).strip()

    def extract_nutrition(self, soup: BeautifulSoup) -> str:
        nutrition = soup.find_all(*self.nutrition)
        if len(nutrition) <= 0:
            return ""

        return "\n".join(
            [f"* {replacer.replace_all(n.text)}" for n in nutrition]
        ).strip()

    # @staticmethod
    # def _format_text(elem: PageElement) -> str:
    #     if not isinstance(elem, Tag) or isinstance(elem, NavigableString):
    #         return ""

    #     text = (
    #         elem.text.strip()
    #         if len(list(elem.children)) <= 0
    #         else "".join([_Extractor._format_text(child) for child in elem.children])
    #     )

    #     if elem.name == "span"
    #         return text
    #     if elem.name == "div"
    #         return f"text\n"
    #     if elem.name == "strong":
    #         return f"__{text}__"
    #     if elem.name == "li":
    #         return f"* {text}"
    #     if elem.name == "h1":
    #         return f"# {text}"
    #     if elem.name == "h2":
    #         return f"## {text}"
    #     if elem.name == "h3":
    #         return f"### {text}"
    #     if elem.name == "h4":
    #         return f"#### {text}"
    #     if elem.name == "h5":
    #         return f"##### {text}"

    #     # default: just return the text
    #     return elem.text.strip()

    def extract_notes(self, soup: BeautifulSoup) -> str:
        notes = soup.find(*self.notes)
        if notes is None:
            return ""

        return notes.get_text()

        # if isinstance(notes, NavigableString):
        #     return notes.text.strip()

        # return "".join([_Extractor._format_text(child) for child in notes.children])


_extractors = [
    # WordPress Recipe Manager
    _Extractor(
        identifier=(None, {"class": "wprm-recipe-container"}),
        recipe_name=(None, {"class": "wprm-recipe-name"}),
        ingredients=("li", {"class": "wprm-recipe-ingredient"}),
        instructions=("li", {"class": "wprm-recipe-instruction"}),
        nutrition=("span", {"class": "wprm-nutrition-label-text-nutrition-container"}),
        notes=("div", {"class": "wprm-recipe-notes"}),
    ),
    # Tasty Recipes
    # _Extractor(
    #     identifier=(None, {"class": "tasty-recipes"}),
    #     recipe_name=(None, {"class": "tasty-recipes-title"}),
    #     ingredients=("li", {"class": "tr-ingredient-checkbox-container"}),
    #     instructions=("li", {"class": "wprm-recipe-instruction"}),
    #     nutrition=("span", {"class": "wprm-nutrition-label-text-nutrition-container"}),
    #     notes=("div", {"class": "wprm-recipe-notes"}),
    # ),
]


def extract(soup: BeautifulSoup):
    """
    Extract the recipe from an HTML page.

    Supported frameworks:
    * WordPress Recipe Manager (wprm)
    * Tasty Recipes (tasty-recipes)
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
    nutrition = extractor.extract_nutrition(soup)
    notes = extractor.extract_notes(soup)

    print(
        f"# {recipe_name}\n"
        "\n"
        "## Ingredients\n"
        "\n"
        f"{ingredients}\n"
        "\n"
        "## Instructions\n"
        "\n"
        f"{instructions}\n"
        "\n"
        "## Author's Notes\n"
        "\n"
        f"{notes}\n"
        "\n"
        "## Nutrition\n"
        "\n"
        f"{nutrition}"
    )