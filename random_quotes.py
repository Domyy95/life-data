import os
import random
from settings import margin

obsidian_book_directory = "/Users/dominic/Personal/second-brain/Resources/Book notes"
obsidian_quotes_file = "/Users/dominic/Personal/second-brain/Resources/lists/Quotes.md"
file_obsidian = [f for f in os.listdir(obsidian_book_directory) if f.endswith(".md")]


def select_random_row(da_file):
    result = ""
    while result.strip() == "" or result == None or "![" in result:
        with open(da_file, "r", encoding="utf-8") as file:
            rows = file.readlines()
            if rows is not None:
                result = random.choice(rows)

    return result


def select_random_quote(da_file):
    result = ""
    while (
        result.strip() == ""
        or result.strip() == ">"
        or result == None
        or "-" not in result
        or "[M" in result
        or "[[" in result
    ):
        with open(da_file, "r", encoding="utf-8") as file:
            rows = file.readlines()
            result = random.choice(rows)

    result = (
        result.replace("“", "")
        .replace("”", "")
        .replace('"', "")
        .replace("-", "")
        .strip()
    )
    return result


def main():
    extracted_quote = select_random_quote(obsidian_quotes_file)
    print(f"Quote of the day: {extracted_quote}\n")

    extracted_file = random.choice(file_obsidian)
    file_path = os.path.join(obsidian_book_directory, extracted_file)
    extracted_row = select_random_row(file_path)

    print(f"Da {extracted_file[:-3]}:")
    print(extracted_row)
    print(margin)


if __name__ == "__main__":
    main()
