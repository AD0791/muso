import pytest
from musoapp import __version__, __app_name__
from musoapp.cli import app
from typer.testing import CliRunner


runner = CliRunner()

def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout
