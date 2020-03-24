import os
import re
import tarfile
from contextlib import contextmanager

import requests


def extract_package_info(package_name, version):
    description = get_package_description(package_name, version)
    cleaned_package_description = clean_package_description(
        parse_package_description(description)
    )
    cleaned_package_description["name"] = package_name
    cleaned_package_description["version"] = version
    return cleaned_package_description


@contextmanager
def temp_tarfile(path):
    f = tarfile.open(path)
    try:
        yield f
    finally:
        f.close()
        os.remove(path)


def get_package_description(package_name, version):
    response = requests.get(
        f"https://cran.r-project.org/src/contrib/{package_name}_{version}.tar.gz",
        stream=True,
    )
    with open(f"{package_name}_{version}.tar.gz", mode="wb") as f:
        f.write(response.raw.read())

    with temp_tarfile(f"{package_name}_{version}.tar.gz") as f:
        desc = f.extractfile(f"{package_name}/DESCRIPTION").read().decode("utf-8")
        return desc


def parse_package_description(description_text):
    title = re.compile(r".*Title: (?P<title>.+?)\n[A-Z]", re.DOTALL)
    description = re.compile(r".*Description: (?P<description>.+?)\n[A-Z]", re.DOTALL)
    maintainers = re.compile(r".*Maintainer: (?P<maintainers>.+?)\n[A-Z]", re.DOTALL)
    authors = re.compile(r".*Author: (?P<authors>.+?)\n[A-Z]", re.DOTALL)
    published_at = re.compile(
        r".*Publication: (?P<published_at>\d{4}-\d{2}-\d{2})", re.DOTALL
    )
    emails = re.compile(r"<(.+@.+)>", re.DOTALL)

    result = {}
    for pattern in [title, description, maintainers, authors, published_at]:
        result = {**result, **pattern.match(description_text).groupdict()}

    result["maintainers_email"] = ",".join(emails.findall(result["maintainers"]))
    return result


def clean_package_description(parsed_description):
    unwanted_brackets = re.compile(r"[\[\(<].+?[\]\)>]")
    spaces_before_after_comma = re.compile(r" ,|, ")
    multiple_or_trailing_spaces = re.compile(r"\n[\s\t]+| $")

    patterns, replacement_chars = (
        [unwanted_brackets, spaces_before_after_comma, multiple_or_trailing_spaces],
        ["", ",", ""],
    )
    for pattern, replacement_char in zip(patterns, replacement_chars):
        for key, value in parsed_description.items():
            if (pattern == unwanted_brackets) and (key == "description"):
                parsed_description[key] = value
            else:
                parsed_description[key] = pattern.sub(replacement_char, value)
    return parsed_description
