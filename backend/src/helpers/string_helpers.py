import re


def slugify(text, separator="-"):
    """Standardizes strings: lowercase, no special chars, custom separator."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_-]+", separator, text)


def clean_filename(name):
    """Removes characters that are illegal in Windows/Linux filenames."""
    return re.sub(r'[\\/*?:"<>|]', "", name)


def clean_str(input_str):
    return input_str.lower().replace(" ", "-")


def swap_spaces(istr, schar="_"):
    return istr.replace(" ", schar)
