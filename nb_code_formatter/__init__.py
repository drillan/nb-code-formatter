import re

import black
import click
import isort
import nbformat

__version__ = "0.1.0"
NBFORMAT_VERSION = 4


def black_formatter(cell_text):
    cell_text = re.sub("^%", "#%#", cell_text, flags=re.M)
    reformated_text = black.format_str(cell_text, mode=black.FileMode())
    return re.sub("^#%#", "%", reformated_text, flags=re.M)


def format_code(cell_text):
    return isort.code(black_formatter(cell_text))


def format_nb(nb):
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            cell["source"] = format_code(cell["source"])
    return nb


def format_file(src, dst=None):
    if dst is None:
        dst = src

    nb = nbformat.read(src, as_version=NBFORMAT_VERSION)
    nbformat.write(format_nb(nb), dst)


@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.File("w"), required=False)
def main(src, dst=None):
    format_file(src, dst)
