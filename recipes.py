import argparse
import requests
import validators
import extractor
from bs4 import BeautifulSoup


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [URL]",
        description="save a recipe from the internet to a Markdown file",
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
    extractor.extract(soup)


if __name__ == "__main__":
    main()