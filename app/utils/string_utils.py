import re


def format_name(name: str) -> str:
    # Step 1 & 2: lowercase and remove non a-z characters except spaces
    cleaned = re.sub(r"[^a-z ]", "", name.lower())

    # Step 3: capitalize first letter of each word (initcap equivalent)
    initcapped = cleaned.title()

    # Step 4: replace one or more spaces with underscore
    result = re.sub(r"\s+", "_", initcapped)

    return result
