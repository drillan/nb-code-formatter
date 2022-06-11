from __future__ import annotations
import re
import pathlib

import black
import click
import isort
import nbformat
from nbformat.notebooknode import NotebookNode

__version__ = "0.1.1"
NBFORMAT_VERSION = 4


def black_formatter(cell_text: str) -> str:
    drop_magic_text: str = re.sub("^%", "#%#", cell_text, flags=re.M)
    reformated_text: str = black.format_str(drop_magic_text, mode=black.FileMode())
    return re.sub("^#%#", "%", reformated_text, flags=re.M)


def format_code(cell_text: str) -> str:
    return isort.code(black_formatter(cell_text))


def format_nb(nb: NotebookNode) -> NotebookNode:
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            cell["source"] = format_code(cell["source"])
    return nb


def format_file(src: str | pathlib.Path, dst: str | pathlib.Path | None = None) -> None:
    if dst is None:
        dst = src

    nb = nbformat.read(src, as_version=NBFORMAT_VERSION)
    nbformat.write(format_nb(nb), dst)


@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.File("w"), required=False)
def main(src: str, dst: str = None):
    format_file(src, dst)
