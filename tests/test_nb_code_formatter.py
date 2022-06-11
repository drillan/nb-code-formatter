import shutil
import tempfile

from click.testing import CliRunner
import nbformat
import nb_code_formatter


def test_cli():
    runner = CliRunner()

    with tempfile.NamedTemporaryFile() as tmpf:
        result = runner.invoke(
            nb_code_formatter.main, ["tests/sample.ipynb", tmpf.name]
        )
        assert result.exit_code == 0
        nb = nbformat.read(tmpf.name, as_version=nb_code_formatter.NBFORMAT_VERSION)
        assert nb["cells"][1]["source"] == 'spam = "ham" * 3\n'
        assert (
            nb["cells"][2]["source"] == "import abc\nimport datetime\n\nimport isort\n"
        )
        assert (
            nb["cells"][3]["source"]
            == 'def longlonglonglonglonglonglonglonglong_functionname(\n    longlonglonglong_arg1: str = "abc",\n    longlonglonglong_arg2: int = 1,\n    longlonglonglong_arg3: float = 1.1,\n):\n    return arg1 * int(arg2 + arg3)\n'
        )


def test_cli_overwrite():
    runner = CliRunner()

    with tempfile.NamedTemporaryFile() as tmpf:
        shutil.copyfile("tests/sample.ipynb", tmpf.name)
        result = runner.invoke(nb_code_formatter.main, [tmpf.name])
        assert result.exit_code == 0
        nb = nbformat.read(tmpf.name, as_version=nb_code_formatter.NBFORMAT_VERSION)
        assert nb["cells"][1]["source"] == 'spam = "ham" * 3\n'
        assert (
            nb["cells"][2]["source"] == "import abc\nimport datetime\n\nimport isort\n"
        )
        assert (
            nb["cells"][3]["source"]
            == 'def longlonglonglonglonglonglonglonglong_functionname(\n    longlonglonglong_arg1: str = "abc",\n    longlonglonglong_arg2: int = 1,\n    longlonglonglong_arg3: float = 1.1,\n):\n    return arg1 * int(arg2 + arg3)\n'
        )
