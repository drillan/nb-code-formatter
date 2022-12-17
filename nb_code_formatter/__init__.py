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
    return black.format_str(cell_text, mode=black.FileMode())


def _format_code(cell_text: str) -> str:
    return isort.code(black_formatter(cell_text)).rstrip()


def _format_linemagic(line: str):
    pat: re.Pattern = re.compile(r"^(%\w+)\s+(.*)")
    result: re.Match | None = pat.match(line)
    magic_command: str = result.group(1)
    python_code: str = result.group(2)
    return " ".join((magic_command, black_formatter(python_code)))


def _format_magic_code(cell_text: str, code_type: str) -> str:
    lines: list = cell_text.split("\n")
    magic: str = lines[0]
    if code_type == "line_magic":
        magic: str = _format_linemagic(lines[0])
    code: str = "\n".join(lines[1:])
    formated_code: str = _format_code(code)
    return "\n".join((magic, formated_code)).rstrip()


def _format_cellmagic_code(cell_text: str) -> str:
    return _format_magic_code(cell_text, "cell_magic")


def _format_linemagic_code(cell_text: str) -> str:
    return _format_magic_code(cell_text, "line_matic")


def get_code_type(source: str) -> str:
    if not source:
        return "pure_python"
    elif source[:2] == "%%":
        return "cell_magic"
    elif source[0] == "%":
        return "line_magic"
    else:
        return "pure_python"


def format_code(cell_text: str) -> str:
    code_type: str = get_code_type(cell_text)
    return {
        "pure_python": _format_code,
        "cell_magic": _format_cellmagic_code,
        "line_magic": _format_linemagic_code,
    }[code_type](cell_text)


def format_nb(nb: NotebookNode) -> NotebookNode:
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            cell["source"] = format_code(cell["source"])
    return nb


def format_file(src: str | pathlib.Path, dst: str | pathlib.Path | None = None) -> None:
    if dst is None:
        dst = src

    nb: nbformat.notebooknode.NotebookNode = nbformat.read(
        src, as_version=NBFORMAT_VERSION
    )
    nbformat.write(format_nb(nb), dst)


@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.File("w"), required=False)
def main(src: str, dst: str = None):
    format_file(src, dst)
